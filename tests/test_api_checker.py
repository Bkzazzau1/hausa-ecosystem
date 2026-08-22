from hausa_ecosystem import api_checker


class FakeApi:
    def __init__(self):
        self.created = {"id": 1, "suna": "Gwajin Hausa API"}
        self.deleted = False

    def __call__(self, method, base_url, path, payload=None, timeout=5):
        if method == "GET" and path == "/":
            return 200, {"sako": "ok"}, '{"sako":"ok"}'

        if method == "GET" and path == "/abubuwa":
            return 200, [], "[]"

        if method == "POST" and path == "/abubuwa":
            return 201, self.created, '{"id":1,"suna":"Gwajin Hausa API"}'

        if method == "GET" and path == "/abubuwa/1" and not self.deleted:
            return 200, self.created, '{"id":1,"suna":"Gwajin Hausa API"}'

        if method == "PUT" and path == "/abubuwa/1":
            self.created = {"id": 1, "suna": payload["suna"]}
            return 200, self.created, '{"id":1,"suna":"An sabunta ta Hausa API"}'

        if method == "DELETE" and path == "/abubuwa/1":
            self.deleted = True
            return 200, {"sako": "An goge abu"}, '{"sako":"An goge abu"}'

        if method == "GET" and path == "/abubuwa/1" and self.deleted:
            return 404, {"detail": "not found"}, '{"detail":"not found"}'

        return 500, {"error": "unexpected"}, '{"error":"unexpected"}'


def test_run_crud_checks_passes_when_api_matches_expected_contract(monkeypatch, capsys):
    monkeypatch.setattr(api_checker, "call_api", FakeApi())

    exit_code = api_checker.run_crud_checks("http://example.test")
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Sakamako: 7 passed, 0 failed" in captured.out
    assert "PASS: POST /abubuwa" in captured.out
    assert "PASS: GET deleted /abubuwa/{id} returns 404" in captured.out


def test_run_api_tests_rejects_bad_arguments(capsys):
    exit_code = api_checker.run_api_tests(["flask"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Kuskure" in captured.out


def test_run_crud_checks_fails_when_create_has_no_id(monkeypatch, capsys):
    def fake_call_api(method, base_url, path, payload=None, timeout=5):
        if method == "GET" and path == "/":
            return 200, {}, "{}"
        if method == "GET" and path == "/abubuwa":
            return 200, [], "[]"
        if method == "POST" and path == "/abubuwa":
            return 201, {"suna": "No ID"}, '{"suna":"No ID"}'
        return 500, {}, "{}"

    monkeypatch.setattr(api_checker, "call_api", fake_call_api)

    exit_code = api_checker.run_crud_checks("http://example.test")
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "FAIL: POST /abubuwa" in captured.out
