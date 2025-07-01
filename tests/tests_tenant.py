from http import HTTPStatus
from src.api.v1.omniapiclient import OmniAPIClient


def check_tenant_got_connected_succesfully(tenant: OmniAPIClient):
    response = tenant.get("api/v1/core/environment/session/")
    assert response.status_code == HTTPStatus.OK


def test_tenant(tenant: OmniAPIClient):
    check_tenant_got_connected_succesfully(tenant=tenant)


def test_coretest(coretest_tenant: OmniAPIClient):
    check_tenant_got_connected_succesfully(tenant=coretest_tenant)


def test_smoketest(smoketest_tenant: OmniAPIClient):
    check_tenant_got_connected_succesfully(tenant=smoketest_tenant)


def test_msft_tenant(msft_tenant: OmniAPIClient):
    check_tenant_got_connected_succesfully(tenant=msft_tenant)


def test_slack_tenant(slack_tenant: OmniAPIClient):
    check_tenant_got_connected_succesfully(tenant=slack_tenant)
