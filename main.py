from networksecurity.componets.data_ingestion import DataIngestion
from networksecurity.componets.data_validation import DataValidation
from networksecurity.componets.data_transformation import DataTransformation
from networksecurity.componets.model_trainer import ModelTrainer  # ✅ Added
from networksecurity.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,  # ✅ Added
    TrainingPipelineConfig,
)
from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact,  # ✅ Added
)
from networksecurity.exception.exception import NetwrokSecurityException
from networksecurity.logging.logger import logging
import sys


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
        data_validation_config = DataValidationConfig(training_pipeline_config=trainingpipelineconfig)
        data_validation = DataValidation(
            data_ingestion_artifact=dataingestionartifact,
            data_validation_config=data_validation_config
        )
        logging.info("Initiating data validation")
        data_validation_artifact: DataValidationArtifact = data_validation.initiate_data_validation()
        print(data_validation_artifact)
        logging.info("Data validation completed")

        # --- Data Transformation ---
        logging.info("Initiating data transformation")
        data_transformation_config = DataTransformationConfig(trainingpipelineconfig)
        data_transformation = DataTransformation(
            data_validation_artifact=data_validation_artifact,
            data_transformation_config=data_transformation_config
        )
        data_transformation_artifact: DataTransformationArtifact = data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info("Data transformation completed")

        # --- ✅ Model Training ---
        if data_validation_artifact.validation_status:
            logging.info("Initiating model training")
            model_trainer_config = ModelTrainerConfig(trainingpipelineconfig)
            model_trainer = ModelTrainer(
                model_trainer_config=model_trainer_config,
                data_transformation_artifact=data_transformation_artifact
            )
            model_trainer_artifact: ModelTrainerArtifact = model_trainer.initiate_model_trainer()
            print(model_trainer_artifact)
            logging.info("Model training completed")
        else:
            logging.warning("Validation failed — Skipping model training.")

    except Exception as e:
        logging.error(e)
        raise NetwrokSecurityException(e, sys)
