from abc import ABC, abstractmethod


class JobSource(ABC):

    @abstractmethod
    def fetch_jobs(self) -> list[dict]:
        """
        Fetch jobs from a specific job source.
        """
        pass