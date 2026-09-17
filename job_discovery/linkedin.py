from job_discovery.base import JobSource


class LinkedInSource(JobSource):

    def fetch_jobs(self) -> list[dict]:
        """
        LinkedIn discovery is not implemented yet.

        This source intentionally returns no jobs so that
        test/demo records cannot enter the production pipeline.
        """
        print("=" * 60)
        print("LINKEDIN JOB DISCOVERY")
        print("=" * 60)
        print("LinkedIn real discovery is not implemented yet.")
        print("No LinkedIn jobs will be returned.")
        print("=" * 60)

        return []