"""
Confluence Posture Policy rule test: Verify that posture policy rules can be
created and applied to Confluence monitored services.
"""

import pytest

from src.enums import ServiceTypes
from typing import Dict, Any, List
from src.api.v1.omniapiclient import OmniAPIClient
from tests.app_factory.policies.policy_helpers import (
    check_trigger_policy_scan,
    create_policy_payload,
)

SERVICE_TYPE = ServiceTypes.confluence

CREATE_CONFLUENCE_POLICY_POLARITY_IS: Dict[str, Any] = create_policy_payload(
    policy_name="omni-test-united-confluence-scp-comprehensive_IS",
    service_type=SERVICE_TYPE,
)

CREATE_CONFLUENCE_POLICY_POLARITY_NOT: Dict[str, Any] = create_policy_payload(
    policy_name="omni-test-united-confluence-scp-comprehensive_NOT",
    service_type=SERVICE_TYPE,
)

pytestmark = [pytest.mark.service_type(SERVICE_TYPE)]


@pytest.fixture(scope="module")
def list_all_policy_polarity_payload() -> List[Dict[str, Any]]:
    """
    Returns a list of policy payload of both polarity IS and IS NOT policies

    :return: List of policy payload
    """
    return [CREATE_CONFLUENCE_POLICY_POLARITY_IS, CREATE_CONFLUENCE_POLICY_POLARITY_NOT]


@pytest.fixture(scope="module")
def service_type() -> str:
    """
    Returns the service type for the fixture
    :return: str
    """
    return ServiceTypes.confluence


@pytest.mark.xray("AAF-3752")
@pytest.mark.confluence
def test_trigger_policy_scan_for_confluence(
    tenant: OmniAPIClient,
    get_or_create_polarity_policy_ids,
    add_monitored_service_to_policy,
):
    """
    Verify that the comprehensive policy scan can be triggered

    :param tenant: connector
    :param get_or_create_polarity_policy_ids: Fixture to get polarity type mapped with its policy ID
    :param add_monitored_service_to_policy: ensure the setup is correct to trigger a scan

    :return: None
    """

    check_trigger_policy_scan(tenant, get_or_create_polarity_policy_ids)
