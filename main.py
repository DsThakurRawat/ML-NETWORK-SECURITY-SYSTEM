from networksecurity.componets.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetwrokSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
import sys

if __name__ == '__main__':
     try:
          TrainingPipelineConfig = TrainingPipelineConfig()
          data_ingestion_config = DataIngestionConfig(TrainingPipelineConfig)
          data_ingestion = DataIngestion(data_ingestion_config)
          logging.info("Started data ingestion")
          dataingestionartifact =  data_ingestion.initiate_data_ingestion()
          print(dataingestionartifact)
          
     except Exception as e:
          raise NetwrokSecurityException(e,sys)