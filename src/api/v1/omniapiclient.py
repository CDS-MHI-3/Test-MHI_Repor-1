import json
import logging
from http import HTTPStatus
from typing import List

from requests import Response, Session

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def build_result_list_from_responses(responses: List[dict]):
    results = []
    for response in responses:
        # if response.status_code == 200 and "results" in response.json():
        results.extend(response.json()["results"])
    return results


class OmniAPIClient:
    def __init__(self, base_url: str, verify_ssl: bool = True):
        self.base_url = base_url
        self.session = Session()
        self.verify_ssl = verify_ssl
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json;charset=UTF-8",
            }
        )
        self.username = ""
        self.password = ""

    def get(self, path: str, **kwargs) -> Response:
        url = self.base_url + path
        logger.debug(f"GET {url} {kwargs}")
        return self.session.get(url, verify=self.verify_ssl, **kwargs)

    def get_uri(self, uri: str) -> Response:
        """
        Useful for queries using pagination urls from the previous
        response.
        """
        logger.debug(f"GET {uri}")
        return self.session.get(uri, verify=self.verify_ssl)

    def get_all_results(self, path: str, page_limit: int = -1, **kwargs) -> List[dict]:
        """
        Paginates over the results of a GET request and returns a List with all the responses.
        """
        responses = []
        endpoint_response = self.get(path, **kwargs)
        responses.append(endpoint_response)
        page_limit -= 1
        while "next" in endpoint_response.json().keys() and page_limit:
            next_url = endpoint_response.json()["next"]
            if next_url is None or len(endpoint_response.json()["results"]) == 0:
                break
            logger.debug(f"GET {next_url}")
            # using session get() method here because the baseurl is included in the response
            endpoint_response = self.session.get(
                next_url,
                verify=self.verify_ssl,
            )
            responses.append(endpoint_response)
            page_limit -= 1
        return build_result_list_from_responses(responses)

    def post(self, path: str, data=None, json=None, **kwargs):
        url = self.base_url + path
        logger.debug(f"POST {url} data:{data} json:{json}")
        return self.session.post(url, data, json, verify=self.verify_ssl, **kwargs)

    def put(self, path: str, data=None, **kwargs) -> Response:
        url = self.base_url + path
        logger.debug(f"PUT {url} data:{data} {kwargs}")
        return self.session.put(url, data, verify=self.verify_ssl, **kwargs)

    def delete(self, path: str, **kwargs) -> Response:
        url = self.base_url + path
        logger.debug(f"DELETE {url} {kwargs}")
        return self.session.delete(url, verify=self.verify_ssl, **kwargs)

    def patch(self, path, data=None, **kwargs) -> Response:
        url = self.base_url + path
        logger.debug(f"PATCH {url} data:{data} {kwargs}")
        return self.session.patch(url, data, verify=self.verify_ssl, **kwargs)

    def user_login(self, username, password) -> Response:
        data = json.dumps({"username": username, "password": password})
        resp = self.post("api/v1/core/user/login/", data=data)
        if resp.status_code == HTTPStatus.OK:
            self.session.headers.update(
                {
                    "x-csrftoken": resp.json()["csrf"],
                    "Cookie": f"csrftoken={resp.json()['csrf']}; sessionid={resp.json()['session']['id']}",
                    "Authorization": f"session {resp.json()['session']['id']}",
                    "Referer": f"{self.base_url}",
                }
            )
            self.username = username
            self.password = password
            logger.info(f"Successful Login {self.base_url}")
        else:
            logger.critical(
                f"There was a problem logging in to {self.base_url} with {username} - check the password"
            )
            print(
                f"There was a problem logging in to {self.base_url} with {username} - check the password"
            )
        return resp
