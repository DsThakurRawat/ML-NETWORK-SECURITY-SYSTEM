import yaml
from networksecurity.exception.exception import NetwrokSecurityException
from networksecurity.logging.logger import logging
import os,sys
import numpy as np
import pickle


def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetwrokSecurityException(e,sys)
    


def write_yaml_file(file_path: str,content:object,replace : bool = False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as file_obj:
            yaml.dump(content,file_obj)
    except Exception as e:
        raise NetwrokSecurityException(e,sys)
    
def save_numpy_array_data(file_path : str,array : np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise NetwrokSecurityException(e,sys)
    
#knn imputer will basiclly created pickle files

def save_object(file_path : str,obj : object) -> None:
    try:
        logging.info("Entered the save_object method of maiutils class")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as file_obj:
            pickle.dump(obj,file_obj)
        logging.info("Exited the save_object method of maiutils class")
    except Exception as e:
        raise NetwrokSecurityException(e,sys)
    

def load_object(file_path: str,)-> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path,"rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise NetwrokSecurityException(e,sys) from e
    

def load_numpy_array_data(file_path:str)->np.array:
    """
    load numpy array data from file 
    file_path : str location of file to load
    return : np.array data loaded
    """
    try:
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetwrokSecurityException(e,sys)