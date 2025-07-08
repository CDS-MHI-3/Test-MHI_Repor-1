from abc import ABC, abstractmethod


class BaseAPI(ABC):
    """
    Abstract base class for API functionality.
    """

    @property
    @abstractmethod
    def base_path(self) -> str:
        """
        This property must be implemented by all subclasses to define the base path; e.g. `api/v1/core/monitoredservice/`
        """
        pass
