from flask import Flask, render_template, redirect, url_for, request
from database import db
from matching import get_ranked_candidates
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "castr-secret-key"


# -----------------------------
# HOME
# -----------------------------
@app.route("/")
def home():

    actor_count = db.actors.count_documents({})
    role_count = db.roles.count_documents({})
    production_count = db.productions.count_documents({})

    return render_template(
        "index.html",
        actor_count=actor_count,
        role_count=role_count,
        production_count=production_count
    )


# -----------------------------
# ACTORS
# -----------------------------
@app.route("/actors")
def actor_list():

    actors = list(db.actors.find())

    return render_template(
        "actors.html",
        actors=actors
    )


# -----------------------------
# ROLES
# -----------------------------
@app.route("/roles")
def role_list():

    roles = list(db.roles.find())

    for role in roles:

        production = db.productions.find_one({
            "_id": role["production_id"]
        })

        role["production_name"] = (
            production["title"]
            if production
            else "Unknown Production"
        )

    return render_template(
        "roles.html",
        roles=roles
    )


# -----------------------------
# MATCHING
# -----------------------------
@app.route("/matches/<role_id>")
def matches(role_id):

    role = db.roles.find_one({
        "_id": ObjectId(role_id)
    })

    if not role:
        return "Role not found", 404

    production = db.productions.find_one({
        "_id": role["production_id"]
    })

    candidates = get_ranked_candidates(role)

    return render_template(
        "matches.html",
        role=role,
        production=production,
        candidates=candidates
    )

# -----------------------------
# CREATE APPLICATION
# -----------------------------
@app.route("/apply/<role_id>/<actor_id>", methods=["POST"])
def apply(role_id, actor_id):

    role = db.roles.find_one({
        "_id": ObjectId(role_id)
    })

    actor = db.actors.find_one({
        "_id": ObjectId(actor_id)
    })

    if not role or not actor:
        return "Actor or role not found", 404

    # Prevent duplicate applications
    existing = db.applications.find_one({
        "role_id": role["_id"],
        "actor_id": actor["_id"]
    })

    if existing:
        return redirect(
            url_for(
                "matches",
                role_id=role_id
            )
        )

    # Get calculated match score
    candidates = get_ranked_candidates(role)

    match_score = 0

    for candidate in candidates:

        if candidate["_id"] == actor["_id"]:
            match_score = candidate["score"]
            break

    application = {
        "actor_id": actor["_id"],
        "role_id": role["_id"],
        "production_id": role["production_id"],
        "match_score": match_score,
        "status": "Applied"
    }

    db.applications.insert_one(application)

    return redirect(url_for("applications"))


# -----------------------------
# VIEW APPLICATIONS
# -----------------------------
@app.route("/applications")
def applications():

    application_list = list(
        db.applications.find()
    )

    for application in application_list:

        actor = db.actors.find_one({
            "_id": application["actor_id"]
        })

        role = db.roles.find_one({
            "_id": application["role_id"]
        })

        production = db.productions.find_one({
            "_id": application["production_id"]
        })

        application["actor_name"] = (
            actor["name"]
            if actor
            else "Unknown Actor"
        )

        application["role_name"] = (
            role["role_name"]
            if role
            else "Unknown Role"
        )

        application["production_name"] = (
            production["title"]
            if production
            else "Unknown Production"
        )

    return render_template(
        "applications.html",
        applications=application_list
    )


# -----------------------------
# UPDATE APPLICATION STATUS
# -----------------------------
@app.route(
    "/application/<application_id>/status",
    methods=["POST"]
)
def update_application_status(application_id):

    from flask import request

    status = request.form.get("status")

    allowed_statuses = [
        "Applied",
        "Shortlisted",
        "Rejected"
    ]

    if status not in allowed_statuses:
        return "Invalid status", 400

    db.applications.update_one(
        {
            "_id": ObjectId(application_id)
        },
        {
            "$set": {
                "status": status
            }
        }
    )

    return redirect(url_for("applications"))

# -----------------------------
# SCHEDULE AUDITION
# -----------------------------
@app.route("/schedule-audition/<application_id>", methods=["POST"])
def schedule_audition(application_id):

    application = db.applications.find_one({
        "_id": ObjectId(application_id)
    })

    if not application:
        return "Application not found", 404

    # Prevent duplicate audition
    existing = db.auditions.find_one({
        "application_id": application["_id"]
    })

    if not existing:

        audition = {
            "application_id": application["_id"],
            "actor_id": application["actor_id"],
            "role_id": application["role_id"],
            "production_id": application["production_id"],
            "date": "2026-10-06",
            "time": "10:00 AM",
            "venue": "CASTR Studio - Chennai",
            "round": "Round 1",
            "status": "Scheduled"
        }

        db.auditions.insert_one(audition)

        db.applications.update_one(
            {"_id": application["_id"]},
            {"$set": {"status": "Audition Scheduled"}}
        )

    return redirect(url_for("auditions"))


# -----------------------------
# VIEW AUDITIONS
# -----------------------------
@app.route("/auditions")
def auditions():

    audition_list = list(db.auditions.find())

    for audition in audition_list:

        actor = db.actors.find_one({
            "_id": audition["actor_id"]
        })

        role = db.roles.find_one({
            "_id": audition["role_id"]
        })

        production = db.productions.find_one({
            "_id": audition["production_id"]
        })

        audition["actor_name"] = (
            actor["name"] if actor else "Unknown Actor"
        )

        audition["role_name"] = (
            role["role_name"] if role else "Unknown Role"
        )

        audition["production_name"] = (
            production["title"]
            if production else "Unknown Production"
        )

    return render_template(
        "auditions.html",
        auditions=audition_list
    )

# -----------------------------
# EVALUATIONS PAGE
# -----------------------------
@app.route("/evaluations")
def evaluations():

    audition_list = list(db.auditions.find())

    for audition in audition_list:

        actor = db.actors.find_one({
            "_id": audition["actor_id"]
        })

        role = db.roles.find_one({
            "_id": audition["role_id"]
        })

        production = db.productions.find_one({
            "_id": audition["production_id"]
        })

        evaluation = db.evaluations.find_one({
            "audition_id": audition["_id"]
        })

        audition["actor_name"] = (
            actor["name"] if actor else "Unknown"
        )

        audition["role_name"] = (
            role["role_name"] if role else "Unknown"
        )

        audition["production_name"] = (
            production["title"]
            if production else "Unknown"
        )

        audition["evaluation"] = evaluation

    return render_template(
        "evaluations.html",
        auditions=audition_list
    )


# -----------------------------
# SUBMIT EVALUATION
# -----------------------------
@app.route("/evaluate/<audition_id>", methods=["POST"])
def evaluate(audition_id):

    audition = db.auditions.find_one({
        "_id": ObjectId(audition_id)
    })

    if not audition:
        return "Audition not found", 404

    acting = int(request.form["acting"])
    expression = int(request.form["expression"])
    dialogue = int(request.form["dialogue"])
    confidence = int(request.form["confidence"])

    total = acting + expression + dialogue + confidence

    # 28/40 = 70%
    if total >= 28:
        decision = "Selected"
    else:
        decision = "Rejected"

    evaluation = {
        "audition_id": audition["_id"],
        "actor_id": audition["actor_id"],
        "role_id": audition["role_id"],
        "production_id": audition["production_id"],
        "acting": acting,
        "expression": expression,
        "dialogue": dialogue,
        "confidence": confidence,
        "total": total,
        "decision": decision
    }

    # Prevent duplicate evaluations
    db.evaluations.update_one(
        {"audition_id": audition["_id"]},
        {"$set": evaluation},
        upsert=True
    )

    db.auditions.update_one(
        {"_id": audition["_id"]},
        {"$set": {"status": "Evaluated"}}
    )

    db.applications.update_one(
        {"actor_id": audition["actor_id"],
         "role_id": audition["role_id"]},
        {"$set": {"status": decision}}
    )

    return redirect(url_for("evaluations"))

# -----------------------------
# ANALYTICS DASHBOARD
# -----------------------------
@app.route("/analytics")
def analytics():

    # Basic database statistics
    total_actors = db.actors.count_documents({})
    total_roles = db.roles.count_documents({})
    total_productions = db.productions.count_documents({})
    total_applications = db.applications.count_documents({})
    total_auditions = db.auditions.count_documents({})
    total_evaluations = db.evaluations.count_documents({})

    # MongoDB Aggregation Pipeline:
    # Group applications according to their status
    status_pipeline = [
        {
            "$group": {
                "_id": "$status",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "count": -1
            }
        }
    ]

    status_results = list(
        db.applications.aggregate(status_pipeline)
    )

    # Average match score using MongoDB aggregation
    score_pipeline = [
        {
            "$group": {
                "_id": None,
                "average_score": {"$avg": "$match_score"},
                "highest_score": {"$max": "$match_score"},
                "lowest_score": {"$min": "$match_score"}
            }
        }
    ]

    score_results = list(
        db.applications.aggregate(score_pipeline)
    )

    if score_results:
        average_score = round(
            score_results[0].get("average_score", 0), 1
        )
        highest_score = score_results[0].get(
            "highest_score", 0
        )
        lowest_score = score_results[0].get(
            "lowest_score", 0
        )
    else:
        average_score = 0
        highest_score = 0
        lowest_score = 0

    return render_template(
        "analytics.html",
        total_actors=total_actors,
        total_roles=total_roles,
        total_productions=total_productions,
        total_applications=total_applications,
        total_auditions=total_auditions,
        total_evaluations=total_evaluations,
        status_results=status_results,
        average_score=average_score,
        highest_score=highest_score,
        lowest_score=lowest_score
    )

if __name__ == "__main__":
    app.run(debug=True)