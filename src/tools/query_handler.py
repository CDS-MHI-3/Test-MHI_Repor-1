import logging
from typing import Dict
from urllib.parse import parse_qs


class QueryParameterHandler:
    """
    A helper class responsible for managing query parameters, including merging default parameters and handling query parameter inputs.
    """

    logger = logging.getLogger(__name__)

    def __init__(
        self, mixin_defaults: Dict | None = None, class_defaults: Dict | None = None
    ):
        """

        :param default_params: Default query parameters provided by the mixin.
        :param class_defaults: Optional additional default parameters from the specific class.
        """
        self.mixin_defaults = mixin_defaults or {}
        self.logger.debug(f"\t\t{self.__class__} default parameters: {mixin_defaults}")
        self.class_defaults = class_defaults or {}
        self.logger.debug(
            f"\t\t{self.__class__} class default parameters: {class_defaults}"
        )

    def merge_query_parameters(self, skip_defaults: bool = False) -> Dict:
        """
        Merges the default parameters from the mixin and the class, unless skip_defaults is True.

        :param skip_defaults: If True, only merge the provided query parameters.
        :return: Merged dictionary of query parameters.
        """
        if skip_defaults:
            return {}
        merged_params = self.mixin_defaults.copy()
        merged_params.update(self.class_defaults)
        return merged_params

    def build_query(
        self,
        base_params: Dict | None = None,
        query_params: str | Dict | None = None,
        skip_defaults: bool = False,
    ) -> Dict:
        """
        Builds a query dictionary by merging base parameters, additional query parameters, and optional default parameters.

        :param base_params: The class-specific base parameters, like a default status.
        :param query_params: Additional query parameters provided by the caller.
        :param skip_defaults: If True, don't merge default parameters.
        :return: Merged dictionary containing the query parameters.
        """
        query_dict = self.merge_query_parameters(skip_defaults=skip_defaults)

        # Merge base parameters
        if base_params:
            if not isinstance(base_params, dict):
                raise TypeError(
                    f"Expected base_params to be a dict, got {type(base_params).__name__}"
                )
            query_dict.update(base_params)

        # Merge additional query parameters
        if isinstance(query_params, dict):
            query_dict.update(query_params)
        elif isinstance(query_params, str):
            query_dict.update(self._parse_query_string(query_params))
        elif query_params is not None:
            raise ValueError(
                f"query_params must be a dict or a str, got {type(query_params).__name__}"
            )

        return query_dict

    @staticmethod
    def _parse_query_string(query_string: str) -> Dict:
        """
        Parses a query string into a dictionary.

        :param query_string: A URL-encoded query string.
        :return: Dictionary of parsed query parameters.
        """
        parsed_params = parse_qs(query_string)
        return {k: v[0] if len(v) == 1 else v for k, v in parsed_params.items()}
