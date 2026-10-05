from database import db
from matching import get_ranked_candidates


role = db.roles.find_one({
    "role_name": "Priya"
})


if role:

    print("\n")
    print("=" * 55)
    print("CASTR - ACTOR ROLE MATCHING")
    print("=" * 55)

    print("\nROLE:", role["role_name"])

    candidates = get_ranked_candidates(role)

    print("\nRANKED CANDIDATES")
    print("-" * 55)

    for rank, candidate in enumerate(candidates, start=1):

        print(
            f"{rank}. {candidate['name']} "
            f"- {candidate['score']}%"
        )

        for item in candidate["breakdown"]:

            status = "MATCH" if item["matched"] else "PARTIAL / NO MATCH"

            print(
                f"   {item['category']}: "
                f"{item['score']}/{item['weight']} "
                f"[{status}]"
            )

        print()

else:
    print("Role not found.")
    