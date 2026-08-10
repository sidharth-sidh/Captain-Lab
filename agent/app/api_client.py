import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class ApiError(Exception):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code


class ApiClient:
    def __init__(self, server_url, timeout=10):
        self.server_url = server_url.rstrip("/")
        self.timeout = timeout

    def _post(self, path, payload):
        return self._request("POST", path, payload)

    def _get(self, path):
        return self._request("GET", path)

    def _request(self, method, path, payload=None):
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        headers = {"Accept": "application/json"}
        if body is not None:
            headers["Content-Type"] = "application/json"
        request = Request(self.server_url + path, data=body, headers=headers, method=method)
        try:
            with urlopen(request, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
                return json.loads(raw) if raw else None
        except HTTPError as error:
            try:
                detail = error.read().decode("utf-8")
            except OSError:
                detail = error.reason
            raise ApiError("HTTP {}: {}".format(error.code, detail), error.code)
        except (URLError, OSError, ValueError) as error:
            raise ApiError("Server request failed: {}".format(error))

    def register(self, computer):
        return self._post("/api/computers/register", computer)

    def list_computers(self):
        return self._get("/api/computers")

    def heartbeat(self, computer_id, computer):
        return self._post("/api/computers/{}/heartbeat".format(computer_id), computer)
