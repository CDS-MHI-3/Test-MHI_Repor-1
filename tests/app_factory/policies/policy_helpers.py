import pytest
from requests import Response, JSONDecodeError
from http import HTTPStatus
from pytest_check import check

from src.enums import PolicyModes
from src.api.v1.core.policyassessment import PolicyAssessment
from src.api.v1.omniapiclient import OmniAPIClient
from src.api.v1.core.policy import Policy


def get_policy_by_name(tenant: OmniAPIClient, policy_name: str) -> dict:
    policy_params = {"limit": 25, "offset": 0, "search": policy_name}
    policy_response = tenant.get(Policy.search(query_params=policy_params))
    if policy_response.status_code != HTTPStatus.OK:
        pytest.fail(
            f"Policy fetch call failed, status {policy_response.status_code} {policy_response.text}"
        )
    try:
        return policy_response.json()["results"]
    except KeyError:
        pytest.fail(
            "results Key/property not present in policy_response json response."
        )


def get_parameter_response(
    response: Response,
    response_parameter: str,
    response_code: object,
    custom_error_message: str | None = None,
) -> any:
    """
    Verify that the response is generating the correct response code (200 or 201), the response is a valid JSON,
    and contains the parameter passed in the function. If the response_parameter is present in the JSON response, return its value.

    :param response: The response object
    :param response_code: The expected response code to verify
    :param response_parameter: The response parameter to check in the JSON response
    :param custom_error_message: Optional custom message for assertions. This message will be passed to `json_response_verify` and used for error messages related to the response verification.
    :return: The value of the response_parameter if present, None otherwise
    """

    # If response is instance of list class then we select first data and return it's requested value
    response_json = response.json()
    json_response = (
        response_json[0] if isinstance(response_json, list) else response_json
    )

    assert (
        response_parameter in json_response
    ), f"Parameter '{response_parameter}' not found in JSON response"
    return json_response.get(response_parameter)


def create_policy_payload(
    policy_name: str,
    service_type: str,
    mode: str = PolicyModes.blacklist,
    role: str = "monitored_service_config",
    ms_id: int = None,
) -> dict:
    """
    Create & return policy payload with all necessary properties
    """
    payload = {
        "name": policy_name,
        "mode": mode,
        "role": role,
        "issue_handling": "notify",
        "policy_type": service_type,
    }
    # For DSP policies, ms_id is necessary in payload
    if ms_id:
        payload["monitored_services"] = [ms_id]
    return payload


def get_single_item_url(policy_id: int) -> str:
    return Policy.base_path + f"{policy_id}/"


def check_trigger_policy_scan(tenant: OmniAPIClient, policy_ids_mapping: dict) -> None:
    """
    From policy ids of different polarity/mode types, trigger policy scan and check using policy assessment that
    the policy scan has been triggered successfully

    :param tenant: Omni Connector Session for making requests for the current tenant.
    :param policy_ids_mapping: Polarity/Mode type mapped with its policy id.

    :return: None
    """
    for policy_type, policy_id in policy_ids_mapping.items():
        policy_response: dict = tenant.get(Policy.get_single_item_url(policy_id)).json()

        if check.is_true(
            policy_response["is_runnable"],
            msg=f'Policy: {policy_id} can not be scanned due to {policy_response["not_runnable_reason"]}',
        ):
            policy_assessment_response: Response = tenant.post(
                PolicyAssessment.base_path, json={"policy": policy_id}
            )

            check.equal(
                policy_assessment_response.status_code,
                HTTPStatus.CREATED,
                msg=f"Policy with ID:{policy_id} and type: {policy_type} failed to scan with status code: {policy_assessment_response.status_code}, text: {policy_assessment_response.text}",
            )

            policy_assessment_id = policy_assessment_response.json()["id"]

            check.is_instance(
                policy_assessment_id,
                int,
                msg=f"Policy with ID:{policy_id} and type: {policy_type} failed to trigger scan.",
            )


def get_or_create_policy(
    tenant: OmniAPIClient, payload: dict, ms_id: int = None
) -> int:
    """
    Get or create Policy

    :param tenant: Omni Connector Session for making requests for the current tenant
    :param payload: Payload to get/create policy
    :param ms_id: Monitored service ID of specific service type, Defaults None.

    :return: Policy ID
    """
    try:
        policy_json = get_policy_by_name(tenant, payload["name"])
        if len(policy_json):
            try:
                return policy_json[0]["id"]
            except (KeyError, IndexError) as json_error:
                check.fail(f"Error retrieving policy ID: {str(json_error)}")
        else:
            # If policy doesn't exist, create a Policy with the payload
            if ms_id:
                payload["monitored_services"] = [ms_id]
            return int(
                get_parameter_response(
                    tenant.post(Policy.base_path, json=payload),
                    "id",
                    HTTPStatus.CREATED,
                )
            )
    except JSONDecodeError as json_decode_error:
        check.fail(f"JSON Decode Error: {str(json_decode_error)}")
    except Exception as e:
        check.fail(f"An unexpected error occurred: {str(e)}")
