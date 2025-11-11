import os
from pathlib import Path

root_folder = "US_VISA"

file_lists = [
    f"{root_folder}/__init__.py",
    f"{root_folder}/components/__init__.py",
    f"{root_folder}/components/data_ingestion.py",  
    f"{root_folder}/components/data_validation.py",
    f"{root_folder}/components/data_transformation.py",
    f"{root_folder}/components/model_trainer.py",
    f"{root_folder}/components/model_evaluation.py",
    f"{root_folder}/components/model_pusher.py",
    f"{root_folder}/configuration/__init__.py",
    f"{root_folder}/constants/__init__.py",
    f"{root_folder}/entity/__init__.py",
    f"{root_folder}/entity/config_entity.py",
    f"{root_folder}/entity/artifact_entity.py",
    f"{root_folder}/exception/__init__.py",
    f"{root_folder}/logger/__init__.py",
    f"{root_folder}/pipline/__init__.py",
    f"{root_folder}/pipline/training_pipeline.py",
    f"{root_folder}/pipline/prediction_pipeline.py",
    f"{root_folder}/utils/__init__.py",
    f"{root_folder}/utils/main_utils.py",
    "app.py",
    "requirements.txt",
    "Dockerfile",
    ".dockerignore",
    "demo.py",
    "setup.py",
    "config/model.yaml",
    "config/schema.yaml",
    "test.py"

]

for filepath in file_lists:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok= True)
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, 'w') as f:
            pass 
    else:
        print(f"{filename} was created in directory {filedir}")

