from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import sqlite3
from datetime import datetime


app = Flask(__name__)

DATABASE = "Findora.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def initialize_database():

    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            category TEXT NOT NULL,
            color TEXT NOT NULL,
            description TEXT NOT NULL,
            location_type TEXT NOT NULL,
            location_details TEXT NOT NULL,
            date_lost TEXT NOT NULL,
            time_lost TEXT NOT NULL,
            report_type TEXT NOT NULL,
            status TEXT NOT NULL,
            image_filename TEXT
        )
    """)

    # Make sure old databases also have image_filename
    try:
        connection.execute(
            "ALTER TABLE reports ADD COLUMN image_filename TEXT"
        )
    except sqlite3.OperationalError:
        pass

    connection.commit()
    connection.close()


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    connection = get_db_connection()

    total_reports = connection.execute(
        "SELECT COUNT(*) FROM reports"
    ).fetchone()[0]

    found_items = connection.execute("""
        SELECT COUNT(*)
        FROM reports
        WHERE report_type = 'FOUND'
    """).fetchone()[0]

    returned_items = connection.execute("""
        SELECT COUNT(*)
        FROM reports
        WHERE status = 'RETURNED'
    """).fetchone()[0]

    recent_reports = connection.execute("""
        SELECT *
        FROM reports
        WHERE status = 'ACTIVE'
        ORDER BY id DESC
        LIMIT 3
    """).fetchall()

    connection.close()

    return render_template(
        "index.html",
        total_reports=total_reports,
        found_items=found_items,
        returned_items=returned_items,
        recent_reports=recent_reports
    )

# =========================================================
# REPORT LOST
# =========================================================

@app.route("/report-lost", methods=["GET", "POST"])
def report_lost():

    if request.method == "POST":

        item_name = request.form["item_name"]
        category = request.form["category"]
        color = request.form["color"]
        description = request.form["description"]

        location_type = request.form["location_type"]
        location_details = request.form["location_details"]

        date_lost = request.form["date_lost"]
        time_lost = request.form["time_lost"]

        # -----------------------------------------
        # IMAGE UPLOAD
        # -----------------------------------------

        image = request.files.get("image")
        image_filename = None

        if image and image.filename:

            image_filename = secure_filename(image.filename)

            upload_folder = os.path.join(
                app.root_path,
                "static",
                "uploads"
            )

            os.makedirs(upload_folder, exist_ok=True)

            image.save(
                os.path.join(
                    upload_folder,
                    image_filename
                )
            )

        # -----------------------------------------
        # DATABASE INSERT
        # -----------------------------------------

        connection = get_db_connection()

        cursor = connection.execute("""
            INSERT INTO reports (
                item_name,
                category,
                color,
                description,
                location_type,
                location_details,
                date_lost,
                time_lost,
                report_type,
                status,
                image_filename
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item_name,
            category,
            color,
            description,
            location_type,
            location_details,
            date_lost,
            time_lost,
            "LOST",
            "ACTIVE",
            image_filename
        ))

        connection.commit()

        report_id = cursor.lastrowid

        connection.close()

        return redirect(
            url_for(
                "report_success",
                report_id=report_id
            )
        )

    return render_template("report_lost.html")


# =========================================================
# REPORT FOUND
# =========================================================

@app.route("/report-found", methods=["GET", "POST"])
def report_found():

    if request.method == "POST":

        item_name = request.form["item_name"]
        category = request.form["category"]
        color = request.form["color"]
        description = request.form["description"]

        location_type = request.form["location_type"]
        location_details = request.form["location_details"]

        date_lost = request.form["date_lost"]
        time_lost = request.form["time_lost"]

        # -----------------------------------------
        # IMAGE UPLOAD
        # -----------------------------------------

        image = request.files.get("image")
        image_filename = None

        if image and image.filename:

            image_filename = secure_filename(image.filename)

            upload_folder = os.path.join(
                app.root_path,
                "static",
                "uploads"
            )

            os.makedirs(upload_folder, exist_ok=True)

            image.save(
                os.path.join(
                    upload_folder,
                    image_filename
                )
            )

        # -----------------------------------------
        # DATABASE INSERT
        # -----------------------------------------

        connection = get_db_connection()

        cursor = connection.execute("""
            INSERT INTO reports (
                item_name,
                category,
                color,
                description,
                location_type,
                location_details,
                date_lost,
                time_lost,
                report_type,
                status,
                image_filename
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item_name,
            category,
            color,
            description,
            location_type,
            location_details,
            date_lost,
            time_lost,
            "FOUND",
            "ACTIVE",
            image_filename
        ))

        connection.commit()

        report_id = cursor.lastrowid

        connection.close()

        return redirect(
            url_for(
                "report_success",
                report_id=report_id
            )
        )

    return render_template("report_found.html")


# =========================================================
# SEARCH
# =========================================================

@app.route("/search")
def search():

    query = request.args.get("q", "").strip()
    report_type = request.args.get("type", "ALL")
    category = request.args.get("category", "ALL")

    connection = get_db_connection()

    sql = """
        SELECT *
        FROM reports
        WHERE status = 'ACTIVE'
    """

    parameters = []

    # -----------------------------------------
    # SEARCH QUERY
    # -----------------------------------------

    if query:

        sql += """
            AND (
                item_name LIKE ?
                OR color LIKE ?
                OR description LIKE ?
                OR location_type LIKE ?
                OR location_details LIKE ?
            )
        """

        search_term = f"%{query}%"

        parameters.extend([
            search_term,
            search_term,
            search_term,
            search_term,
            search_term
        ])

    # -----------------------------------------
    # REPORT TYPE FILTER
    # -----------------------------------------

    if report_type != "ALL":

        sql += """
            AND report_type = ?
        """

        parameters.append(report_type)

    # -----------------------------------------
    # CATEGORY FILTER
    # -----------------------------------------

    if category != "ALL":

        sql += """
            AND category = ?
        """

        parameters.append(category)

    # -----------------------------------------
    # SORT
    # -----------------------------------------

    sql += """
        ORDER BY id DESC
    """

    reports = connection.execute(
        sql,
        parameters
    ).fetchall()

    connection.close()

    return render_template(
        "search.html",
        reports=reports,
        query=query,
        report_type=report_type,
        category=category
    )


# =========================================================
# MATCHES
# =========================================================

@app.route("/matches/<int:report_id>")
def matches(report_id):

    connection = get_db_connection()

    # -----------------------------------------
    # GET SELECTED REPORT
    # -----------------------------------------

    selected_report = connection.execute(
        "SELECT * FROM reports WHERE id = ?",
        (report_id,)
    ).fetchone()

    if selected_report is None:

        connection.close()

        return "Report not found", 404

    # -----------------------------------------
    # FIND OPPOSITE REPORT TYPE
    # -----------------------------------------

    if selected_report["report_type"] == "LOST":
        opposite_type = "FOUND"
    else:
        opposite_type = "LOST"

    possible_reports = connection.execute(
        """
        SELECT *
        FROM reports
        WHERE report_type = ?
        AND status = 'ACTIVE'
        AND id != ?
        """,
        (opposite_type, report_id)
    ).fetchall()

    connection.close()

    # -----------------------------------------
    # MATCHING
    # -----------------------------------------

    matches_list = []

    for report in possible_reports:

        score = 0
        reasons = []

        # -----------------------------------------
        # CATEGORY MATCH
        # -----------------------------------------

        if (
            selected_report["category"].lower()
            == report["category"].lower()
        ):

            score += 25

            reasons.append(
                "Same category"
            )

        # -----------------------------------------
        # COLOR MATCH
        # -----------------------------------------

        if (
            selected_report["color"].lower()
            == report["color"].lower()
        ):

            score += 20

            reasons.append(
                "Same color"
            )

        # -----------------------------------------
        # LOCATION MATCH
        # -----------------------------------------

        if (
            selected_report["location_type"].lower()
            == report["location_type"].lower()
        ):

            score += 15

            reasons.append(
                "Same location"
            )

        # -----------------------------------------
        # LOCATION DETAILS / BLOCK MATCH
        # -----------------------------------------

        selected_location_details = (
            selected_report["location_details"] or ""
        ).lower()

        report_location_details = (
            report["location_details"] or ""
        ).lower()

        if (
            selected_location_details
            and report_location_details
            and selected_location_details
            == report_location_details
        ):

            score += 10

            reasons.append(
                "Same block"
            )

        # -----------------------------------------
        # ITEM NAME MATCH
        # -----------------------------------------

        selected_name = (
            selected_report["item_name"] or ""
        ).lower()

        report_name = (
            report["item_name"] or ""
        ).lower()

        selected_words = set(
            selected_name.split()
        )

        report_words = set(
            report_name.split()
        )

        common_words = (
            selected_words
            & report_words
        )

        name_similarity = (
            len(common_words)
            / max(
                len(selected_words),
                len(report_words),
                1
            )
        )

        if name_similarity >= 0.75:

            score += 20

            reasons.append(
                "Very similar item name"
            )

        elif name_similarity >= 0.5:

            score += 15

            reasons.append(
                "Similar item name"
            )

        elif name_similarity > 0:

            score += 8

            reasons.append(
                "Partially similar item name"
            )

        # -----------------------------------------
        # DATE MATCH
        # -----------------------------------------

        if (
            selected_report["date_lost"]
            == report["date_lost"]
        ):

            score += 5

            reasons.append(
                "Same date"
            )

        # -----------------------------------------
        # TIME MATCH
        # -----------------------------------------

        try:

            selected_time = datetime.strptime(
                selected_report["time_lost"],
                "%H:%M"
            )

            report_time = datetime.strptime(
                report["time_lost"],
                "%H:%M"
            )

            difference = abs(
                (
                    selected_time
                    - report_time
                ).total_seconds()
            ) / 60

            if difference <= 30:

                score += 5

                reasons.append(
                    "Time within 30 minutes"
                )

            elif difference <= 120:

                score += 2

                reasons.append(
                    "Time within 2 hours"
                )

        except (ValueError, TypeError):

            pass

        # -----------------------------------------
        # STORE MATCH
        # -----------------------------------------

        if score >= 30:

            matches_list.append({
                "report": report,
                "score": score,
                "reasons": reasons
            })

    # -----------------------------------------
    # HIGHEST SCORE FIRST
    # -----------------------------------------

    matches_list.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return render_template(
        "matches.html",
        selected_report=selected_report,
        matches=matches_list
    )


# =========================================================
# REPORT DETAILS
# =========================================================

@app.route("/report/<int:report_id>")
def report_details(report_id):

    connection = get_db_connection()

    report = connection.execute(
        """
        SELECT *
        FROM reports
        WHERE id = ?
        """,
        (report_id,)
    ).fetchone()

    connection.close()

    if report is None:

        return "Report not found", 404

    return render_template(
        "report_details.html",
        report=report
    )


# =========================================================
# REPORT SUCCESS
# =========================================================

@app.route("/report-success/<int:report_id>")
def report_success(report_id):

    connection = get_db_connection()

    report = connection.execute(
        "SELECT * FROM reports WHERE id = ?",
        (report_id,)
    ).fetchone()

    connection.close()

    if report is None:

        return "Report not found", 404

    return render_template(
        "report_success.html",
        report=report
    )


# =========================================================
# MARK REPORT AS RETURNED
# =========================================================

@app.route(
    "/report/<int:report_id>/returned",
    methods=["POST"]
)
def mark_returned(report_id):

    connection = get_db_connection()

    connection.execute(
        """
        UPDATE reports
        SET status = 'RETURNED'
        WHERE id = ?
        """,
        (report_id,)
    )

    connection.commit()
    connection.close()

    return redirect(
        url_for(
            "report_details",
            report_id=report_id
        )
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    initialize_database()

    app.run(debug=True)
