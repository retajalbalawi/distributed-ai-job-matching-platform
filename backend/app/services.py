def normalize_skills(skills: str) -> set[str]:
    return {
        skill.strip().lower()
        for skill in skills.split(",")
        if skill.strip()
    }


def calculate_match_score(user_skills: str, job_skills: str) -> tuple[float, str]:
    user_set = normalize_skills(user_skills)
    job_set = normalize_skills(job_skills)

    if not job_set:
        return 0.0, "No required skills listed for this job."

    matched = user_set.intersection(job_set)
    missing = job_set.difference(user_set)

    score = round((len(matched) / len(job_set)) * 100, 2)

    explanation = (
        f"Matched skills: {', '.join(sorted(matched)) if matched else 'None'}. "
        f"Missing skills: {', '.join(sorted(missing)) if missing else 'None'}."
    )

    return score, explanation