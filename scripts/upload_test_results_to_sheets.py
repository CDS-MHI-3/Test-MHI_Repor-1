"""
Upload pytest test results to Google Sheets
Reads from pytest-json-report output and creates/updates a Google Sheet
"""

import os
import json
import argparse
from datetime import datetime, timezone
import sys
from typing import Dict, List, Any
import base64

try:
    import gspread
    from google.oauth2.service_account import Credentials
except ImportError:
    print("Required packages not installed. Run: pip install gspread google-auth")
    sys.exit(1)


class TestResultsUploader:
    def __init__(self, service_account_key: str, spreadsheet_id: str):
        """
        Initialize the uploader with Google Sheets credentials
        
        Args:
            service_account_key: Path to JSON file or base64-encoded JSON string
            spreadsheet_id: Google Sheets spreadsheet ID
        """
        self.spreadsheet_id = spreadsheet_id
        self.client = self._authenticate(service_account_key)

    def _authenticate(self, service_account_key: str) -> gspread.Client:
        """Authenticate with Google Sheets API"""
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]

        try:
            # Step 1: Try file path
            if os.path.exists(service_account_key):
                with open(service_account_key, 'r') as f:
                    creds_dict = json.load(f)
                print("[INFO] Authenticated using service account file")
            else:
                # Step 2: Try to base64-decode
                try:
                    decoded = base64.b64decode(service_account_key).decode('utf-8')
                    creds_dict = json.loads(decoded)
                    print("[INFO] Authenticated using base64-encoded service account key")
                except Exception as e:
                    print("[ERROR] Invalid service account key. Provide a valid file path or base64-encoded string.")
                    raise e

            creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
            return gspread.authorize(creds)

        except Exception as e:
            print(f"[ERROR] Authentication failed: {e}")
            sys.exit(1)

    def parse_test_results(self, json_file_path: str) -> Dict[str, Any]:
        """Parse pytest JSON report"""
        try:
            with open(json_file_path, 'r') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"[ERROR] Parsing test results: {e}")
            sys.exit(1)

    def format_results_for_sheets(self, test_data: Dict[str, Any], 
                                  environment: str, 
                                  job_name: str,
                                  build_url: str = "") -> List[List[str]]:
        """Format test results for Google Sheets"""

        summary = test_data.get('summary', {})
        total = summary.get('total', 0)
        passed = summary.get('passed', 0)
        failed = summary.get('failed', 0)
        skipped = summary.get('skipped', 0)
        error = summary.get('error', 0)
        pass_rate = (passed / total * 100) if total > 0 else 0
        created = test_data.get('created', datetime.now(timezone.utc).isoformat())
        duration = test_data.get('duration', 0)

        if isinstance(created, (int, float)):
            timestamp = datetime.fromtimestamp(created, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        else:
            timestamp = datetime.fromisoformat(created.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S UTC')

        rows = []

        summary_row = [
            timestamp, environment, job_name, "ALL TESTS",
            str(total), str(passed), str(failed), str(skipped), str(error),
            f"{pass_rate:.1f}%", f"{duration:.2f}s", build_url,
            "SUMMARY", "", "", "", "", ""
        ]
        rows.append(summary_row)

        tests = test_data.get('tests', [])
        for test in tests:
            if test.get('outcome') not in ['failed', 'error', 'skipped']:
                continue

            failure_message = ""
            if test.get('outcome') == 'failed':
                call_info = test.get('call', {})
                crash_info = call_info.get('crash', {})
                failure_message = crash_info.get('message', '')

                if not failure_message:
                    longrepr = call_info.get('longrepr', '')
                    if longrepr:
                        lines = longrepr.split('\n')
                        for line in lines:
                            if line.strip().startswith('E   '):
                                failure_message = line.strip()[4:]
                                break
                        if not failure_message and lines:
                            failure_message = lines[0][:200] + '...' if len(lines[0]) > 200 else lines[0]

            skip_reason = ""
            if test.get('outcome') == 'skipped':
                call_info = test.get('call', {})
                longrepr = call_info.get('longrepr', '')
                if longrepr:
                    if isinstance(longrepr, tuple) and len(longrepr) > 2:
                        skip_reason = longrepr[-1]
                    elif isinstance(longrepr, str):
                        skip_reason = longrepr
                    if skip_reason.startswith('Skipped: '):
                        skip_reason = skip_reason[9:]

            test_duration = 0
            for phase in ['setup', 'call', 'teardown']:
                test_duration += test.get(phase, {}).get('duration', 0)

            full_error = ""
            stack_trace = ""
            logs = ""
            error_location = ""

            if test.get('outcome') in ['failed', 'error']:
                phase_info = test.get('call', test.get('setup', test.get('teardown', {})))
                full_error = phase_info.get('longrepr', '')
                crash_info = phase_info.get('crash', {})
                if crash_info:
                    error_location = f"{crash_info.get('path', '')}:{crash_info.get('lineno', '')}"
                traceback = phase_info.get('traceback', [])
                if traceback:
                    stack_trace = "\n".join([
                        f"{entry.get('path', '')}:{entry.get('lineno', '')} - {entry.get('message', '')}"
                        for entry in traceback
                    ])
                log_entries = phase_info.get('log', [])
                if log_entries:
                    logs = "\n".join([f"{log.get('levelname', '')} - {log.get('msg', '')}" for log in log_entries])

            details = failure_message or skip_reason or ""

            test_row = [
                timestamp, environment, job_name, test.get('nodeid', ''),
                '1',
                '1' if test.get('outcome') == 'passed' else '0',
                '1' if test.get('outcome') == 'failed' else '0',
                '1' if test.get('outcome') == 'skipped' else '0',
                '1' if test.get('outcome') == 'error' else '0',
                '0.0%', f"{test_duration:.2f}s", build_url,
                test.get('outcome', 'unknown').upper(),
                details[:500] + '...' if len(details) > 500 else details,
                full_error[:1000] + '...' if len(full_error) > 1000 else full_error,
                stack_trace[:1000] + '...' if len(stack_trace) > 1000 else stack_trace,
                logs[:1000] + '...' if len(logs) > 1000 else logs,
                error_location
            ]
            rows.append(test_row)

        return rows

    def upload_to_sheets(self, data_rows: List[List[str]], worksheet_name: str = "Test Results"):
        """Upload data to Google Sheets"""
        try:
            spreadsheet = self.client.open_by_key(self.spreadsheet_id)
            try:
                worksheet = spreadsheet.worksheet(worksheet_name)
            except gspread.WorksheetNotFound:
                headers = [
                    'Timestamp', 'Environment', 'Job Name', 'Test Name', 'Total Tests', 
                    'Passed', 'Failed', 'Skipped', 'Errors', 'Pass Rate', 
                    'Duration', 'Build URL', 'Type', 'Details', 'Full Error', 
                    'Stack Trace', 'Logs', 'Error Location'
                ]
                worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=1000, cols=len(headers))
                worksheet.append_row(headers)

            if worksheet.row_count == 0 or not worksheet.get_all_values():
                headers = [
                    'Timestamp', 'Environment', 'Job Name', 'Test Name', 'Total Tests', 
                    'Passed', 'Failed', 'Skipped', 'Errors', 'Pass Rate', 
                    'Duration', 'Build URL', 'Type', 'Details', 'Full Error', 
                    'Stack Trace', 'Logs', 'Error Location'
                ]
                worksheet.append_row(headers)

            for row in data_rows:
                worksheet.append_row(row)

            print(f"Successfully uploaded {len(data_rows)} row(s) to Google Sheets")

        except Exception as e:
            print(f"[ERROR] Upload failed: {e}")
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Upload pytest results to Google Sheets')
    parser.add_argument('--json-file', required=True, help='Path to pytest JSON report file')
    parser.add_argument('--service-account-key', help='Path to service account JSON file or base64-encoded string')
    parser.add_argument('--spreadsheet-id', help='Google Sheets spreadsheet ID')
    parser.add_argument('--environment', default='unknown', help='Test environment')
    parser.add_argument('--job-name', default='unknown', help='CI job name')
    parser.add_argument('--build-url', default='', help='Build URL')
    parser.add_argument('--worksheet-name', default='Test Results', help='Worksheet name')

    args = parser.parse_args()

    service_account_key = args.service_account_key or os.environ.get('GOOGLE_SERVICE_ACCOUNT_KEY')
    spreadsheet_id = args.spreadsheet_id or os.environ.get('GOOGLE_SHEETS_ID')

    if not service_account_key:
        print("[ERROR] No service account key provided via --service-account-key or GOOGLE_SERVICE_ACCOUNT_KEY env var")
        sys.exit(1)

    if not spreadsheet_id:
        print("[ERROR] No spreadsheet ID provided via --spreadsheet-id or GOOGLE_SHEETS_ID env var")
        sys.exit(1)

    if not os.path.exists(args.json_file):
        print(f"[ERROR] JSON file not found: {args.json_file}")
        sys.exit(1)

    uploader = TestResultsUploader(service_account_key, spreadsheet_id)
    test_data = uploader.parse_test_results(args.json_file)

    data_rows = uploader.format_results_for_sheets(
        test_data, args.environment, args.job_name, args.build_url
    )

    worksheet_name = args.worksheet_name or datetime.now().strftime('%Y-%m-%d')
    uploader.upload_to_sheets(data_rows, worksheet_name)


if __name__ == '__main__':
    main()
