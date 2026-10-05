from database import db

# -----------------------------
# CLEAR OLD DEMO DATA
# -----------------------------
db.actors.delete_many({})
db.productions.delete_many({})
db.roles.delete_many({})
db.applications.delete_many({})
db.auditions.delete_many({})
db.evaluations.delete_many({})


# -----------------------------
# ACTORS
# -----------------------------
actors = [
    {
        "name": "Ananya Rao",
        "age": 23,
        "gender": "Female",
        "location": "Chennai",
        "experience_years": 4,
        "languages": [
            {"name": "Tamil", "proficiency": 5},
            {"name": "English", "proficiency": 4}
        ],
        "skills": [
            {"name": "Emotional Acting", "level": 5},
            {"name": "Comedy", "level": 4},
            {"name": "Dance", "level": 4}
        ],
        "previous_roles": [
            {
                "production": "The Last Train",
                "character": "Meera",
                "year": 2025
            }
        ],
        "available": True
    },

    {
        "name": "Meera Kumar",
        "age": 24,
        "gender": "Female",
        "location": "Chennai",
        "experience_years": 3,
        "languages": [
            {"name": "Tamil", "proficiency": 5},
            {"name": "English", "proficiency": 5},
            {"name": "Hindi", "proficiency": 3}
        ],
        "skills": [
            {"name": "Emotional Acting", "level": 4},
            {"name": "Comedy", "level": 5},
            {"name": "Dance", "level": 3}
        ],
        "previous_roles": [
            {
                "production": "College Days",
                "character": "Nila",
                "year": 2024
            }
        ],
        "available": True
    },

    {
        "name": "Divya Nair",
        "age": 22,
        "gender": "Female",
        "location": "Chennai",
        "experience_years": 2,
        "languages": [
            {"name": "Tamil", "proficiency": 4},
            {"name": "Malayalam", "proficiency": 5},
            {"name": "English", "proficiency": 4}
        ],
        "skills": [
            {"name": "Emotional Acting", "level": 5},
            {"name": "Dance", "level": 5},
            {"name": "Improvisation", "level": 4}
        ],
        "previous_roles": [],
        "available": True
    },

    {
        "name": "Arjun Krishnan",
        "age": 27,
        "gender": "Male",
        "location": "Chennai",
        "experience_years": 5,
        "languages": [
            {"name": "Tamil", "proficiency": 5},
            {"name": "English", "proficiency": 4}
        ],
        "skills": [
            {"name": "Action", "level": 5},
            {"name": "Emotional Acting", "level": 4},
            {"name": "Improvisation", "level": 4}
        ],
        "previous_roles": [
            {
                "production": "City Shadows",
                "character": "Karthik",
                "year": 2025
            }
        ],
        "available": True
    },

    {
        "name": "Rahul Menon",
        "age": 29,
        "gender": "Male",
        "location": "Bengaluru",
        "experience_years": 6,
        "languages": [
            {"name": "Tamil", "proficiency": 3},
            {"name": "English", "proficiency": 5},
            {"name": "Malayalam", "proficiency": 5}
        ],
        "skills": [
            {"name": "Comedy", "level": 5},
            {"name": "Improvisation", "level": 5},
            {"name": "Emotional Acting", "level": 3}
        ],
        "previous_roles": [
            {
                "production": "Weekend Stories",
                "character": "Vijay",
                "year": 2024
            }
        ],
        "available": True
    }
]


actor_result = db.actors.insert_many(actors)

print(f"{len(actor_result.inserted_ids)} actors inserted.")


# -----------------------------
# PRODUCTIONS
# -----------------------------
productions = [
    {
        "title": "Echoes of Chennai",
        "type": "Film",
        "director": "Karthik Raman",
        "location": "Chennai",
        "status": "Casting"
    },

    {
        "title": "Midnight Stories",
        "type": "Web Series",
        "director": "Priya Menon",
        "location": "Chennai",
        "status": "Casting"
    }
]

production_result = db.productions.insert_many(productions)

print(f"{len(production_result.inserted_ids)} productions inserted.")


# -----------------------------
# ROLES
# -----------------------------
roles = [
    {
        "production_id": production_result.inserted_ids[0],
        "role_name": "Priya",
        "description": "Young journalist investigating a mysterious story.",
        "gender": "Female",
        "age_min": 20,
        "age_max": 27,
        "location": "Chennai",
        "minimum_experience": 2,

        "required_languages": [
            {
                "name": "Tamil",
                "minimum_proficiency": 4,
                "weight": 20
            }
        ],

        "required_skills": [
            {
                "name": "Emotional Acting",
                "minimum_level": 3,
                "weight": 30
            },
            {
                "name": "Comedy",
                "minimum_level": 2,
                "weight": 20
            },
            {
                "name": "Dance",
                "minimum_level": 2,
                "weight": 15
            }
        ],

        "experience_weight": 15,
        "status": "Open"
    },

    {
        "production_id": production_result.inserted_ids[1],
        "role_name": "Vikram",
        "description": "Confident detective with strong screen presence.",
        "gender": "Male",
        "age_min": 25,
        "age_max": 32,
        "location": "Chennai",
        "minimum_experience": 3,

        "required_languages": [
            {
                "name": "Tamil",
                "minimum_proficiency": 4,
                "weight": 20
            }
        ],

        "required_skills": [
            {
                "name": "Action",
                "minimum_level": 3,
                "weight": 35
            },
            {
                "name": "Emotional Acting",
                "minimum_level": 3,
                "weight": 25
            }
        ],

        "experience_weight": 20,
        "status": "Open"
    }
]

role_result = db.roles.insert_many(roles)

print(f"{len(role_result.inserted_ids)} roles inserted.")

print("\nCASTR database seeded successfully!")