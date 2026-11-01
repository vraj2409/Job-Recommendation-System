import pandas as pd
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.corpus import stopwords

# Download NLTK resources (will be called once)
def download_nltk_resources():
    """Download required NLTK resources."""
    resources = ['punkt', 'averaged_perceptron_tagger', 'wordnet', 'stopwords']
    for resource in resources:
        try:
            nltk.download(resource, quiet=True)
        except:
            pass

# POS TAG constants
ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'
POS_LIST = [NOUN, VERB, ADJ, ADV]

def nltk_pos_tagger(nltk_tag):
    """
    Map NLTK POS tags to WordNet POS tags.
    """
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

def keep_alpha_char(text):
    """
    Remove non-alphabetic characters, keeping only alphabetical characters.
    """
    if not isinstance(text, str):
        return ""
    alpha_only_string = re.sub(r'[^a-zA-Z]', ' ', text)
    cleaned_string = re.sub(r'\s+', ' ', alpha_only_string)
    return cleaned_string.strip()

def lemmatize_sentence(sentence):
    """
    Lemmatize the words in the input sentence.
    """
    if not isinstance(sentence, str) or not sentence.strip():
        return ""
    
    lemmatizer = WordNetLemmatizer()
    
    try:
        # Part-of-speech tagging using NLTK
        nltk_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))
        
        # Map NLTK POS tags to WordNet POS tags
        wordnet_tagged = map(lambda x: (x[0], nltk_pos_tagger(x[1])), nltk_tagged)
        
        lemmatized_sentence = []
        
        # Lemmatize each word based on its POS tag
        for word, tag in wordnet_tagged:
            if tag is not None:
                lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
            else:
                lemmatized_sentence.append(word)
        
        return " ".join(lemmatized_sentence)
    except:
        return sentence

def remove_stop_words(text):
    """
    Remove English stop words from the input text.
    """
    if not isinstance(text, str):
        return ""
    words = text.split()
    filtered = [w for w in words if w.lower() not in STOP_WORDS and len(w) > 1]
    return ' '.join(filtered)

def clean_text(text):
    """
    Full text cleaning pipeline.
    """
    if not isinstance(text, str):
        return ""
    text = keep_alpha_char(text)
    text = text.lower()
    text = remove_stop_words(text)
    return text

def pre_process_resume(resume_text):
    """
    Preprocesses a resume text.
    """
    return clean_text(resume_text)

# Common stop words to remove
STOP_WORDS = {
    'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'must', 'shall', 'can', 'this', 'that',
    'i', 'you', 'he', 'she', 'it', 'we', 'they', 'my', 'your', 'his', 'her',
    'their', 'our', 'its', 'me', 'him', 'us', 'them', 'who', 'which', 'what',
    'where', 'when', 'why', 'how', 'all', 'each', 'every', 'both', 'few',
    'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
    'own', 'same', 'so', 'than', 'too', 'very', 'just', 'also', 'now'
}

def preprocess_skills(skills_str):
    """Convert skills string to cleaned list."""
    if not isinstance(skills_str, str):
        return []
    skills = skills_str.split(';')
    return [clean_text(skill) for skill in skills]

def combine_features(row):
    """Combine multiple columns into a single text feature."""
    features = []
    
    if 'job_title' in row:
        features.append(str(row['job_title']) * 2)  # Weight title more
    if 'job_description' in row:
        features.append(str(row['job_description']))
    if 'required_skills' in row:
        features.append(str(row['required_skills']) * 2)  # Weight skills more
    if 'experience_level' in row:
        features.append(str(row['experience_level']))
    
    return ' '.join(features)

def load_data(filepath='data/jobs.csv'):
    """Load jobs data from CSV file."""
    return pd.read_csv(filepath)

def preprocess_skills(df):
    """Preprocess skills column."""
    df['skills_list'] = df['skills'].str.split(';')
    return df

def get_all_skills(df):
    """Extract all unique skills from the dataset."""
    all_skills = set()
    for skills in df['skills_list']:
        all_skills.update(skills)
    return list(all_skills)
