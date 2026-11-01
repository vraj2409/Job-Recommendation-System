import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from preprocess import clean_text

# Constants
NUM_POSTING = 50
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "job_posting.csv")

def load_job_data():
    """Load job data from CSV."""
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    raise FileNotFoundError(f"Job data not found at {DATA_PATH}")

def get_job_df():
    """Load and preprocess job database."""
    job_df = load_job_data()
    job_df = job_df.dropna(subset=['Role']).copy()
    job_df['data'] = job_df['Role'].apply(clean_text)
    return job_df

def get_top_features(resume_text, job_df, top_n=100):
    """Extract top keywords from resume using TF-IDF."""
    all_text = list(job_df['data']) + [resume_text]
    
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    tfidf_matrix = vectorizer.fit_transform(all_text)
    
    resume_vector = tfidf_matrix[-1]
    feature_names = np.array(vectorizer.get_feature_names_out())
    scores = resume_vector.toarray()[0]
    
    top_indices = np.argsort(scores)[::-1]
    top_features = feature_names[top_indices]
    top_scores = scores[top_indices]
    
    return top_features[top_scores > 0][:top_n]

def recommend_jobs(resume_text, job_df, num_posting=NUM_POSTING):
    """Recommend jobs based on resume using TF-IDF and cosine similarity."""
    all_text = list(job_df['data']) + [resume_text]
    
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000, ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(all_text)
    
    job_vectors = tfidf_matrix[:-1]
    resume_vector = tfidf_matrix[-1]
    
    similarities = cosine_similarity(resume_vector, job_vectors).flatten()
    top_indices = similarities.argsort()[::-1][:num_posting]
    
    result_df = job_df.iloc[top_indices].copy()
    result_df['Match %'] = (similarities[top_indices] * 100).round(1)
    
    return result_df
