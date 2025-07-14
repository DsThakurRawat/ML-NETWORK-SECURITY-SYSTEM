from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetwrokSecurityException    
from networksecurity.logging.logger import logging

from scipy.stats import ks_2samp
import pandas as pd
import numpy as np
import os
import sys
from typing import List
