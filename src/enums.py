from enum import Enum
from typing import List, Any, Literal


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


class Environments(StringEnum):
    """
    Environments
    """

    int_smoke = "INT-SMOKE"
    prod_smoke = "PROD-SMOKE"
    int_core = "INT-CORE"
    prod_core = "PROD-CORE"
    prod_eu = "PROD-EU"
    int_omnitab = "INT-OMNITAB"
    int_slack = "INT-SLACK"
    prod_us2 = "PROD-US2"
    prod_aus1 = "PROD-AUS1"
    int_msftdev = "INT-MSFTDEV"


class TestEnvironments(StringEnum):
    """
    XRAY Environments
    """

    int_smoke = "INT-Smoke"
    prod_smoke = "PROD-Smoke"
    int_core = "INT-Coretest"
    prod_core = "US1-Coretest"
    prod_us2 = "US2-Coretest"
    prod_eu = "EU1-Coretest"
    prod_aus1 = "AUS1-Coretest"


class ServiceTypes(StringEnum):
    anthropic: str = "anthropic"
    asana: str = "asana"
    auth0: str = "auth0"
    box: str = "box"
    classifications: str = "classifications"
    confluence: str = "confluence"
    core: str = "core"
    custom: str = "custom"
    crowdstrike: str = "crowdstrike"
    databricks: str = "databricks"
    docusign: str = "docusign"
    duo: str = "duo"
    fastly: str = "fastly"
    github: str = "github"
    gitlab: str = "gitlab"
    gsuite: str = "gsuite"
    hubspot: str = "hubspot"
    imanage: str = "imanage"
    jamf: str = "jamf"
    jira: str = "jira"
    jiraworkflow: str = "jiraworkflow"
    jumpcloud: str = "jumpcloud"
    integrations: str = "integrations"
    lucid: str = "lucid"
    miro: str = "miro"
    monday: str = "monday"
    mongo: str = "mongo"
    netsuite: str = "netsuite"
    notion: str = "notion"
    okta: str = "okta"
    o365: str = "o365"
    onelogin: str = "onelogin"
    openai: str = "openai"
    ping: str = "ping"
    sapsf: str = "sapsf"
    sendgrid: str = "sendgrid"
    sfdc: str = "sfdc"
    sfmc: str = "sfmc"
    slack: str = "slack"
    smartsheet: str = "smartsheet"
    snow: str = "snow"
    snowflake: str = "snowflake"
    stripe: str = "stripe"
    tableau: str = "tableau"
    veevavault: str = "veevavault"
    webex: str = "webex"
    wiz: str = "wiz"
    workday: str = "workday"
    zendesk: str = "zendesk"
    zoom: str = "zoom"


class HumanServiceTypes(StringEnum):
    auth0: str = "Auth0"
    asana: str = "Asana"
    box: str = "Box"
    classifications: str = "Classifications"
    confluence: str = "Confluence"
    core: str = "core"
    crowdstrike: str = "CrowdStrike"
    databricks: str = "Databricks"
    duo: str = "Duo"
    fastly: str = "Fastly"
    github: str = "GitHub"
    gsuite: str = "Google Workspace"
    hubspot: str = "Hubspot"
    imanage: str = "imanage"
    jamf: str = "Jamf"
    jira: str = "Jira"
    jumpcloud: str = "JumpCloud"
    lucid: str = "Lucid"
    monday: str = "Monday"
    mongo: str = "Mongo"
    netsuite: str = "NetSuite"
    notion: str = "Notion"
    okta: str = "Okta"
    o365: str = "Microsoft 365"
    ping: str = "Ping"
    sapsf: str = "SAP SuccessFactors"
    sfdc: str = "Salesforce"
    sfmc: str = "Salesforce Marketing Cloud"
    slack: str = "Slack"
    snow: str = "ServiceNow"
    snowflake: str = "Snowflake"
    sendgrid: str = "SendGrid"
    tableau: str = "Tableau"
    workday: str = "Workday"
    webex: str = "Webex"
    zendesk: str = "Zendesk"
    zoom: str = "Zoom"


class ComplianceTypes(StringEnum):
    fedramp: str = "fedramp"
    iso_27001: str = "iso_27001"
    nist_80053: str = "nist_80053"
    nist_csf: str = "nist_csf"
    nist_csf_cadence: str = "nist_csf_cadence"
    nist_80053_rev4: str = "nist_80053_rev4"
    nist_80053_rev5: str = "nist_80053_rev5"
    soc2: str = "soc2"
    soc2_cadence: str = "soc2_cadence"
    sox: str = "sox"


class ReportTypes(StringEnum):
    json: str = "json"
    xlsx: str = "xlsx"
    csv: str = "csv"
    pdf: str = "pdf"


class ReportPrettyNames(StringEnum):
    setup_changes_by_type_report: str = "Setup Changes by Type Report"
    salesforce_new_user_access: str = "Salesforce New User Access"
    sfdc_org_comparison_report: str = "SFDC Org Posture Comparison Report"
    findings_export_report: str = "All Findings Export Report"
    occurrence_export_report: str = "Finding Occurrence Export Report"


class InsightStatus(StringEnum):
    open: str = "open"
    dismissed: str = "dismissed"
    inherited: str = "inherited"
    resolved: str = "resolved"
    closed: str = "closed"


class InsightLevel(StringEnum):
    di: str = "insight"
    dii: str = "thread"
    diio: str = "occurrence"


class EventType(StringEnum):
    """
    Used with the pipeline tests
    """

    login: str = "login"
    create_user: str = "create_user"


class EventStatus(StringEnum):
    """
    Used with the pipeline tests
    """

    failed: str = "failed"
    success: str = "success"


class Roles(StringEnum):
    """
    Used with the pipeline tests
    """

    admin: str = "administrator"


class PolicyRole(StringEnum):
    security: str = "security"
    functional: str = "functional"
    posture: str = "monitored_service_config"


class PostureExplorerUserFilter(StringEnum):
    internal: str = "is_internal_user"
    active: str = "active"
    admin: str = "has_admin_perms"
    elevated_perm: str = "has_elevated_perms"


class OmnitabReportNames(StringEnum):
    assessment_summary: str = "LastDataAssessmentSummary"
    ms_sync: str = "MSDataSyncStatus"
    service_now_sync: str = "SNDataJobForMSStatus"
    ms_not_ingested: str = "CustomerServicesNotIngested"
    ms_errors_and_warnings = "MSErrorsAndWarnings"


class HumanThirdPartyAppsFilter(StringEnum):
    monitored_service: str = "Monitored Service"
    service_type: str = "Service Type"
    publisher: str = "Publisher"
    first_seen: str = "First Seen"
    last_seen: str = "Last Seen"
    scope_risk: str = "Scope Criticality"
    environment: str = "Environment"
    oauth_tokens: str = "OAuth Tokens"
    oauth_client: str = "OAuth Client"
    internal_app: str = "Internal App"
    bot_only_app: str = "Bot-Only App"
    approved_at: str = "Approved At"
    approved_by: str = "Approved By"


class ThirdPartyAppsFilter(StringEnum):
    monitored_service: str = "monitored_service__in"
    service_type: str = "service_type__in"
    publisher: str = "publisher_name__in"
    first_seen_from: str = "created__gte"
    first_seen_to: str = "created__lte"
    last_seen_from: str = "last_seen_in_use__gte"
    last_seen_to: str = "last_seen_in_use__lte"
    scope_risk: str = "highest_risk_scope_score__ranges"
    environment: str = "monitored_service__tags__in"
    oauth_tokens: str = "has_oauth_tokens"
    oauth_client: str = "oauth_client_seen"
    internal_app: str = "is_internal_app"
    bot_only_app: str = "is_only_bot_user_integration"
    approved_at_from: str = "approved_at__gte"
    approved_at_to: str = "approved_at__lte"
    approved_by_user: str = "approved_by__in"
    approved_by_auto: str = "auto_approved_app"


class InsightsFilter(StringEnum):
    monitored_service__in: str = "monitored_service__in"
    service_type__in: str = "service_type__in"
    service_type: str = "service_type"
    monitored_service__tags__in: str = "monitored_service__tags__in"
    total_filtered_instance_data_count: str = "total_filtered_instance_data_count"
    last_seen: str = "last_seen"


class HumanThirdPartyAppsStats(StringEnum):
    num_apps_high_scopes: str = "Highly-privileged apps"
    new_apps_last_30_days: str = "New SaaS-to-SaaS apps"


class ThirdPartyAppsStats(StringEnum):
    num_apps_high_scopes: str = "num_apps_high_scopes"
    new_apps_last_30_days: str = "new_apps_last_30_days"
    new_unapproved_apps_last_30_days: str = "new_unapproved_apps_last_30_days"
    new_approved_apps_last_30_days: str = "new_approved_apps_last_30_days"
    num_unapproved_apps_high_scopes: str = "num_unapproved_apps_high_scopes"
    num_approved_apps_high_scopes: str = "num_approved_apps_high_scopes"


class InputTypes(StringEnum):
    checkbox: str = "checkbox"
    radio: str = "radio"


# disable black formatting for this enum
# it wants to add paretheses around some of the strings
# fmt: off
class WorkflowCSVHeaders(StringEnum):
    monitored_service_type: str = "Monitored Service Type"
    monitored_service_name: str = "Monitored Service Name"
    finding_type: str = "Finding Type"
    policy_name: str = "Policy Name"
    rule_name: str = "Rule Name"
    rule_description: str = "Rule Description"
    finding_status: str = "Finding Status",
    finding_created: str = "Finding Created",
    finding_last_activated: str = "Finding Last Activated",
    finding_risk_label: str = "Finding Risk Label",
    finding_risk_score: str = "Finding Risk Score",
    monitored_service_env_labels: str = "Monitored Service Environment Labels",
    role_usernames: str = "Role Usernames",
    classification_names: str = "Classification Names",
    monitored_service_id: str = "Monitored Service ID"
    policy_id: str = "Policy ID",
    rule_id: str = "Rule ID",
    finding_id: str = "Finding ID",
    target: str = "Target"
    target_detail: str = "Target Detail"
    observed_value: str = "Observed Value"
    reason: str = "Reason"
    compliant_value: str = "Compliant Value"
    violation_occurred_at: str = "Violation Occurred At"
    remediation_solution: str = "Remediation Solution"


# fmt: on


class SentinelValue(StringEnum):
    ao_null: str = "AO_NULL"
    ao_empty: str = "AO_EMPTY"
    ao_missing: str = "AO_MISSING"


class SentinelTranslation(StringEnum):
    ao_null: str = "<Null>"
    ao_empty: str = "<Empty>"
    ao_missing: str = "<Missing>"
    ao_empty_list: str = "[]"


class Polarity(StringEnum):
    must_not_be: str = "NOT"
    must_be: str = "IS"
    not_contain: str = "NCT"
    list_length_less_than: str = "LLLT"
    list_length_greater_than: str = "LLGT"


class ColumnMappings:
    NAME: dict = {"Name": "name"}
    USERNAME: dict = {"Username": "username"}
    NAME_USERNAME: dict = {**NAME, **USERNAME}
    NAME_DESCRIPTION: dict = {**NAME, "Description": "description"}
    ASSIGNED_USERS: dict = {**NAME_USERNAME, "User Type": "user_type"}
    SETTING_VALUE: dict = {"Setting": "setting", "Value": "current_value"}
    SYSTEM_SETTINGS: dict = {
        **SETTING_VALUE,
        "Criticality": "criticality",
        "Category": "category_label",
    }


class KnownProductionDomains(StringEnum):
    coretest_us1 = "https://coretest.appomni.com/"
    coretest_us2 = "https://coretest-us2.appomni.com/"
    coretest_us3 = "https://coretest-us3.appomni.com/"
    coretest_aus1 = "https://coretest-aus1.appomni.com/"
    coretest_eu1 = "https://coretest-eu1.appomni.com/"


class KnownIntegrationDomains(StringEnum):
    integration_coretest = "https://coretest.int.appomni.com/"
    integration_smoketest = "https://smoketest.int.appomni.com/"


InsightStatusT = Literal["open", "dismissed", "resolved"]


class RuleTypeName(StringEnum):
    PRIMARY_RBAC: str = "config.primary_rbac.assignment"
    SECONDARY_RBAC: str = "config.secondary_rbac.assignment"
    OTHER_RBAC: str = "config.other_rbac.assignment"
    SYSTEM_RBAC: str = "config.org.sys_setting"
    PRIMARY_RBAC_NEW: str = "config.primary_rbac.new"
    SECONDARY_RBAC_NEW: str = "config.secondary_rbac.new"
    OTHER_RBAC_NEW: str = "config.other_rbac.new"
    USER_PERM_ACCESS: str = "config.user.perm_access"
    PRIMARY_RBAC_PERM_ACCESS: str = "config.primary_rbac.perm_access"
    SECONDARY_RBAC_PERM_ACCESS: str = "config.secondary_rbac.perm_access"
    GROUP_NEW: str = "config.group.new"
    GROUP_ASSIGNMENT: str = "config.group.assignment"


class Operations(StringEnum):
    contains: str = "__contains__"
    equals: str = "__eq__"
    not_equals: str = "__ne__"


class PolicyModes(StringEnum):
    whitelist: str = "whitelist"
    blacklist: str = "blacklist"


class ConnectionAuthTypes(StringEnum):
    basic: str = "Basic"
    oauth2: str = "OAuth2"


class TagTypes(StringEnum):
    Environment: str = "environment"
    Generic: str = "generic"
    Impact: str = "impact"
    Trust: str = "trust"
    DetectionAttribute: str = "detection_attribute"
    Outcome: str = "outcome"
    Compliance: str = "compliance"


class Actions(StringEnum):
    Creating: str = "Creating"
    Deleting: str = "Deleting"
    Fetching: str = "Fetching"
    Updating: str = "Updating"


class RiskLevel(Enum):
    critical = ("critical", "Critical")
    high = ("high", "High")
    medium = ("medium", "Medium")
    low = ("low", "Low")
    informational = ("informational", "Informational")

    def __init__(self, machine_value: str, human_value: str):
        self._value_ = machine_value
        self.human_value = human_value

    @classmethod
    def machine_values(cls) -> set[str]:
        return {level.value for level in cls}

    @classmethod
    def human_values(cls) -> set[str]:
        return {level.human_value for level in cls}

    @classmethod
    def from_score(cls, score: int | None) -> "RiskLevel":
        if score is None:
            return cls.informational
        if score == 0:
            return cls.informational
        if 1 <= score <= 25:
            return cls.low
        if 26 <= score <= 50:
            return cls.medium
        if 51 <= score <= 75:
            return cls.high
        return cls.critical
