"""
Auth0 Posture Policy rule test: Verify that posture policy rules can be
created and applied to Auth0 monitored services.
"""

import pytest
from typing import Any, Dict, List
from src.enums import ServiceTypes
from src.api.v1.omniapiclient import OmniAPIClient
from tests.app_factory.policies.policy_helpers import (
    check_trigger_policy_scan,
    create_policy_payload,
)

SERVICE_TYPE = ServiceTypes.auth0

CREATE_AUTH0_POLICY_POLARITY_IS: Dict[str, Any] = create_policy_payload(
    policy_name="omni-test-united-auth0-scp-comprehensive_IS",
    service_type=SERVICE_TYPE,
)
CREATE_AUTH0_POLICY_POLARITY_NOT: Dict[str, Any] = create_policy_payload(
    policy_name="omni-test-united-auth0-scp-comprehensive_NOT",
    service_type=SERVICE_TYPE,
)

pytestmark = [pytest.mark.service_type(SERVICE_TYPE)]


@pytest.fixture(scope="module")
def list_all_policy_polarity_payload() -> List[Dict[str, Any]]:
    """
    Returns a list of policy payload of both polarity IS and IS NOT policies

    :return: List of policy payload
    """
    return [CREATE_AUTH0_POLICY_POLARITY_IS, CREATE_AUTH0_POLICY_POLARITY_NOT]


@pytest.fixture(scope="module")
def service_type() -> str:
    """
    Returns the service type for the fixture
    :return: str
    """
    return ServiceTypes.auth0


@pytest.mark.xray("AAF-10031")
@pytest.mark.auth0
def test_trigger_policy_scan_for_auth0(
    tenant: OmniAPIClient,
    get_or_create_polarity_policy_ids,
    add_monitored_service_to_policy,
):
    """
    Verify that the comprehensive policy scan can be triggered

    :param tenant: The API client to execute queries. Pre-configured for the target tenant
    :param get_or_create_polarity_policy_ids: Fixture to get polarity type mapped with its policy ID
    :param add_monitored_service_to_policy: ensure the setup is correct to trigger a scan

    :return: None
    """
    check_trigger_policy_scan(tenant, get_or_create_polarity_policy_ids)
