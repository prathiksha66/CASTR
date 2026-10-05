from database import db


def calculate_match_score(actor, role):
    """
    Calculates actor-role compatibility using weighted
    language, skill and experience scores.
    """

    score = 0
    total_weight = 0
    breakdown = []

    # ------------------------------
    # 1. LANGUAGE SCORE
    # ------------------------------
    for requirement in role.get("required_languages", []):

        weight = requirement["weight"]
        total_weight += weight

        actor_language = next(
            (
                language
                for language in actor.get("languages", [])
                if language["name"].lower()
                == requirement["name"].lower()
            ),
            None
        )

        if actor_language:

            actual_level = actor_language["proficiency"]

            # Ratings are out of 5
            language_score = (actual_level / 5) * weight

            score += language_score

            breakdown.append({
                "category": requirement["name"] + " Language",
                "matched":
                    actual_level >= requirement["minimum_proficiency"],
                "score": round(language_score, 2),
                "weight": weight
            })

        else:

            breakdown.append({
                "category": requirement["name"] + " Language",
                "matched": False,
                "score": 0,
                "weight": weight
            })

    # ------------------------------
    # 2. SKILL SCORE
    # ------------------------------
    for requirement in role.get("required_skills", []):

        weight = requirement["weight"]
        total_weight += weight

        actor_skill = next(
            (
                skill
                for skill in actor.get("skills", [])
                if skill["name"].lower()
                == requirement["name"].lower()
            ),
            None
        )

        if actor_skill:

            actual_level = actor_skill["level"]

            skill_score = (actual_level / 5) * weight

            score += skill_score

            breakdown.append({
                "category": requirement["name"],
                "matched":
                    actual_level >= requirement["minimum_level"],
                "score": round(skill_score, 2),
                "weight": weight
            })

        else:

            breakdown.append({
                "category": requirement["name"],
                "matched": False,
                "score": 0,
                "weight": weight
            })

    # ------------------------------
    # 3. EXPERIENCE SCORE
    # ------------------------------
    experience_weight = role.get(
        "experience_weight",
        0
    )

    total_weight += experience_weight

    minimum_experience = role.get(
        "minimum_experience",
        0
    )

    actor_experience = actor.get(
        "experience_years",
        0
    )

    # Give higher experienced actors slightly better scores
    target_experience = minimum_experience + 3

    if target_experience > 0:

        experience_score = min(
            actor_experience / target_experience,
            1
        ) * experience_weight

    else:
        experience_score = experience_weight

    score += experience_score

    breakdown.append({
        "category": "Experience",
        "matched":
            actor_experience >= minimum_experience,
        "score": round(experience_score, 2),
        "weight": experience_weight
    })

    # ------------------------------
    # FINAL PERCENTAGE
    # ------------------------------
    if total_weight > 0:

        percentage = (
            score / total_weight
        ) * 100

    else:
        percentage = 0

    return round(percentage, 2), breakdown


def get_ranked_candidates(role):

    from database import db

    actors = list(db.actors.find())

    ranked_candidates = []

    for actor in actors:

        # -----------------------------
        # BASIC ELIGIBILITY FILTERING
        # -----------------------------

        # Age
        if actor.get("age", 0) < role.get("age_min", 0):
            continue

        if actor.get("age", 0) > role.get("age_max", 100):
            continue

        # Gender
        role_gender = role.get("gender")

        if role_gender and role_gender.lower() != "any":

            if actor.get("gender", "").lower() != role_gender.lower():
                continue

        # Location
        role_location = role.get("location")

        if role_location:

            if actor.get("location", "").lower() != role_location.lower():
                continue

        # Availability
        if not actor.get("available", False):
            continue

        # -----------------------------
        # CALCULATE MATCH SCORE
        # -----------------------------

        score, breakdown = calculate_match_score(
            actor,
            role
        )

        ranked_candidates.append({

            "_id": actor["_id"],

            "name": actor["name"],

            "age": actor.get("age"),

            "gender": actor.get("gender"),

            "location": actor.get("location"),

            "experience_years":
                actor.get("experience_years", 0),

            "score": score,

            "breakdown": breakdown
        })

    # Highest score first
    ranked_candidates.sort(
        key=lambda candidate: candidate["score"],
        reverse=True
    )

    return ranked_candidates