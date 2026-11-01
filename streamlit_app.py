import streamlit as st
import pandas as pd
from io import BytesIO
import os

from model import get_job_df, get_top_features, recommend_jobs
from preprocess import clean_text
from file_parser import parse_resume

# Constants
NUM_POSTING = 50
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def make_clickable(link):
    """Create clickable HTML link."""
    if pd.isna(link) or not link or str(link).strip() == '':
        return ""
    return f'<a href="{link}" target="_blank">Apply Link</a>'

def download_buttons(df):
    """Create download buttons for CSV and Excel."""
    st.markdown("**Download the internship postings as CSV File**")
    
    download_df = df.drop(columns=['data'], errors='ignore')
    
    csv_buffer = BytesIO()
    excel_buffer = BytesIO()
    
    download_df.to_csv(csv_buffer, index=False)
    download_df.to_excel(excel_buffer, index=False, engine='openpyxl')
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("Download CSV", csv_buffer.getvalue(), 
                          "job_recommendations.csv", "text/csv")
    with col2:
        st.download_button("Download Excel", excel_buffer.getvalue(),
                          "job_recommendations.xlsx", 
                          "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

def display_keywords(resume_text, job_df):
    """Display extracted keywords from resume."""
    num_keywords = st.slider("Select keywords extracted from your resume:", 1, 100, 5)
    keywords = get_top_features(resume_text, job_df, num_keywords)
    st.markdown(f"**Selected {num_keywords} keywords:**")
    st.table(pd.DataFrame({"Top Keywords": keywords}))

def format_table(df):
    """Format dataframe for display."""
    columns = ['Role', 'Location', 'Application/Link', 'Date Posted', 'Match %']
    available = [c for c in columns if c in df.columns]
    
    display_df = df[available].copy()
    if 'Application/Link' in display_df.columns:
        display_df['Application/Link'] = display_df['Application/Link'].apply(make_clickable)
    
    display_df = display_df.reset_index(drop=True)
    display_df.index = display_df.index + 1
    return display_df

def main():
    """Main application."""
    st.set_page_config(page_title="Job Recommendation System", layout="wide")
    
    # CSS styling
    st.markdown("""
    <style>
        table { width: 100%; border-collapse: collapse; background-color: #1e2128; }
        th { background-color: #262730; color: #fff; padding: 12px; text-align: left; }
        td { padding: 12px; border-bottom: 1px solid #3d4148; color: #fff; }
        tr:hover { background-color: #262730; }
        a { color: #4da6ff; text-decoration: none; }
    </style>
    """, unsafe_allow_html=True)
    
    st.title('Internship Recommendations Based On Resume')
    st.markdown("**Author: Job Recommendation System**")
    
    st.markdown("""
    This web app matches your resume with available job postings using **TF-IDF and cosine similarity**.
    Upload your resume and get personalized job recommendations!
    """)
    
    # File uploader
    uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["txt", "pdf"])
    
    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")
        st.info(f"File size: {uploaded_file.size} bytes")
        
        resume_text = parse_resume(uploaded_file)
        
        if resume_text and not resume_text.startswith("Error"):
            processed_resume = clean_text(resume_text)
            
            with st.expander("View Extracted Resume Text"):
                st.text(resume_text[:2000] + "..." if len(resume_text) > 2000 else resume_text)
            
            job_df = get_job_df()
            
            st.markdown("---")
            display_keywords(processed_resume, job_df)
            
            st.markdown("---")
            recommendations = recommend_jobs(processed_resume, job_df, NUM_POSTING)
            download_buttons(recommendations)
            
            st.markdown("---")
            st.markdown(f"### Recommended Jobs Based on Your Resume")
            st.markdown(f"Found **{len(recommendations)}** matching jobs")
            
            display_df = format_table(recommendations)
            st.write(display_df.to_html(escape=False), unsafe_allow_html=True)
        else:
            st.error("Could not read the file. Please try another format.")
    else:
        st.markdown("---")
        st.markdown("### Available Job Postings")
        job_df = get_job_df()
        display_df = format_table(job_df)
        st.write(display_df.to_html(escape=False), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
