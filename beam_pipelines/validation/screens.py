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
from apache_beam.io.filesystems import FileSystems

class StgCustomerValidation:
    def __init__(self, severity_levels = None):
        self.columns_count = None
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
        # Validate file structure and format
        self.columns_count = len(expected_columns)

        """
        if not os.path.exists(file_path):
            self._handle_error("File missing", "file_missing")
        """
        # Check if file exists in GCS
        match_result = list(FileSystems.match([file_path]))
        if not match_result or not match_result[0].metadata_list:
            self._handle_error("File missing", "file_missing")

        """
        if not re.match(filename_template, os.path.basename(file_path)):
            self._handle_error("File name does not match the template", "filename_template")
        """
        # Validate file name
        file_name = file_path.split("/")[-1]
        if not re.match(filename_template, file_name):
            self._handle_error("File name does not match the template", "filename_template")

        """
        with open(file_path, "r") as file:
            lines = file.readlines(2)
        """
        # Read file content from GCS
        with FileSystems.open(file_path) as file:
            lines = [line.decode("utf-8") for line in file.readlines(2)]

        if not lines or len(lines) == 1:
            self._handle_error("Empty file or only header line", "empty_file")

        header = lines[0].strip().split(",")
        if header != expected_columns:
            self._handle_error("Missing or mismatched columns in file header", "missing_column_header")

        return True

    # ----------------COLUMN SCREENS----------------
    def validate_and_correct_row(self, row):
        # Validate and correct individual rows
        errors = []

        if not len(row) == self.columns_count:
            self._handle_error("Missing columns in row", "missing_column_data")
            errors.append("Row missing column data")
            return row, errors

        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", row.get("email", "")):
            errors.append("Invalid email format")

        if row.get("state") not in {"NY", "CA", "TX", "FL", "IL"}:
            row["state"] = "DF" # Corrective action: Default state code to DF
            errors.append("Invalid state code, defaulted to DF")

        if row.get("country") != "US":
            row["country"] = "US" # Corrective action: Default country code to US
            errors.append("Invalid country, defaulted to US")

        if len(row.get("postal_code", "")) != 5 or not row["postal_code"].isdigit():
            row["postal_code"] = "10000" # Corrective action: Default postal code to 10000
            errors.append("Invalid postal code, defaulted to 10000")

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
                

