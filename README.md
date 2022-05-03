# Load project from git 

#### Prerequisites:
* Upload all relavant files to a git reposistory  - as shown here
  * Each ML functions needs to have a python file
  * Each artifacts needs to have local file  - same as models files
  * Must have project.yaml  - you can produce source project YAML by excute save function on the source cluter
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
