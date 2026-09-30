from src.matcher import SKILLS


def recruiter_query(query, candidate_results):

    query = query.lower()

    # Find skills mentioned in the recruiter's question
    requested_skills = []

    for skill in SKILLS:

        if skill.lower() in query:

            requested_skills.append(
                skill
            )

    # If no skill was detected
    if not requested_skills:

        return []


    matching_candidates = []

    for candidate in candidate_results:

        matched_skills = candidate[
            "Matched Skills"
        ].lower()

        # Check whether candidate has
        # all requested skills
        has_all_skills = True

        for skill in requested_skills:

            if skill.lower() not in matched_skills:

                has_all_skills = False

                break

        if has_all_skills:

            matching_candidates.append(
                candidate["Candidate"]
            )


    return matching_candidates