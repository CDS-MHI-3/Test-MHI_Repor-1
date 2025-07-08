import logging
from typing import Dict, Any
import json
from urllib.parse import urlencode
from functools import singledispatch


from src.api.base_api import BaseAPI

from src.tools.query_handler import QueryParameterHandler


@singledispatch
def _jsonify_pre_urlencode(obj):
    return json.dumps(obj)


def ao_urlencode(params: Dict[str, Any]) -> str:
    """
    Handle urllib's conversion of `"` 's to "'"

    :param params: Query parameters as a dict
    :return: url encoded query parameters as a string
    """
    return urlencode({k: _jsonify_pre_urlencode(v) for k, v in params.items()})


class SearchableMixin:
    """
    Mixin for search functionality. Use this for endpoints that allow searching with query strings;
        e.g. GET Insights that are open and from Service Type Salesforce
    """

    logger = logging.getLogger(__name__)

    default_query_parameters = {
        "limit": 100,
        "offset": 0,
    }

    @classmethod
    def search(
        cls,
        query_params: str | Dict | None = None,
        base_params: Dict | None = None,
        default_params_only: bool = False,
        skip_default_params: bool = False,
        base_path_override: str | None = "",
    ) -> str:
        """
        Return URL for searching items.

        :param query_params: Additional query parameters provided by the caller.
        :param base_params: Base parameters for the query.
        :param default_params_only: If True, return only the query parameters provided.
        :param skip_default_params: If True, exclude default query parameters from the final query.
        :param base_path_override: Extra field to add in the base path for the search and default is empty.
            example : basepath: /api/v1/integrations/externalticketing/ticketingtemplate/
                and base_path_override: possible_assignment_for_field/ to make
                url :api/v1/integrations/externalticketing/ticketingtemplate/possible_assignment_for_field
        :return: URL for searching items.
        """
        cls.logger.info(f"\tEntering search in {cls.__name__}")

        # Ensure the class inherits from BaseAPI
        if not issubclass(cls, BaseAPI):
            raise TypeError(
                f"{cls.__name__} must inherit from BaseAPI to use SearchableMixin"
            )

        # Initialize the QueryParameterHandler
        query_handler = QueryParameterHandler(
            mixin_defaults=SearchableMixin.default_query_parameters,  # Pass mixin-level default parameters
            class_defaults=getattr(cls, "default_query_parameters", {}),
        )

        # Build the final query parameters using the handler
        final_query_params = query_handler.build_query(
            base_params=base_params,
            query_params=query_params,
            skip_defaults=skip_default_params,
        )

        # Generate the query string
        query_string = ao_urlencode(final_query_params)
        cls.logger.info(f"\tFinal query string in {cls.__name__}: {query_string}")

        # Return the full search URL
        return f"{cls.base_path}{base_path_override}?{query_string}"
