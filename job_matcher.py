"""
job_matcher.py
Compares resume text against job-role requirements using TF-IDF
vectors and cosine similarity, then ranks roles by match score.
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_job_roles(csv_path="data/job_roles.csv"):
    """Loads job roles with columns: job_role, required_skills (comma-separated)."""
    df = pd.read_csv(csv_path)
    return df


def match_roles(cleaned_resume_text: str, job_roles_df: pd.DataFrame) -> list:
    """
    Vectorizes the resume and each job role's skill list with TF-IDF,
    computes cosine similarity, and returns a list of
    (job_role, score_percent) sorted from highest to lowest.
    """
    # Build a "document" per job role: its comma-separated skills as plain text
    role_docs = job_roles_df["required_skills"].str.replace(",", " ").tolist()
    role_names = job_roles_df["job_role"].tolist()

    # The resume text is the last document in the corpus
    corpus = role_docs + [cleaned_resume_text]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    resume_vector = tfidf_matrix[-1]
    role_vectors = tfidf_matrix[:-1]

    similarities = cosine_similarity(resume_vector, role_vectors)[0]

    results = list(zip(role_names, similarities))
    results.sort(key=lambda x: x[1], reverse=True)

    # Convert similarity (0-1) to a friendlier percentage
    results = [(role, round(score * 100, 1)) for role, score in results]
    return results


def top_n_roles(results: list, n: int = 3) -> list:
    """Returns the top N (role, score) tuples."""
    return results[:n]


if __name__ == "__main__":
    from text_cleaner import clean_text

    sample_resume = "Experienced in Python, Pandas, scikit-learn, Machine Learning, SQL."
    cleaned = clean_text(sample_resume)

    jobs_df = load_job_roles()
    ranked = match_roles(cleaned, jobs_df)

    print("Ranked roles:")
    for role, score in ranked:
        print(f"  {role}: {score}%")

    print("\nTop 3:", top_n_roles(ranked, 3))