from job_discovery.base import JobSource


class TestJobSource(JobSource):

    def fetch_jobs(self) -> list[dict]:
        return [
            {
                "source": "TEST",
                "external_job_id": "TEST-001",
                "job_title": "Azure Data Engineer",
                "company_name": "Demo Analytics",
                "location": "Bangalore",
                "experience_min": 2.0,
                "experience_max": 4.0,
                "job_url": "https://example.com/jobs/TEST-001",
                "description": (
                    "Looking for an Azure Data Engineer with "
                    "SQL, Python, PySpark, ADF and Databricks skills."
                ),
            },
            {
                "source": "TEST",
                "external_job_id": "TEST-002",
                "job_title": "Python Developer",
                "company_name": "Demo Software",
                "location": "Hyderabad",
                "experience_min": 2.0,
                "experience_max": 5.0,
                "job_url": "https://example.com/jobs/TEST-002",
                "description": (
                    "Looking for a Python developer with "
                    "Django and REST API experience."
                ),
            },
        ]