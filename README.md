# Load project from git 

#### Prerequisites:
* Upload all relavant files to a git reposistory  - as shown here
  * Each ML functions needs to have a python file
  * Each artifacts needs to have local file  - same as models files
  * Must have project.yaml  - you can produce source project YAML by excute save function on the source cluter
  * You can find an example how to push from jupyter on this [link](https://github.com/GiladShapira94/project/blob/master/GitHub-Readme.md)
* Edit YAML file for the intallation - see example in this repository

# Edit YAML file
The project YAML need to be edit before you load the project to the target cluster - you can see and example project YAML in this repository
* #### Functions:
  * kind - must provide ('job','local','remote','serving','nuclio')
  * name - function name
  * url - local path to fuction python file
  * image - function image 
  * requirements - package to be installed
  * default_class - defualt class for serving functions
  * model - here you need to define your model details 
    * name - model name
    * uri - local path for model file (important - before deploy serving function log the models to the systems)
* #### Artifacts:
  * kind - artifacts kind ('dataset','artifact','model')
  * local_path - local path the artifact file
  * format - file format, if necessary 
  * key - must provide, key data value
  * model_file - model file name  - not the path 
# How to load a project
#### load a project from git 
1. Load project from GitHub ,the context of the git repository would save in the context directory
````
project = mlrun.load_project(url='git://github.com/GiladShapira94/project.git',name='project-git',context='./project')
````
2. Sync function - Must
````
project.sync_functions(save=True)
````

#### Upload artifacts 
This function get project name as an input, go over project YAML file and upload the artifacts by thier atributes that you define in the YAML file
````
import mlrun 
import pickle
from pickle import dumps


def upload_artifacts(project):
    project = mlrun.load_project(name=project,context=context)

    for i in range(len(project.spec.artifacts)):
        art_dict = project.spec.artifacts[i]
        if 'kind' not in project.spec.artifacts[i].keys():
            raise KeyError(f"Please spicify kind value on your YAML file")
        kind = art_dict['kind']
        if kind == 'dataset':
            source  = project.spec.artifacts[i]['local_path']
            source = mlrun.get_dataitem(source)
            df = source.as_df()
            key = project.spec.artifacts[i]['key']
            file_format = project.spec.artifacts[i]['format']
            project.log_dataset(key=key,df=df,index=False,format=file_format)
            print(f"{key} {kind} Sucssefly Uploaded")
            
        elif kind == '' or kind == 'artifacts':
            key = project.spec.artifacts[i]['key']
            body = project.spec.artifacts[i]['body']
            labels = project.spec.artifacts[i]['labels']
            format_file = project.spec.artifacts[i]['format']
            source  = project.spec.artifacts[i]['local_path']
            project.log_artifact(key,format=file_format)
            print(f"{key} {kind} Sucssefly Uploaded")
            
        elif kind == 'model':
            key = project.spec.artifacts[i]['key']
            data = pickle.load(open(project.spec.artifacts[i]['local_path'],'rb'))
            file = project.spec.artifacts[i]['model_file']
            project.log_model(key,body=dumps(data),model_file=file)
            print(f"{key} Sucssefly Uploaded")
            print(f"{key} {kind} Sucssefly Uploaded")
````
#### IMPORTANT 
if you need to enter atrifacts path for deploying function  - edit the project YAML and then load the project again
#### Save to DB - 
After you upload the artifacts you need to the project to the iguazio DB
````
project.save_to_db()
````
#### Deploy functions 
This function get project name as an input, go over project YAML file and deploy the functions by thier atributes that you define in the YAML file
````
import mlrun

import mlrun

def deploy_all(project):

    project = mlrun.load_project(name=project,context=context)
    for i in range(len(project.spec.functions)):
        func_dict = project.spec.functions[i]
        func = project.get_function(func_dict['name'])
        name = func_dict['name']
        if 'kind' not in project.spec.functions[i].keys():
            raise KeyError(f"Please spicify kind value on your YAML file , For example: job, serving, remote")
        kind = func_dict['kind']
        if kind in ['remote','serving']:
            if 'default_class' in project.spec.functions[i].keys():
                func.spec.default_class=project.spec.functions[i]['default_class']
            if 'model' in project.spec.functions[i].keys():
                func.add_model(project.spec.functions[i]['model']['name'],project.spec.functions[i]['model']['uri'])
            func.apply(mlrun.auto_mount())
            func.deploy()
            project.set_function(f'db://{project.name}/{name}')
            print("******************************************************************************************************")
        elif kind not in ['remote','serving']:
            func.apply(mlrun.auto_mount())
            func.deploy() 
            project.set_function(f'db://{project.name}/{name}')
            print("******************************************************************************************************")
````
#### Set function in project YAML 
Excute this line for all ML functions 
````
project.set_function(f'db://<project name>/<function name>')
````
#### Save project YAML
Before you try to run project workflow its important to save changes in the project YAML
````
project.save()
````
#### Run project workflow 
````
project.run(<workflow name>,watch=True)
````

