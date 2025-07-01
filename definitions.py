from pathlib import Path

ROOT_DIR = Path(__file__).parent

LOGS_DIR = ROOT_DIR / "logs"
CONFIG_DIR = ROOT_DIR / "config"
UI_SCREENSHOTS = LOGS_DIR / "UI_screenshots"
AUTH_JSON = LOGS_DIR / "authenticated.json"
REPORTS_DOWNLOADED_DIR = LOGS_DIR / "reports_downloaded"
REPORTS_RESULTS_DIR = LOGS_DIR / "reports_results"
REPORTS_COMPLIANCE_MAPPING_DIR = ROOT_DIR / "src/reports/compliance_mappings"
REPORTS_INDEXES = ROOT_DIR / "src/reports/indexes"
PERSONAL_CONFIG = ROOT_DIR / "src/tenants_config/personal_tenants.py"
DATA_MOCKS = ROOT_DIR / "src/data/"
POLICY_CREATOR_DATA_DIR = ROOT_DIR / "src/tools/policy_creator/data"
PIPELINE_TEST_DATA_DIR = DATA_MOCKS / "pipeline"
SCHEMAS_DIR = ROOT_DIR / "src/data/schemas/"
TESTMAIL_NAMESPACE = "6fgfj"
TEST_EMAIL = "6fgfj.otrp@inbox.testmail.app"
TEST_RG_EMAIL = "6fgfj.otr-RG@inbox.testmail.app"
XRAY_RESULTS_DIR = LOGS_DIR / "xray"
XRAY_MARKER_MIGRATION_DIR = LOGS_DIR / "xray_marker_migration"
