from dataclasses import dataclass
from datetime import datetime
from networksecurity.constant import training_pipeline

@dataclass
class DataIngestionArtifact:
    trained_file_path : str
    test_file_path : str