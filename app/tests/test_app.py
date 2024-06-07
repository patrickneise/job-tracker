def test_create_get_job(test_client, job_payload):
    create_response = test_client.post("/jobs", data=job_payload)
    assert create_response.status_code == 200

    get_response = test_client.get(f"/jobs/{job_payload["id"]}")
    assert get_response.status_code == 200

    assert f"{job_payload["company"]}" in get_response.text
    assert f"{job_payload["title"]}" in get_response.text
    assert f"{job_payload["description"]}" in get_response.text
    assert f"{job_payload["posting"]}" in get_response.text
    assert f"{job_payload["website"]}" in get_response.text


def test_create_get_jobs(test_client, jobs_payload):
    for job_payload in jobs_payload:
        create_response = test_client.post("/jobs", data=job_payload)
        assert create_response.status_code == 200

    get_response = test_client.get("/jobs/")
    assert get_response.status_code == 200

    for job_payload in jobs_payload:
        assert f"/jobs/{job_payload["id"]}" in get_response.text
        assert f"{job_payload["company"]}" in get_response.text
        assert f"{job_payload["title"]}" in get_response.text
        assert f"{job_payload["description"]}" in get_response.text
        assert f"{job_payload["posting"]}" in get_response.text
        assert f"{job_payload["website"]}" in get_response.text


def test_get_jobs_limit(test_client, jobs_payload):
    for job_payload in jobs_payload:
        create_response = test_client.post("/jobs/", data=job_payload)
        assert create_response.status_code == 200

    get_response = test_client.get("/jobs/", params={"limit": 1})
    assert get_response.status_code == 200

    assert f"/jobs/{jobs_payload[0]["id"]}" in get_response.text
    assert f"{jobs_payload[0]["company"]}" in get_response.text
    assert f"{jobs_payload[0]["title"]}" in get_response.text
    assert f"{jobs_payload[0]["description"]}" in get_response.text
    assert f"{jobs_payload[0]["posting"]}" in get_response.text
    assert f"{jobs_payload[0]["website"]}" in get_response.text

    assert f"/jobs/{jobs_payload[1]["id"]}" not in get_response.text
    assert f"{jobs_payload[1]["company"]}" not in get_response.text
    assert f"{jobs_payload[1]["title"]}" not in get_response.text
    assert f"{jobs_payload[1]["description"]}" not in get_response.text
    assert f"{jobs_payload[1]["posting"]}" not in get_response.text
    assert f"{jobs_payload[1]["website"]}" not in get_response.text


def test_get_jobs_skip(test_client, jobs_payload):
    for job_payload in jobs_payload:
        create_response = test_client.post("/jobs/", data=job_payload)
        assert create_response.status_code == 200

    get_response = test_client.get("/jobs/", params={"skip": 1})
    assert get_response.status_code == 200

    assert f"/jobs/{jobs_payload[0]["id"]}" not in get_response.text
    assert f"{jobs_payload[0]["company"]}" not in get_response.text
    assert f"{jobs_payload[0]["title"]}" not in get_response.text
    assert f"{jobs_payload[0]["description"]}" not in get_response.text
    assert f"{jobs_payload[0]["posting"]}" not in get_response.text
    assert f"{jobs_payload[0]["website"]}" not in get_response.text

    assert f"/jobs/{jobs_payload[1]["id"]}" in get_response.text
    assert f"{jobs_payload[1]["company"]}" in get_response.text
    assert f"{jobs_payload[1]["title"]}" in get_response.text
    assert f"{jobs_payload[1]["description"]}" in get_response.text
    assert f"{jobs_payload[1]["posting"]}" in get_response.text
    assert f"{jobs_payload[1]["website"]}" in get_response.text
