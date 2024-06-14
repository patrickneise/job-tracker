BASE_PATH = "/api/jobs"


def test_create_get_job(test_client, job_payload):
    create_response = test_client.post(BASE_PATH, json=job_payload)
    assert create_response.status_code == 201

    get_response = test_client.get(f"{BASE_PATH}/{job_payload["id"]}")
    assert get_response.status_code == 200

    get_response_json = get_response.json()
    assert get_response_json["id"] == job_payload["id"]
    assert get_response_json["company"] == job_payload["company"]
    assert get_response_json["title"] == job_payload["title"]
    assert get_response_json["description"] == job_payload["description"]
    assert get_response_json["posting"] == job_payload["posting"]
    assert get_response_json["website"] == job_payload["website"]


def test_create_job_fail(test_client, job_payload):
    job_payload.pop("company")
    create_response = test_client.post(BASE_PATH, json=job_payload)
    assert create_response.status_code == 422


def test_create_existing_job(test_client, job_payload):
    create_response = test_client.post(BASE_PATH, json=job_payload)
    assert create_response.status_code == 201

    second_create_response = test_client.post(BASE_PATH, json=job_payload)
    assert second_create_response.status_code == 409


def test_get_missing_job(test_client):
    response = test_client.get(f"{BASE_PATH}/1")
    assert response.status_code == 404


def test_create_get_jobs(test_client, jobs_payload):
    for job_payload in jobs_payload:
        create_response = test_client.post(BASE_PATH, json=job_payload)
        assert create_response.status_code == 201

    get_response = test_client.get(BASE_PATH)
    assert get_response.status_code == 200

    get_response_json = get_response.json()
    for index, job_payload in enumerate(jobs_payload):
        assert get_response_json[index]["id"] == job_payload["id"]
        assert get_response_json[index]["company"] == job_payload["company"]
        assert get_response_json[index]["title"] == job_payload["title"]
        assert get_response_json[index]["description"] == job_payload["description"]
        assert get_response_json[index]["posting"] == job_payload["posting"]
        assert get_response_json[index]["website"] == job_payload["website"]


def test_get_jobs_limit(test_client, jobs_payload):
    for job_payload in jobs_payload:
        create_response = test_client.post(BASE_PATH, json=job_payload)
        assert create_response.status_code == 201

    get_response = test_client.get(BASE_PATH, params={"limit": 1})
    assert get_response.status_code == 200

    get_response_json = get_response.json()
    assert len(get_response_json) == 1

    assert get_response_json[0]["id"] == jobs_payload[0]["id"]
    assert get_response_json[0]["company"] == jobs_payload[0]["company"]
    assert get_response_json[0]["title"] == jobs_payload[0]["title"]
    assert get_response_json[0]["description"] == jobs_payload[0]["description"]
    assert get_response_json[0]["posting"] == jobs_payload[0]["posting"]
    assert get_response_json[0]["website"] == jobs_payload[0]["website"]


def test_get_jobs_skip(test_client, jobs_payload):
    for job_payload in jobs_payload:
        create_response = test_client.post(BASE_PATH, json=job_payload)
        assert create_response.status_code == 201

    get_response = test_client.get(BASE_PATH, params={"skip": 1})
    assert get_response.status_code == 200

    get_response_json = get_response.json()
    assert len(get_response_json) == 1

    assert get_response_json[0]["id"] == jobs_payload[1]["id"]
    assert get_response_json[0]["company"] == jobs_payload[1]["company"]
    assert get_response_json[0]["title"] == jobs_payload[1]["title"]
    assert get_response_json[0]["description"] == jobs_payload[1]["description"]
    assert get_response_json[0]["posting"] == jobs_payload[1]["posting"]
    assert get_response_json[0]["website"] == jobs_payload[1]["website"]


def test_update_job(test_client, job_payload):
    create_response = test_client.post("/api/jobs", json=job_payload)
    assert create_response.status_code == 201

    update_payload = {"description": "Chief Technology Officer at Netflix"}
    update_response = test_client.put("/api/jobs/1", json=update_payload)
    assert update_response.status_code == 202

    update_response_json = update_response.json()
    assert update_response_json["id"] == job_payload["id"]
    assert update_response_json["company"] == job_payload["company"]
    assert update_response_json["title"] == job_payload["title"]
    assert update_response_json["description"] == update_payload["description"]
    assert update_response_json["posting"] == job_payload["posting"]
    assert update_response_json["website"] == job_payload["website"]


def test_update_missing_job(test_client):
    update_payload = {"description": "Chief Technology Officer at Netflix"}
    update_response = test_client.put("/api/jobs/1", json=update_payload)
    assert update_response.status_code == 404


def test_update_job_to_current_job(test_client, jobs_payload):
    for job_payload in jobs_payload:
        create_response = test_client.post(BASE_PATH, json=job_payload)
        assert create_response.status_code == 201

    update_payload = {
        "company": jobs_payload[0]["company"],
        "title": jobs_payload[0]["title"],
    }
    update_response = test_client.put("/api/jobs/2", json=update_payload)
    assert update_response.status_code == 409


def test_delete_existing_job(test_client, job_payload):
    create_response = test_client.post("/api/jobs", json=job_payload)
    assert create_response.status_code == 201

    delete_response = test_client.delete(f"/api/jobs/{job_payload["id"]}")
    assert delete_response.status_code == 202


def test_delete_nonexisting_job(test_client, job_payload):
    delete_response = test_client.delete(f"/api/jobs/{job_payload["id"]}")
    assert delete_response.status_code == 404
