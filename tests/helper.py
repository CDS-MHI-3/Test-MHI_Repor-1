from src.api.v1.omniapiclient import OmniAPIClient


def get_tenant_from_config(tenant_config) -> OmniAPIClient:
    """
    OmniConnector Session for the logged in tenant.

    :return: Omni Connector Session for making requests for the current tenant.
    """
    api_client = OmniAPIClient(tenant_config.base_url)
    api_client.user_login(tenant_config.username, tenant_config.password)
    return api_client
