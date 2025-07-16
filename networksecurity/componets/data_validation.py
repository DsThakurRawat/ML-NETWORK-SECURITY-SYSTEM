from __future__ import annotations

import os
import sys
from typing import List

import numpy as np
import pandas as pd
from scipy.stats import ks_2samp

from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetwrokSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file


class DataValidation:
    """Validate raw datasets produced by the Data‑Ingestion step."""

    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig,
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetwrokSecurityException(e, sys) from e

    # ------------------------------------------------------------------ #
    # Utility helpers
    # ------------------------------------------------------------------ #

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        """Load a CSV file into a DataFrame."""
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetwrokSecurityException(e, sys) from e

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        """Ensure the dataframe has exactly the columns defined in the schema file."""
        try:
            required_columns = len(self._schema_config["columns"])
            logging.info(f"Required number of columns : {required_columns}")
            logging.info(f"Actual number   of columns : {len(dataframe.columns)}")
            return len(dataframe.columns) == required_columns
        except Exception as e:
            raise NetwrokSecurityException(e, sys) from e

    def detect_dataset_drift(
        self,
        base_df: pd.DataFrame,
        current_df: pd.DataFrame,
        threshold: float = 0.05,
    ) -> bool:
        """Run a univariate KS‑test between the base (train) and current (test) datasets.

        Returns
        -------
        bool
            True  →   significant drift detected  
            False →   no drift
        """
        try:
            drift_report: dict[str, dict[str, float | bool]] = {}
            drift_found = False

            numeric_dtypes = [np.int16, np.int32, np.int64, np.float16, np.float32, np.float64]

            for column in base_df.columns:
                # skip non‑numeric columns
                if base_df[column].dtype not in numeric_dtypes:
                    continue

                stats = ks_2samp(base_df[column], current_df[column])
                is_drift = stats.pvalue < threshold
                drift_found = drift_found or is_drift

                drift_report[column] = {
                    "p_value": float(stats.pvalue),
                    "drift_status": is_drift,
                }

            # persist the report
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            os.makedirs(os.path.dirname(drift_report_file_path), exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=drift_report)

            return drift_found
        except Exception as e:
            raise NetwrokSecurityException(e, sys) from e

    # ------------------------------------------------------------------ #
    # Driver
    # ------------------------------------------------------------------ #

    def initiate_data_validation(self) -> DataValidationArtifact:
        """Orchestrates the complete validation flow and returns the artifact."""
        try:
            # -------------------------------------------------------------- #
            # 1. Load data
            # -------------------------------------------------------------- #
            train_df = self.read_data(self.data_ingestion_artifact.trained_file_path)
            test_df = self.read_data(self.data_ingestion_artifact.test_file_path)

            # -------------------------------------------------------------- #
            # 2. Basic column validation
            # -------------------------------------------------------------- #
            error_message = ""
            if not self.validate_number_of_columns(train_df):
                error_message += "Train dataframe does not contain all required columns.\n"
            if not self.validate_number_of_columns(test_df):
                error_message += "Test dataframe does not contain all required columns.\n"

            if error_message:
                raise Exception(error_message)

            logging.info("Column‑count validation passed.")

            # -------------------------------------------------------------- #
            # 3. Data‑drift check
            # -------------------------------------------------------------- #
            drift_found = self.detect_dataset_drift(train_df, test_df)
            if drift_found:
                logging.warning("⚠️  Statistical drift detected between train and test data.")
            else:
                logging.info("No statistical drift detected.")

            # -------------------------------------------------------------- #
            # 4. Persist validated datasets
            # -------------------------------------------------------------- #
            os.makedirs(os.path.dirname(self.data_validation_config.valid_train_file_path), exist_ok=True)

            train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
            test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)

            # -------------------------------------------------------------- #
            # 5. Build and return artifact
            # -------------------------------------------------------------- #
            data_validation_artifact = DataValidationArtifact(
                validation_status=not drift_found,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            logging.info(f"DataValidationArtifact created: {data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise NetwrokSecurityException(e, sys) from e

        