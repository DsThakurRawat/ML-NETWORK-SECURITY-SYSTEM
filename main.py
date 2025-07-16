from networksecurity.componets.data_ingestion import DataIngestion
from networksecurity.componets.data_validation import DataValidation
from networksecurity.exception.exception import NetwrokSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
import sys

if __name__ == '__main__':
     try:
          trainingpipelineconfig = TrainingPipelineConfig()
          data_ingestion_config = DataIngestionConfig(trainingpipelineconfig)
          data_ingestion = DataIngestion(data_ingestion_config)
          logging.info("Initiate the  data ingestion")
          dataingestionartifact =  data_ingestion.initiate_data_ingestion()
          print(dataingestionartifact)
          logging.info("Data ingestion completed")

          data_validation_config = DataValidation(trainingpipelineconfig)
          data_validation = DataValidation(data_ingestion_config,data_validation_config)
          logging.info("Initiate  data validation")
          data_validation_artifact = data_validation.initiate_data_validation(dataingestionartifact)
          print(data_validation_artifact)
          logging.info("Data validation completed")
          
     except Exception as e:
          raise NetwrokSecurityException(e,sys)