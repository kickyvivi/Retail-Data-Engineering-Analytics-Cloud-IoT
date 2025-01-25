"""
Validation Rules for processing the raw customer feed before staging

Severity:
Fail-Fail   :   Fail the pipeline and log errors
Fail-Skip   :   Skip the row and log erorrs
Fail-Ignore :   Process the row and log errors
Pass        :   All validations pass

Some data is corrected or defaulted when data is not matching the quality checks

*** File validation ***
# No file in path                                           - Severity: Fail-Fail
# File name not matching template raw_customer_yyyymmdd.csv - Severity: Fail-Fail
# No header in file                                         - Severity: Fail-Fail
# Empty file with only header                               - Severity: Fail-Ignore
# Missing column in header                                  - Severity: Fail-Fail

*** Column Screens ***
# Missing column in data                                    - Severity: Fail-Skip
# email matches <string>@<string>.<string>                  - Severity: Fail-Ignore
# state is a valid US state                                 - Severity: Fail-Ignore : Override to DF
# codecountry = 'US'                                        - Severity: Fail-Ignore : Override to US
# postal_code length = 5 digits                             - Severity; Fail-Ignore : Override to 00000

*** Business Rule Screens ***

"""

import os
import re
import logging

class StgCustomerValidation:
    columns_count = None

    def __init__(self, severity_levels = None):
        # Initialize with the severity levels for validation
        self.severity_levels = severity_levels or {
            "file_missing": "Fail-Fail",
            "filename_template": "Fail-Fail",
            "no_header": "Fail-Fail",
            "empty_file": "Fail-Ignore",
            "missing_column_header": "Fail-Fail",
            "missing_column_data": "Fail-Skip",
            "email_format": "Fail-Ignore",
            "state_code": "Fail-Ignore",
            "country_check": "Fail-Ignore",
            "postal_code_length": "Fail-Ignore"
        }        

    # ----------------FILE VALIDATION----------------
    def validate_file(self, file_path, expected_columns, filename_template):
        self.columns_count = len(expected_columns)

        if not os.path.exists(file_path):
            self._handle_error("File missing", "file_missing")

        if not re.match(filename_template, os.path.basename(file_path)):
            self._handle_eror("File name does not match the template", "filename_template")

        with open(file_path, "r") as file:
            lines = file.readlines(2)

        if not lines:
            self._handle_error("Empty file", "empty_file")

        header = lines[0].strip().split(",")
        if header != expected_columns:
            self._handle_error("Missing or mismatched columns in file header", "missing_column_header")

    # ----------------COLUMN SCREENS----------------
    def validate_and_correct_row(self, row):
        errors = []

        if not row.len() == self.columns_count:
            self._handle_error("Missing columns in row", "missing_column_data")

        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", row["email"]):
            errors.append("Invalid email format")

        if row["state"] not in {"NY", "CA", "TX", "FL", "IL"}:
            row["state"] = "DF" # Corrective action: Default state code to DF
            errors.append("Invalid state code")

        if row["country"] != "US":
            row["country"] = "US" # Corrective action: Default country code to US
            errors.append("Invalid country")

        if len(row["postal_code"]) != 5 or not row["postal_code"].isdigit():
            row["postal_code"] = "00000"
            errors.append("Invalid postal code length")

        return row, errors

    # ----------------HELPER FUNCTIONS----------------
    def _handle_error(self, message, error_type):
        severity = self.severity_levels.get(error_type, "Fail-Ignore")
        logging.error(f"{message} | Severity: {severity}")

        if severity == "Fail-Fail":
            raise ValueError(f"Validation failed: {message}")
        if severity == "Fail-Skip":
            return None
        return True
                

