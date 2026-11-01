# Internship-Job-Recommendation-System

A machine learning-powered job recommendation system that matches resumes with job postings using Natural Language Processing (NLP) techniques.

[![GitHub](https://img.shields.io/badge/GitHub-Sneh5824-blue)](https://github.com/Sneh5824/Intership-Job-Recommendation-System-)

## Table of Contents
1. [Overview](#overview)
2. [How It Works](#how-it-works)
3. [Project Structure](#project-structure)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Technical Details](#technical-details)
7. [Algorithm Explanation](#algorithm-explanation)

---

## Overview

This project is an **AI-powered job recommendation system** that analyzes a user's resume and matches it with available job postings. It uses **TF-IDF (Term Frequency-Inverse Document Frequency)** and **Cosine Similarity** to find the most relevant jobs based on the skills and experience mentioned in the resume.

### Key Features
- Upload resume in PDF, TXT, or DOCX format
- Extract keywords from resume automatically
- Match resume with job postings using NLP
- Display match percentage for each job
- Download recommendations as CSV or Excel
- Dark-themed user interface

---

## How It Works

### Step-by-Step Process

```
┌─────────────────┐
│  Upload Resume  │
│  (PDF/TXT/DOCX) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Extract Text   │
│  from Resume    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Preprocess     │
│  Clean Text     │
│  Remove Noise   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  TF-IDF         │
│  Vectorization  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Cosine         │
│  Similarity     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Rank Jobs by   │
│  Match Score    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Display        │
│  Recommendations│
└─────────────────┘
```

### Detailed Explanation

1. **Resume Upload**: User uploads their resume file (PDF, TXT, or DOCX)

2. **Text Extraction**: The system reads the file and extracts all text content
   - PDF: Uses PyPDF2 library
   - DOCX: Uses python-docx library
   - TXT: Direct text reading

3. **Text Preprocessing**: Clean the extracted text
   - Remove special characters (keep only letters)
   - Convert to lowercase
   - Remove stop words (common words like "the", "is", "at")

4. **TF-IDF Vectorization**: Convert text to numerical vectors
   - Calculate term frequency (how often a word appears)
   - Calculate inverse document frequency (how unique the word is)
   - Create a vector representation of the resume

5. **Cosine Similarity**: Compare resume vector with job vectors
   - Calculate angle between vectors
   - Score ranges from 0 (no match) to 1 (perfect match)

6. **Ranking**: Sort jobs by similarity score and display top matches

---

## Project Structure

```
job_recommendation_system/
│
├── streamlit_app.py      # Main web application
├── model.py              # Recommendation algorithm
├── preprocess.py         # Text cleaning functions
├── file_parser.py        # Resume file reading
├── requirements.txt      # Python dependencies
├── style.css             # CSS styling
├── README.md             # This documentation
│
└── data/
    ├── job_posting.csv   # Job listings database
    └── testing_*.pdf     # Sample resume files for testing
```

### File Descriptions

| File | Purpose |
|------|---------|
| `streamlit_app.py` | Main application with UI, handles user interaction |
| `model.py` | Contains TF-IDF and cosine similarity logic |
| `preprocess.py` | Text cleaning and preprocessing functions |
| `file_parser.py` | Reads PDF, DOCX, and TXT files |
| `job_posting.csv` | Database of job postings with Role, Location, etc. |

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project
```bash
cd d:\SAP\TEST\job_recommendation_system
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Verify Installation
```bash
python -c "import streamlit; import pandas; import sklearn; print('All packages installed!')"
```

---

## Usage

### Running the Application
```bash
streamlit run streamlit_app.py
```

This will open the application in your default web browser at `http://localhost:8501`

### Using the Application

1. **Open the web app** in your browser
2. **Upload your resume** (PDF, TXT, or DOCX format)
3. **View extracted keywords** from your resume
4. **See job recommendations** ranked by match percentage
5. **Download results** as CSV or Excel file
6. **Click "Apply Link"** to apply for jobs

---

## Technical Details

### Libraries Used

| Library | Version | Purpose |
|---------|---------|---------|
| `streamlit` | Latest | Web application framework |
| `pandas` | Latest | Data manipulation |
| `numpy` | Latest | Numerical operations |
| `scikit-learn` | Latest | TF-IDF and cosine similarity |
| `PyPDF2` | Latest | PDF text extraction |
| `python-docx` | Latest | DOCX text extraction |
| `openpyxl` | Latest | Excel file creation |

### Data Format

The `job_posting.csv` file should have these columns:
```
Company,Role,Location,Application/Link,Date Posted
Google,Software Engineer Intern,Mountain View CA,https://careers.google.com,Jan 03
Amazon,Data Science Intern,Seattle WA,https://amazon.jobs,Jan 05
...
```

---

## Algorithm Explanation

### TF-IDF (Term Frequency-Inverse Document Frequency)

TF-IDF is a numerical statistic that reflects how important a word is to a document.

#### Formula:
```
TF-IDF(t, d) = TF(t, d) × IDF(t)

Where:
- TF(t, d) = (Number of times term t appears in document d) / (Total terms in d)
- IDF(t) = log(Total documents / Documents containing term t)
```

#### Example:
```
Resume: "Python machine learning data science"
Job 1:  "Python developer backend"
Job 2:  "Machine learning engineer Python"

TF-IDF gives higher weight to:
- "machine learning" (specific technical skill)
- "data science" (domain expertise)

Lower weight to:
- "Python" (appears in many jobs, less unique)
```

### Cosine Similarity

Measures the angle between two vectors, regardless of their magnitude.

#### Formula:
```
Cosine Similarity = (A · B) / (||A|| × ||B||)

Where:
- A · B = dot product of vectors A and B
- ||A|| = magnitude of vector A
- ||B|| = magnitude of vector B
```

#### Visual Representation:
```
        Job Vector
           ↗
          /
         /  θ (angle)
        /
       /
      ────────────→ Resume Vector

Cosine Similarity = cos(θ)
- θ = 0°  → Similarity = 1.0 (Perfect match)
- θ = 90° → Similarity = 0.0 (No match)
```

### Complete Workflow Example

```python
# 1. Resume Text (after preprocessing)
resume = "python machine learning data analysis sql"

# 2. Job Texts (after preprocessing)
jobs = [
    "python developer backend api",           # Job 1
    "machine learning engineer python data",  # Job 2
    "frontend developer javascript react"     # Job 3
]

# 3. TF-IDF Vectorization
# Creates numerical vectors for each text
# Resume Vector: [0.4, 0.5, 0.3, 0.0, 0.0, ...]
# Job 1 Vector:  [0.6, 0.0, 0.0, 0.4, 0.0, ...]
# Job 2 Vector:  [0.3, 0.5, 0.4, 0.0, 0.0, ...]
# Job 3 Vector:  [0.0, 0.0, 0.0, 0.0, 0.7, ...]

# 4. Cosine Similarity Calculation
# Resume vs Job 1: 0.35 (35% match)
# Resume vs Job 2: 0.85 (85% match) ← Best match!
# Resume vs Job 3: 0.05 (5% match)

# 5. Result: Job 2 is recommended first
```

---

## Code Examples

### Text Preprocessing
```python
# preprocess.py
def clean_text(text):
    # Input: "Hello! I am a Python Developer."
    
    # Step 1: Keep only letters
    text = "Hello I am a Python Developer"
    
    # Step 2: Convert to lowercase
    text = "hello i am a python developer"
    
    # Step 3: Remove stop words
    text = "python developer"
    
    return text
```

### TF-IDF and Similarity
```python
# model.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_jobs(resume_text, job_df):
    # Combine all texts
    all_text = list(job_df['data']) + [resume_text]
    
    # Create TF-IDF vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_text)
    
    # Calculate similarity
    resume_vector = tfidf_matrix[-1]
    job_vectors = tfidf_matrix[:-1]
    
    similarities = cosine_similarity(resume_vector, job_vectors)
    
    # Sort by similarity
    top_jobs = similarities.argsort()[::-1]
    
    return top_jobs
```

---

## Troubleshooting

### Common Issues

1. **"No module named 'streamlit'"**
   ```bash
   pip install streamlit
   ```

2. **"Job data not found"**
   - Ensure `job_posting.csv` exists in the `data/` folder
   - Check the file has correct column names

3. **"Error reading PDF"**
   - Install PyPDF2: `pip install PyPDF2`
   - Try a different PDF file

4. **Application not loading**
   - Check if port 8501 is available
   - Try: `streamlit run streamlit_app.py --server.port 8502`

---

## Future Improvements

- [ ] Add more job data sources
- [ ] Implement skill extraction using NER
- [ ] Add user profiles and saved searches
- [ ] Include salary predictions
- [ ] Add resume improvement suggestions

---

## Author

Job Recommendation System Project

## License

This project is for educational purposes.
#   J o b - R e c o m m e n d a t i o n - S y s t e m  
 