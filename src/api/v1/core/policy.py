from src.api.base_api import BaseAPI

from src.api.mixins.searchable_mixin import SearchableMixin


class Policy(BaseAPI, SearchableMixin):  # SearchableMixin
    base_path = "api/v1/core/policy/"

    @classmethod
    def baseline_policy(cls, service_type: str):
        return (
            cls.base_path
            + f"?limit=1&offset=0&baseline_policy_for_tenant=true&policy_type={service_type}"
        )

    @classmethod
    def rule_options(cls, policy_id: int):
        return cls.base_path + f"{policy_id}/new_rule_options/"

    @classmethod
    def check_ctp_done(cls, policy_id: int):
        return cls.base_path + f"{policy_id}/check_ctp_done/"

    @classmethod
    def get_single_item_url(cls, item_id: str | int) -> str:
        """
        Return URL for fetching a single item. accepting both string and integer as item_id
        """
        return f"{cls.base_path}{item_id}/"


# class PolicyNewPattern(BaseAPI, SingleItemMixin, SearchableMixin):
#     """
#     The new pattern before deprecating the `Policy` class. Once the new pattern is fully adopted,
#     `Policy` will be deprecated, and this class will be renamed to `Policy`.
#     """

#     base_path = "api/v1/core/policy/"
