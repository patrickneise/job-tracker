import pytest


@pytest.fixture()
def job_payload():
    return {
        "id": 1,
        "company": "Netflix",
        "title": "Chief Technology Officer",
        "description": "CTO at Netflix",
        "posting": "https://www.netflix.com/posting/1",
        "website": "https://www.netflix.com/",
        "status": "watching",
    }


@pytest.fixture()
def jobs_payload():
    return [
        {
            "id": 1,
            "company": "Netflix",
            "title": "Chief Technology Officer",
            "description": "CTO at Netflix",
            "posting": "https://www.netflix.com/posting/1",
            "website": "https://www.netflix.com/",
            "status": "watching",
        },
        {
            "id": 2,
            "company": "GitHub",
            "title": "VP, Engineering",
            "description": "VP of Eng at GitHub",
            "posting": "https://www.github.com.com/posting/1",
            "website": "https://www.github.com/",
            "status": "applied",
        },
    ]
