from job_discovery.base import JobSource


class TestJobSource(JobSource):

    def fetch_jobs(self) -> list[dict]:
        return [
            {
                "job_title": "Data Engineer",
                "company_name": "Test Company",
            }
        ]


source = TestJobSource()

jobs = source.fetch_jobs()

print(jobs)