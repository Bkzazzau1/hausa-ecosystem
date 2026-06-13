import json
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


def make_url(base_url, path):
    return urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))


def parse_body(text):
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def call_api(method, base_url, path, payload=None, timeout=5):
    data = None
    headers = {"Accept": "application/json"}

    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = Request(make_url(base_url, path), data=data, headers=headers, method=method)

    try:
        with urlopen(request, timeout=timeout) as response:
            text = response.read().decode("utf-8")
            return response.status, parse_body(text), text
    except HTTPError as error:
        text = error.read().decode("utf-8")
        return error.code, parse_body(text), text


def run_api_tests(args):
    if len(args) != 2 or args[0] not in ("flask", "fastapi"):
        print("Kuskure: Yi amfani da: hausa test-api flask http://127.0.0.1:5000")
        print("Ko:      hausa test-api fastapi http://127.0.0.1:8000")
        return 1

    framework, base_url = args
    print(f"Ana gwada {framework} API: {base_url}")

    try:
        return run_crud_checks(base_url)
    except URLError as error:
        print(f"FAIL: API ba ta amsa ba: {error}")
        print("Ka tabbatar server yana kunne sannan ka sake gwadawa.")
        return 1
    except TimeoutError:
        print("FAIL: API ta dauki lokaci sosai kafin ta amsa.")
        return 1


def run_crud_checks(base_url):
    passed = 0
    failed = 0

    def check(name, condition, details=""):
        nonlocal passed, failed
        if condition:
            print(f"PASS: {name}")
            passed += 1
            return True
        print(f"FAIL: {name}")
        if details:
            print(f"  {details}")
        failed += 1
        return False

    status, body, text = call_api("GET", base_url, "/")
    check("GET /", status == 200, f"status={status}, body={text}")

    status, body, text = call_api("GET", base_url, "/abubuwa")
    check("GET /abubuwa", status == 200 and isinstance(body, list), f"status={status}, body={text}")

    status, body, text = call_api("POST", base_url, "/abubuwa", {"suna": "Gwajin Hausa API"})
    created_id = body.get("id") if isinstance(body, dict) else None
    check("POST /abubuwa", status in (200, 201) and created_id is not None, f"status={status}, body={text}")

    if created_id is None:
        print(f"Sakamako: {passed} passed, {failed} failed")
        return 1

    status, body, text = call_api("GET", base_url, f"/abubuwa/{created_id}")
    check("GET /abubuwa/{id}", status == 200 and isinstance(body, dict), f"status={status}, body={text}")

    status, body, text = call_api("PUT", base_url, f"/abubuwa/{created_id}", {"suna": "An sabunta ta Hausa API"})
    check(
        "PUT /abubuwa/{id}",
        status == 200 and isinstance(body, dict) and body.get("suna") == "An sabunta ta Hausa API",
        f"status={status}, body={text}",
    )

    status, body, text = call_api("DELETE", base_url, f"/abubuwa/{created_id}")
    check("DELETE /abubuwa/{id}", status == 200, f"status={status}, body={text}")

    status, body, text = call_api("GET", base_url, f"/abubuwa/{created_id}")
    check("GET deleted /abubuwa/{id} returns 404", status == 404, f"status={status}, body={text}")

    print(f"Sakamako: {passed} passed, {failed} failed")
    return 0 if failed == 0 else 1
