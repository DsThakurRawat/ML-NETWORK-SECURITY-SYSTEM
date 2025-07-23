from networksecurity.componets.data_ingestion import DataIngestion
from networksecurity.componets.data_validation import DataValidation
from networksecurity.exception.exception import NetwrokSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    TrainingPipelineConfig,
    DataTransformationConfig,
)
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
import sys
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR


from networksecurity.componets.data_transformation import DataTransformation

if __name__ == '__main__':
    try:
        trainingpipelineconfig = TrainingPipelineConfig()

        # --- Data Ingestion ---
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=trainingpipelineconfig)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        logging.info("Initiating data ingestion")
        dataingestionartifact: DataIngestionArtifact = data_ingestion.initiate_data_ingestion()
        print(dataingestionartifact)
        logging.info("Data ingestion completed")

        # --- Data Validation ---
        # CORRECT: Instantiate DataValidationConfig using the TrainingPipelineConfig
        data_validation_config = DataValidationConfig(training_pipeline_config=trainingpipelineconfig)
        
        # CORRECT: Pass the artifact and the new config to the DataValidation class
        data_validation = DataValidation(
            data_ingestion_artifact=dataingestionartifact,
            data_validation_config=data_validation_config
        )
        
        logging.info("Initiating data validation")
        # CORRECT: Call the method without passing any arguments
        data_validation_artifact: DataValidationArtifact = data_validation.initiate_data_validation()
        print(data_validation_artifact)
        logging.info("Data validation completed")
        print(data_validation_artifact)

        # --- Data Transformation ---
        # --- Data Transformation ---
        logging.info("Initiating data transformation")

# ✅ Use the same trainingpipelineconfig defined earlier
        data_transformation_config = DataTransformationConfig(trainingpipelineconfig)

        data_transformation = DataTransformation(
    data_validation_artifact=data_validation_artifact,
    data_transformation_config=data_transformation_config
)

        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info("Data transformation completed")

       

    except Exception as e:
        logging.error(e)
        raise NetwrokSecurityException(e, sys)
