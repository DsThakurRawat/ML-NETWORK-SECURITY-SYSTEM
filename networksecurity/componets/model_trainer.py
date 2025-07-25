import os
from networksecurity.exception.exception import NetwrokSecurityException
from networksecurity.logging.logger import logging

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import save_object,load_object
from networksecurity.utils.main_utils.utils import load_numpy_array_data
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification
from networksecurity.entity.artifact_entity import ModelTrainerArtifact,DataTransformationArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig
import os,sys

#importing all the machine learning algorithms


from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC,SVR
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier,AdaBoostClassifier,AdaBoostRegressor






class ModelTrainer:
      def __init__(self,model_trainer_config : ModelTrainerConfig,data_transformation_artifact : DataTransformationArtifact):
            try:
                  self.model_trainer_config = model_trainer_config
                  self.data_transformation_artifact = data_transformation_artifact
            except Exception as e:
                  raise NetwrokSecurityException(e,sys)
            
      def train_model(self,x_train,y_train,x_test,):
            models = {
                  "Random Frest" : RandomForestClassifier(verbose = 1),
                  "Decision Tree" : DecisionTreeClassifier(),
                  "Gradient Boosting" : GradientBoostingClassifier(verbose = 1),
                  "Logistic Regression" : LogisticRegression(verbose=1),
                  "AdaBoost" : AdaBoostClassifier(),
            }
           #hyper parameter tuning
            params = {
                  "Decision Tree" : {
                        'criterion': ['gini', 'entropy'],
                  },
                  "Random Forest" : {
                        'n_estimators': [8,16,32,64,128,256],
                  },
                  "Gradient Boosting" : {
                        "learning_rate": [0.1,0.01,0.05],
                        "subsample": [0.6,0.7,0.9],
                        "n_estimators": [8,16,32,64,128,256],

                  },
                  "Logistic Regression" : {},
                  "AdaBoost" : {
                        "learning_rate": [0.1,0.01,0.05],
                        "n_estimators": [8,16,32,64,128,256],
                  }


                 
           },
      

    
            
      def initiate_model_trainer(self)->ModelTrainerArtifact:
            try:
                  train_file_path = self.data_transformation_artifact.transformed_train_file_path
                  test_file_path = self.data_transformation_artifact.transformed_test_file_path
                  train_arr = load_numpy_array_data(train_file_path)
                  test_arr = load_numpy_array_data(test_file_path)

                  x_train,y_train = train_arr[:,:-1],train_arr[:,-1]
                  x_test,y_test = test_arr[:,:-1],test_arr[:,-1]

                  model = NetworkModel(preprocessor=load_object(file_path=self.model_trainer_config.preprocessor_path),
                  model=load_object(file_path=self.model_trainer_config.model_path))
            except Exception as e:
                  raise NetwrokSecurityException(e,sys)
            
            model = self.train_model(x_train,y_train)

            