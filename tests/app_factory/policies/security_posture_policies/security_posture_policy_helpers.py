"""
Helper class to generate service config policy rule payloads as JSON objects
"""

from http import HTTPStatus
from pytest_check import check
from src.enums import Polarity
from src.api.v1.omniapiclient import OmniAPIClient
from src.api.v1.core.policy import Policy

base_json_object = {
    "policy": 1,
    "rule_type": "typevalue",
    "name": "namevalue",
    "tags": [],
}

ms_config_object = {
    "md_version": 1,
    "md_kind": "temp",
    "setting_name": "temp",
    "polarity": Polarity.must_be,
    "values": ["true"],
}

SYSTEM_CONFIG = "system_config"
IS_ID = "polarity_is_policy_id"
NOT_ID = "polarity_not_policy_id"
ALL_ID = "polarity_all_policy_id"


def add_monitored_service(
    tenant: OmniAPIClient,
    service_ms_id: int,
    list_of_policies: list,
) -> None:
    """
    Adds monitored services to the policies to be used for testing

    :param tenant: Omni connector to the tenant to add the monitored services to
    :param service_ms_id: Service monitor service ID
    :param list_of_policies: IDs for the comprehensive Service Policy

    :return: None
    """
    payload = {"monitored_services": [service_ms_id]}
    for policy_id in list_of_policies:
        add_monitored_service_response = tenant.patch(
            Policy.get_single_item_url(policy_id), json=payload
        )
        check.equal(
            add_monitored_service_response.status_code,
            HTTPStatus.OK,
            msg=f"Monitored Service patch call failed for {policy_id}, status {add_monitored_service_response.status_code} {add_monitored_service_response.text}",
        )
