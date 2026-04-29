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

    # Final weighted score
    final_score = round(
        (0.5 * skill_score + 0.25 * major_score + 0.25 * location_score) * 100,
        2,
    )

    explanation = (
        f"Skill match: {len(matched)}/{len(job_skills)}. "
        f"Matched: {', '.join(sorted(matched)) if matched else 'None'}. "
        f"Missing: {', '.join(sorted(missing)) if missing else 'None'}. "
        f"Major relevance: {major_score}. "
        f"Location relevance: {location_score}."
    )

    return final_score, explanation