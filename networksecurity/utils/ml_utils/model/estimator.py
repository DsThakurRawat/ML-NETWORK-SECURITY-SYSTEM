from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME

import os
import sys

from networksecurity.exception.exception import NetwrokSecurityException
from networksecurity.logging.logger import logging

class NetworkModel: #class which have both preprocesssor and model file
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetwrokSecurityException(e,sys)
        
    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            return self.model.predict(x_transform)
            return y_hat
        
        except Exception as e:
               raise NetwrokSecurityException(e,sys)
        
    
