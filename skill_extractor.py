"""
skill_extractor.py
Identifies technical skills present in cleaned resume text by matching
against a controlled skill dictionary (data/skill_dictionary.csv).
"""

import pandas as pd


def load_skill_dictionary(csv_path="data/skill_dictionary.csv"):
    """Loads the skill dictionary as a DataFrame with columns: skill, category."""
    df = pd.read_csv(csv_path)
    df["skill"] = df["skill"].str.lower().str.strip()
    return df


def extract_skills(cleaned_text: str, skill_df: pd.DataFrame) -> dict:
    """
    Searches cleaned_text for each skill in the dictionary.
    Returns a dict grouped by category:
        {"Programming": ["python", "java"], "Databases": ["sql"], ...}
    """
    found_by_category = {}

    for _, row in skill_df.iterrows():
        skill = row["skill"]
        category = row["category"]

        # Simple substring/keyword match.
        # Handles multi-word skills like "power bi" and symbol skills like "c++".
        if skill in cleaned_text:
            found_by_category.setdefault(category, [])
            if skill not in found_by_category[category]:
                found_by_category[category].append(skill)

    return found_by_category


def flatten_skills(found_by_category: dict) -> set:
    """Flattens the category dict into a single set of skill names."""
    all_skills = set()
    for skills in found_by_category.values():
        all_skills.update(skills)
    return all_skills


if __name__ == "__main__":
    from text_cleaner import clean_text

    sample = "Skilled in Python, Pandas, SQL, and basic Machine Learning with scikit-learn."
    cleaned = clean_text(sample)
    skills_df = load_skill_dictionary()
    result = extract_skills(cleaned, skills_df)
    print(result)