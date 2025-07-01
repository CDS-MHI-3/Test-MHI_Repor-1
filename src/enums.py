from enum import Enum
from typing import List, Any


class StringEnum(str, Enum):
    @classmethod
    def names(cls) -> List[str]:
        """
        Return names for all values - for comparing names between matched enums
        """
        return list(cls.__members__.keys())

    @classmethod
    def values(cls) -> List[str]:
        """
        Return values for all members - for testing validity without exception
        """
        return [x for x in cls]

    def __eq__(self, other: Any) -> bool:
        """
        Allow comparison by type or value

        Notes:
            * Enum provides a hash dunder suitable to our needs
            * Python provides a ne dunder suitable to our needs
        """
        if type(other) is self.__class__:
            return self.name == other.name
        return str(self.value) == str(other)

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        """
        Make our value the standard representation.
        Allows string var assignment

        """
        return self.value


class KnownProductionDomains(StringEnum):
    coretest_us1 = "https://coretest.appomni.com/"
    coretest_us2 = "https://coretest-us2.appomni.com/"
    coretest_us3 = "https://coretest-us3.appomni.com/"
    coretest_aus1 = "https://coretest-aus1.appomni.com/"
    coretest_eu1 = "https://coretest-eu1.appomni.com/"


class KnownIntegrationDomains(StringEnum):
    integration_coretest = "https://coretest.int.appomni.com/"
    integration_smoketest = "https://smoketest.int.appomni.com/"
