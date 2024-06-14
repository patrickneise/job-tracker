BASE_PATH = "/api/jobs"


def test_create_get_interview(test_client, interview_payload, job_payload):
    create_job_response = test_client.post(BASE_PATH, json=job_payload)
    assert create_job_response.status_code == 201

    create_interview_response = test_client.post(
        f"{BASE_PATH}/{job_payload["id"]}/interviews", json=interview_payload
    )
    assert create_interview_response.status_code == 201

    get_interview_response = test_client.get(
        f"{BASE_PATH}/{job_payload["id"]}/interviews/{interview_payload["id"]}"
    )
    assert get_interview_response.status_code == 200

    get_interview_response_json = get_interview_response.json()
    assert get_interview_response_json["id"] == interview_payload["id"]
    assert get_interview_response_json["start"] == interview_payload["start"]
    assert get_interview_response_json["stop"] == interview_payload["stop"]
    assert get_interview_response_json["details"] == interview_payload["details"]
    assert get_interview_response_json["url"] == interview_payload["url"]


def test_create_interview_fail(test_client, interview_payload, job_payload):
    create_job_response = test_client.post(BASE_PATH, json=job_payload)
    assert create_job_response.status_code == 201

    interview_payload.pop("details")
    create_interview_response = test_client.post(
        f"{BASE_PATH}/{job_payload["id"]}/interviews", json=interview_payload
    )
    assert create_interview_response.status_code == 422


def test_create_existing_interview(test_client, interview_payload, job_payload):
    create_job_response = test_client.post(BASE_PATH, json=job_payload)
    assert create_job_response.status_code == 201

    create_interview_response = test_client.post(
        f"{BASE_PATH}/{job_payload["id"]}/interviews", json=interview_payload
    )
    assert create_interview_response.status_code == 201

    second_create_interview_response = test_client.post(
        f"{BASE_PATH}/{job_payload["id"]}/interviews", json=interview_payload
    )
    assert second_create_interview_response.status_code == 409


def test_get_missing_interview(test_client, job_payload):
    create_job_response = test_client.post(BASE_PATH, json=job_payload)
    assert create_job_response.status_code == 201

    get_interview_response = test_client.get(f"{BASE_PATH}/1/interviews/1")
    assert get_interview_response.status_code == 404


def test_create_get_interviews(test_client, job_payload, interviews_payload):
    create_job_response = test_client.post(BASE_PATH, json=job_payload)
    assert create_job_response.status_code == 201

    for interview_payload in interviews_payload:
        create_response = test_client.post(
            f"{BASE_PATH}/{job_payload["id"]}/interviews", json=interview_payload
        )
        assert create_response.status_code == 201

    get_interviews_response = test_client.get(
        f"{BASE_PATH}/{job_payload["id"]}/interviews"
    )
    assert get_interviews_response.status_code == 200

    get_interviews_response_json = get_interviews_response.json()
    for index, interview_payload in enumerate(interviews_payload):
        assert get_interviews_response_json[index]["id"] == interview_payload["id"]
        assert (
            get_interviews_response_json[index]["start"] == interview_payload["start"]
        )
        assert get_interviews_response_json[index]["stop"] == interview_payload["stop"]
        assert (
            get_interviews_response_json[index]["details"]
            == interview_payload["details"]
        )
        assert get_interviews_response_json[index]["url"] == interview_payload["url"]


def test_get_interviews_limit(test_client, job_payload, interviews_payload):
    create_job_response = test_client.post(BASE_PATH, json=job_payload)
    assert create_job_response.status_code == 201

    for interview_payload in interviews_payload:
        create_response = test_client.post(
            f"{BASE_PATH}/{job_payload["id"]}/interviews", json=interview_payload
        )
        assert create_response.status_code == 201

    get_interviews_response = test_client.get(
        f"{BASE_PATH}/0/interviews", params={"limit": 1}
    )
    assert get_interviews_response.status_code == 200

    get_interviews_response_json = get_interviews_response.json()
    assert len(get_interviews_response_json) == 1
    assert get_interviews_response_json[0]["id"] == interviews_payload[0]["id"]
    assert get_interviews_response_json[0]["start"] == interviews_payload[0]["start"]
    assert get_interviews_response_json[0]["stop"] == interviews_payload[0]["stop"]
    assert (
        get_interviews_response_json[0]["details"] == interviews_payload[0]["details"]
    )
    assert get_interviews_response_json[0]["url"] == interviews_payload[0]["url"]


def test_get_interviews_skip(test_client, job_payload, interviews_payload):
    create_job_response = test_client.post(BASE_PATH, json=job_payload)
    assert create_job_response.status_code == 201

    for interview_payload in interviews_payload:
        create_response = test_client.post(
            f"{BASE_PATH}/{job_payload["id"]}/interviews", json=interview_payload
        )
        assert create_response.status_code == 201

    get_interviews_response = test_client.get(
        f"{BASE_PATH}/0/interviews", params={"skip": 1}
    )
    assert get_interviews_response.status_code == 200

    get_interviews_response_json = get_interviews_response.json()
    assert len(get_interviews_response_json) == 1
    assert get_interviews_response_json[0]["id"] == interviews_payload[1]["id"]
    assert get_interviews_response_json[0]["start"] == interviews_payload[1]["start"]
    assert get_interviews_response_json[0]["stop"] == interviews_payload[1]["stop"]
    assert (
        get_interviews_response_json[0]["details"] == interviews_payload[1]["details"]
    )
    assert get_interviews_response_json[0]["url"] == interviews_payload[1]["url"]


# test update interview

# test update missing interview

# test update interview to existing interview

# test delete existing interview

# test delete nonexisting interview
