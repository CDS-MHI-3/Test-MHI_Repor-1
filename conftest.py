# conftest.py
import http
import logging

import definitions
import os
import pytest


from src.api.v1.omniapiclient import OmniAPIClient
from src.tenants.config import TenantConfig

LOGGER = logging.getLogger(__name__)

# register assertion rewrites is utilities that need it
pytest.register_assert_rewrite("src.tools.api_utils")


# register assertion rewrites is utilities that need it
def pytest_sessionstart(session):
    config = TenantConfig(os.getenv("OMNI_ENV"))
    session.results = dict()
    print(f"Running tests for [{os.getenv('OMNI_ENV')}]")
    print(f"Config: {config}")

    healthcheck(config)

    if not os.path.exists(definitions.LOGS_DIR):
        os.mkdir(definitions.LOGS_DIR)
    if not os.path.exists(definitions.REPORTS_RESULTS_DIR):
        os.mkdir(definitions.REPORTS_RESULTS_DIR)
    if not os.path.exists(definitions.XRAY_RESULTS_DIR):
        os.mkdir(definitions.XRAY_RESULTS_DIR)
    if not os.path.exists(definitions.XRAY_MARKER_MIGRATION_DIR):
        os.mkdir(definitions.XRAY_MARKER_MIGRATION_DIR)


# Test Fixtures
@pytest.fixture(scope="session")
def tenant_config():
    return TenantConfig(os.getenv("OMNI_ENV"))


@pytest.fixture(scope="session")
def tenant(tenant_config: TenantConfig) -> OmniAPIClient:
    """
    OmniConnector Session for the current logged in tenant

    :return: Omni Connector Session for making requests for the current tenant
    """

    api_client = OmniAPIClient(
        tenant_config.base_url, verify_ssl=tenant_config.verify_ssl
    )

    api_client.user_login(tenant_config.username, tenant_config.password)
    return api_client


def healthcheck(config: TenantConfig):
    if not config.verify_ssl:
        print("Skipping healthcheck due to SSL verification being disabled")
        return
    api_client = OmniAPIClient(config.base_url, verify_ssl=True)
    # Adding a forward slash after the healthcheck as per comment in KAL-504
    response = api_client.get("healthcheck/", allow_redirects=True)
    if response.text != "OK" or response.status_code != http.HTTPStatus.OK:
        pytest.fail(
            f"Stopping tests. Healthcheck failed for {config.base_url}, {response.text}"
        )
    else:
        print(f"Healthcheck passed {config.base_url} {response}")
