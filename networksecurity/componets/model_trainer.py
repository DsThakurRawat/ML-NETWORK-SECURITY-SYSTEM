import os
import sys

from networksecurity.exception.exception import NetwrokSecurityException
from networksecurity.logging.logger import logging

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import save_object, load_object, load_numpy_array_data, evaluate_models
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from networksecurity.entity.artifact_entity import ModelTrainerArtifact, DataTransformationArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
import mlflow

class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetwrokSecurityException(e, sys)
        
    def track_mlflow(self,best_model,classification_train_metric):
        with mlflow.start_run():
            f1_score = classification_train_metric.f1_score
            precision_score = classification_train_metric.precision_score
            recall_score = classification_train_metric.recall_score

            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("precision_score", precision_score)
            mlflow.log_metric("recall_score", recall_score)

            mlflow.log_params(best_model.get_params())
            mlflow.sklearn.log_model(best_model, "model")




        

    def train_model(self, x_train, y_train, x_test, y_test):
        try:
            models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }

            params = {
                "Decision Tree": {
                    'criterion': ['gini', 'entropy'],
                },
                "Random Forest": {
                    'n_estimators': [8, 16, 32, 64, 128, 256],
                },
                "Gradient Boosting": {
                    "learning_rate": [0.1, 0.01, 0.05],
                    "subsample": [0.6, 0.7, 0.9],
                    "n_estimators": [8, 16, 32, 64, 128, 256],
                },
                "Logistic Regression": {},
                "AdaBoost": {
                    "learning_rate": [0.1, 0.01, 0.05],
                    "n_estimators": [8, 16, 32, 64, 128, 256],
                }
            }

            model_report: dict = evaluate_models(
                x_train=x_train,
                y_train=y_train,
                x_test=x_test,
                y_test=y_test,
                models=models,
                params=params
            )

            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_model = models[best_model_name]



            





            y_train_pred = best_model.predict(x_train)
            y_test_pred = best_model.predict(x_test)

            classification_train_metric = get_classification_score(y_true=y_train, y_pred=y_train_pred)
            classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)
            
            # Track the mlflow model
           
            # Track the mlflow model
            self.track_mlflow(best_model=best_model,classification_train_metric =  classification_train_metric)


            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)

            network_model = NetworkModel(preprocessor=preprocessor, model=best_model)
            save_object(self.model_trainer_config.trained_model_file_path, obj=network_model)

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric
            )

            logging.info(f"Model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact

        except Exception as e:
            logging.error(f"Error during model training: {e}")
            raise NetwrokSecurityException(e, sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train, y_train = train_arr[:, :-1], train_arr[:, -1]
            x_test, y_test = test_arr[:, :-1], test_arr[:, -1]

            model_trainer_artifact = self.train_model(x_train, y_train, x_test, y_test)
            return model_trainer_artifact

        except Exception as e:
            logging.error(f"Error in initiate_model_trainer: {e}")
            raise NetwrokSecurityException(e, sys)


"""
using ml flow 

MLflow is an open-source platform for managing the complete machine learning lifecycle. It helps you track, reproduce, and deploy machine learning models in a standardized and scalable way.

🧠 Why Use MLflow?
In any ML/DL project, you typically go through:

Experimentation (different models, hyperparameters, datasets)

Tracking (metrics, versions)

Packaging (saving the model/code in reusable format)

Deployment (exposing it to production)

MLflow brings all of this together.

| Component           | Purpose                                                                                     |
| ------------------- | ------------------------------------------------------------------------------------------- |
| **MLflow Tracking** | Log metrics, parameters, artifacts, source code for each experiment run                     |
| **MLflow Projects** | Package your code in a reproducible format (e.g., conda, Docker)                            |
| **MLflow Models**   | Save and serve models with support for many frameworks (e.g., sklearn, TensorFlow, PyTorch) |
| **MLflow Registry** | Manage the lifecycle of models: staging → production → archived                             |


✅ Features
Works with any ML library (scikit-learn, TensorFlow, PyTorch, XGBoost, etc.)

Logs:

Metrics (accuracy, loss, etc.)

Parameters (e.g., learning rate, depth)

Artifacts (plots, models)

Source version (Git commit)

Model versioning and rollback

Web UI to view and compare runs

Integrates well with cloud and MLOps tools

🛠 Example (MLflow Tracking in Python)

import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

with mlflow.start_run():
    model = RandomForestClassifier(n_estimators=100, max_depth=5)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 5)
    mlflow.log_metric("accuracy", acc)
    
    mlflow.sklearn.log_model(model, "random_forest_model")

    
      🔗 MLflow in MLOps
MLflow is often used as the experiment tracking + model registry tool in MLOps pipelines, integrated with:

Docker + FastAPI for deployment

Airflow/Kubeflow for orchestration

AWS/GCP/Azure for cloud hosting





"""

