import os
import ast
from dotenv import load_dotenv
from src.enums import KnownIntegrationDomains, KnownProductionDomains

import definitions

"""
Used to store connection configuration for different AO Tenants
"""


class TenantConfig:
    def __init__(self, environment=None, config_path=definitions.CONFIG_DIR) -> None:
        """
        Initialize TenantConfig with the name of the environment and optional path to the configuration directory.

        :param environment: Name of the environment (e.g., 'integration.coretest', 'production.coretest'). The naming convention is
        'environment_name.tenant_name'. If environment is not specified, the .env file will be loaded, and it's assumed the necessary
        environment variables are already set.
        :param config_path: Path to the directory containing .env files. Defaults to 'config'.
        """
        if environment:
            # Construct the path to the specific .env file based on the environment name
            env_file_name = f".env.{environment}"
            env_path = os.path.join(config_path, env_file_name)
            self.environment = environment
            # Load the .env file if it exists
            if os.path.exists(env_path):
                load_dotenv(dotenv_path=env_path)
            else:
                raise FileNotFoundError(
                    f"No configuration file found for the specified environment: {env_path}"
                )
        # Required environment variables
        self.base_url = self._load_env_var("AO_BASE_URL")
        self.username = self._load_env_var("AO_USERNAME")
        self.password = self._load_env_var("AO_PASSWORD")
        # Optional environment variables
        self.admin_email = os.getenv("ADMIN_EMAIL")
        self.org_key = os.getenv("ORG_KEY")
        self.preferred_monitored_services = ast.literal_eval(
            os.getenv("PREFERRED_MONITORED_SERVICES")
        )
        # True must be a string so eval does not fail. Circle CI passes value as a string.
        self.verify_ssl = eval(os.getenv("VERIFY_SSL", "True"))

    def __str__(self) -> str:
        return f"TenantConfig(base_url:{self.base_url}, username:{self.username}, password:********, admin_email:{self.admin_email}, org_key:{self.org_key}, preferred_monitored_services:{self.preferred_monitored_services}, verify_ssl:{self.verify_ssl})"

    def get_name_of_integration_environment(self) -> str:
        if self.base_url in KnownIntegrationDomains.values():
            return self.base_url.split("//")[1].split(".")[0]
        else:
            return ""

    def get_name_of_production_environment(self) -> str:
        if self.base_url in KnownProductionDomains.values():
            return self.base_url.split("//")[1].split(".")[0]
        else:
            return ""

    def _load_env_var(self, env_var_name: str) -> str:
        env_var = os.environ.get(env_var_name, None)
        if not env_var:
            raise ValueError(f"Environment variable {env_var_name} not set")
        return env_var
