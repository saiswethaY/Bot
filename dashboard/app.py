from flask import Flask, render_template

from database.connection import get_connection


app = Flask(__name__)


def get_dashboard_data():
    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM jobs;
                """
            )
            total_jobs = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM job_matches;
                """
            )
            total_matches = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM applications
                WHERE application_status = 'SUBMITTED';
                """
            )
            submitted_applications = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM applications
                WHERE application_status = 'FAILED';
                """
            )
            failed_applications = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT
                    j.job_title,
                    j.company_name,
                    j.location,
                    jm.match_score,
                    jm.match_status
                FROM job_matches jm
                JOIN jobs j
                    ON jm.job_id = j.job_id
                ORDER BY jm.evaluated_at DESC
                LIMIT 10;
                """
            )

            matches = cursor.fetchall()

            cursor.execute(
                """
                SELECT
                    a.application_id,
                    j.job_title,
                    j.company_name,
                    a.application_status,
                    a.applied_at,
                    a.failure_reason
                FROM applications a
                JOIN jobs j
                    ON a.job_id = j.job_id
                ORDER BY a.updated_at DESC
                LIMIT 10;
                """
            )

            applications = cursor.fetchall()

    return {
        "total_jobs": total_jobs,
        "total_matches": total_matches,
        "submitted_applications": submitted_applications,
        "failed_applications": failed_applications,
        "matches": matches,
        "applications": applications,
    }


@app.route("/")
def dashboard():
    data = get_dashboard_data()

    return render_template(
        "dashboard.html",
        data=data,
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )