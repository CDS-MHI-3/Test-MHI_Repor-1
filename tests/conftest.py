import os
import pytest

from src.api.v1.omniapiclient import OmniAPIClient
from src.tenants.config import TenantConfig

from tests.helper import get_tenant_from_config

"""
Coretest Tenant
"""


@pytest.fixture(scope="session")
def tenant_config_coretest():
    config = TenantConfig()
    config.base_url = "https://coretest.int.appomni.com/"
    config.username = "coretest@appomni.com"
    config.password = os.getenv("INT_CORE_PW")
    if config.password is None:
        raise ValueError("INT_CORE_PW environment variable is not set.")
    return config


@pytest.fixture(scope="session")
def coretest_tenant(tenant_config_coretest) -> OmniAPIClient:
    """
    OmniConnector Session for the current logged in tenant.

    :return: Omni Connector Session for making requests for the current tenant.
    """
    return get_tenant_from_config(tenant_config_coretest)


@pytest.fixture(scope="session")
def tenant_config_msftdev():
    config = TenantConfig()
    config.base_url = "https://msftagentdev.int.appomni.com/"
    config.username = "omni-test-connections"
    config.password = os.getenv("INT_MSFTDEV_PW")
    if config.password is None:
        raise ValueError("INT_MSFTDEV_PW environment variable is not set.")
    return config


@pytest.fixture(scope="session")
def msft_tenant(tenant_config_msftdev) -> OmniAPIClient:
    """
    OmniConnector Session for the current logged in tenant.

    :return: Omni Connector Session for making requests for the current tenant.
    """
    return get_tenant_from_config(tenant_config_msftdev)


"""
Slack Tenant
"""


@pytest.fixture(scope="session")
def tenant_config_slackdev():
    config = TenantConfig()
    config.base_url = "https://slackdev.int.appomni.com/"
    config.username = "omni-test-reports"
    config.password = os.getenv("INT_SLACK_PW")
    if config.password is None:
        raise ValueError("INT_SLACK_PW environment variable is not set.")
    return config


@pytest.fixture(scope="session")
def slack_tenant(tenant_config_slackdev) -> OmniAPIClient:
    """
    OmniConnector Session for the current logged in tenant.

    :return: Omni Connector Session for making requests for the current tenant.
    """
    return get_tenant_from_config(tenant_config_slackdev)


"""
Smoketest Tenant
"""


@pytest.fixture(scope="session")
def tenant_config_smoketest():
    config = TenantConfig()
    config.base_url = "https://smoketest.int.appomni.com/"
    config.username = "omni-test-pipeline"
    config.password = os.getenv("INT_SMOKE_PIPELINE_PW")
    if config.password is None:
        raise ValueError("INT_SMOKE_PIPELINE_PW environment variable is not set.")
    return config


@pytest.fixture(scope="session")
def smoketest_tenant(tenant_config_smoketest) -> OmniAPIClient:
    """
    OmniConnector Session for the current logged in tenant.

    :return: Omni Connector Session for making requests for the current tenant.
    """
    return get_tenant_from_config(tenant_config_smoketest)
