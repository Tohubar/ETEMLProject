import os, sys  
import yaml, dill
import numpy as np
import pandas as pd
from US_VISA.exception import UsVisaException
from US_VISA.logger import logging


def read_yaml(filepath: str) -> dict:
    logging.info("Entered read_yaml() func")
    try:
        with open(filepath, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
        logging.info("Exite read_yaml() func")
    except Exception as e:
        raise UsVisaException(e, sys)

def write_yaml(filepath: str, content: object, replace: bool = False) -> None:
    logging.info("Entered write_yaml() func")
    try:
        if replace:
          if os.path.exists(filepath):
              os.remove(filepath)
        os.makedirs(os.path.dirname(filepath), exist_ok= True)
        logging.info("exite write_yaml() func")

        with open(filepath, "w") as fil:
            yaml.dump(content, fil)
    except Exception as e:
        UsVisaException(e, sys)

def load_object(filepath:str) -> object:
    logging.info("Entered load_object() func")

    try:
        with open(filepath, "rb") as fil:
            obj = dill.load(fil)
        logging.info("exite load_object() func")
        
        return obj
    except Exception as e:
        raise UsVisaException(e, sys)
def save_object(filepath: str, content: object):
    logging.info("Entered save_object() util")

    try:
        os.makedirs(os.path.dirname(filepath), exist_ok= True)
        with open(filepath, "wb") as fil:
            dill.dump(content, fil)
        logging.info("exited save_object() util")
        
    except Exception as e:
        raise UsVisaException(e, sys)

def load_numpy_array(filepath: str) -> np.array:
    try:
        with open(filepath, 'rb') as fil:
            nparr = np.load(fil)
        return nparr
    except Exception as e:
        raise UsVisaException(e, sys)
    
def save_numpy_array(filepath: str, nparr: np.array):
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok= True)
        with open(filepath, "wb") as fil:
            np.save(nparr, fil)
    except Exception as e:
        raise UsVisaException(e, sys)
    
def drop_column(df: pd.DataFrame, cols: list):
    try:
        return df.drop(columns= cols, axis= 1)
    except Exception as e:
        raise UsVisaException(e, sys)