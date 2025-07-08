import pytest
from typing import Any, Dict, List
from tests.app_factory.policies.security_posture_policies.security_posture_policy_helpers import (
    add_monitored_service,
    IS_ID,
    NOT_ID,
    ALL_ID,
)
from tests.app_factory.policies.policy_helpers import get_or_create_policy


@pytest.fixture()
def get_or_create_polarity_policy_ids(
    request: pytest.FixtureRequest,
    list_all_policy_polarity_payload: List[Dict[str, Any]],
) -> Dict[str, int]:
    """
    Returns a List of policy id for the policy with BOTH polarity rules for passed tenant in a tenant marker

    :param request: pytest request to fetch `tenant` marker's value
    :param list_all_policy_polarity_payload: List of policy payload for both polarity IS and IS NOT policies

    :return: List of policy ids
    """

    polarity_types: List[str] = [IS_ID, NOT_ID, ALL_ID]
    polarity_policy_ids_mapping = dict()
    tenant_marker = request.node.get_closest_marker("tenant")

    # If no value in tenant marker is passed, default tenant from OMNI_ENV is selected
    selected_tenant = (
        request.getfixturevalue("tenant")
        if not tenant_marker
        else request.getfixturevalue(tenant_marker.args[0])
    )

    # Iterate for both polarity policies IS & NOT and fetch the policy id of that policy
    for index, policy_polarity_payload in enumerate(list_all_policy_polarity_payload):
        polarity_policy_ids_mapping[polarity_types[index]] = get_or_create_policy(
            selected_tenant, policy_polarity_payload
        )

    return polarity_policy_ids_mapping


@pytest.fixture()
def ms_id(service_type: str) -> int:
    """
    Returns monitored service id
    :param service_type: Service type
    :return: Monitored service id
    """
    if service_type == "asana":
        return 79292
    elif service_type == "auth0":
        return 79297
    return 79286


@pytest.fixture()
def add_monitored_service_to_policy(
    request: pytest.FixtureRequest,
    ms_id: int,
    get_or_create_polarity_policy_ids,
):
    """
    Attaches an MS to both policies so that rbac rules can be created with rbac elements for passed tenant in a tenant marker

    :param request: pytest request to fetch `tenant` marker's value
    :param get_or_create_polarity_policy_ids: Fixture to get polarity type mapped with its policy ID
    :param ms_id: Monitored service id

    :return: None
    """
    tenant_marker = request.node.get_closest_marker("tenant")

    # If no value in tenant marker is passed, default tenant from OMNI_ENV is selected
    selected_tenant = (
        request.getfixturevalue("tenant")
        if not tenant_marker
        else request.getfixturevalue(tenant_marker.args[0])
    )

    add_monitored_service(
        tenant=selected_tenant,
        service_ms_id=ms_id,
        list_of_policies=list(get_or_create_polarity_policy_ids.values()),
    )
