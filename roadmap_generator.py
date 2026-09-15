"""
roadmap_generator.py
Generates a simple, rule-based weekly learning roadmap based on
the skills missing for a target role.
"""

# A small library of learning suggestions per skill.
# Falls back to a generic suggestion if a skill isn't listed here.
SKILL_LEARNING_TIPS = {
    "docker": "Learn Docker fundamentals: images, containers, and Dockerfiles.",
    "fastapi": "Build a small REST API with FastAPI and connect it to a model.",
    "mlflow": "Learn MLflow for experiment tracking and model versioning.",
    "cloud deployment": "Deploy a small project on Streamlit Cloud or Render.",
    "sql": "Practice SQL joins, aggregations, and subqueries on a sample database.",
    "power bi": "Build a dashboard in Power BI using a public dataset.",
    "tableau": "Create a visualization dashboard in Tableau Public.",
    "pytorch": "Complete a beginner PyTorch tutorial and train a small model.",
    "tensorflow": "Complete a beginner TensorFlow/Keras image classification tutorial.",
    "nlp": "Learn basic NLP concepts: tokenization, stemming, and embeddings.",
    "transformers": "Explore the Hugging Face Transformers library with a pretrained model.",
    "opencv": "Practice basic image processing tasks (resize, filter, edge detection) with OpenCV.",
    "react": "Build a small component-based UI with React.",
    "node.js": "Build a simple REST API backend using Node.js and Express.",
    "git": "Practice branching, merging, and pull requests on a personal GitHub repo.",
    "javascript": "Learn JS fundamentals: variables, functions, DOM manipulation, and fetch API.",
    "rest api": "Build and consume a simple REST API using any backend framework.",
}

DEFAULT_TIP = "Study the fundamentals of this skill and build one small hands-on project with it."


def generate_roadmap(missing_skills: list) -> list:
    """
    Takes a list of missing skill names and returns a week-by-week
    roadmap as a list of strings, e.g.:
        ["Week 1: Docker - Learn Docker fundamentals...", ...]
    """
    roadmap = []
    for i, skill in enumerate(missing_skills, start=1):
        tip = SKILL_LEARNING_TIPS.get(skill.lower(), DEFAULT_TIP)
        roadmap.append(f"Week {i}: {skill.title()} — {tip}")
    return roadmap


if __name__ == "__main__":
    missing = ["FastAPI", "Docker", "MLflow", "Cloud Deployment"]
    for line in generate_roadmap(missing):
        print(line)