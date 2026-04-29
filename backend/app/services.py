
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_similarity(text1, text2):
    vec1 = model.encode(text1)
    vec2 = model.encode(text2)

    score = cosine_similarity([vec1], [vec2])[0][0]
    return float(score)

def normalize_skills(skills: str) -> set[str]:
    return {
        skill.strip().lower()
        for skill in skills.split(",")
        if skill.strip()
    }


def calculate_match_score(user, job):
    user_skills = normalize_skills(user.skills)
    job_skills = normalize_skills(job.required_skills)

    # Skill match
    matched = user_skills.intersection(job_skills)
    missing = job_skills.difference(user_skills)

    skill_score = len(matched) / len(job_skills) if job_skills else 0

    # Major match (simple logic)
    major_score = 1 if user.major.lower() in job.description.lower() else 0.5

    # Location match
    location_score = 1 if user.major.lower() in job.location.lower() else 0.5
    
    #semantic score
    semantic_score = semantic_similarity(user.skills, job.required_skills)

    # Final weighted score
    final_score = round(
    (0.4 * skill_score + 0.2 * major_score + 0.2 * location_score + 0.2 * semantic_score) * 100,
    2,
)

    explanation = (
        f"Skill match: {len(matched)}/{len(job_skills)}. "
        f"Matched: {', '.join(sorted(matched)) if matched else 'None'}. "
        f"Missing: {', '.join(sorted(missing)) if missing else 'None'}. "
        f"Major relevance: {major_score}. "
        f"Location relevance: {location_score}."
        f"Semantic similarity: {round(semantic_score,2)}"
    )

    return final_score, explanation