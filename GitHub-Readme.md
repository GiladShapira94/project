# Push folder to GitHub example
After you run a project on your source cluster you would need to push the artifacts file to your GitHub repository, this example show 
how you can do it from jupyter or any python notebook .

#### install Gitpython package
````
pip install Gitpython
````
#### Clone From GitHub
* Before you try to push ,clone your repository  - do not pass this step 

````
git.Repo.clone_from('<GitHub url>', '<name directory>')
````
#### Initialize a repository
1. For initialize new repository, use:
````
import git

repo = git.Repo.init(<directory name>)

````
2. For initialize exciting repository, use:
````
import git

repo = git.Repo(<directory name>)

````

#### Config GitHub user.name and user.email
````
with repo.config_writer() as git_config:
    git_config.set_value('user', 'email', '<email>')
    git_config.set_value('user', 'name', '<user name>')
# To check configuration values, use `config_reader()`
with repo.config_reader() as git_config:
    print(git_config.get_value('user', 'email'))
    print(git_config.get_value('user', 'name'))
````
#### Change source path - Must for push authentication

1. Delete current source
````
repo.delete_remote('origin')
````
2. Create new source with authentication details

````
repo.create_remote('origin','https://<user name>:<git token>@github.com/<user name>/project.git')
````
3. Print source details 
````
print(f'Remote name: {repo.remotes.origin.name}')
print(f'Remote URL: {repo.remotes.origin.url}')
````
#### Add and Commit files
* tip  - you can use this code lines to save easily all directory contant to a list for the add command
````
from os import listdir
from os.path import isfile, join

files_to_add = [f for f in listdir(<directory path>) if isfile(join(<directory path>, f))]
`````
1. Add files  - all files in the list will add 
````
repo.index.add(files_to_add)
````
2. Add files  - all files in the list will add 
````
repo.index.commit('Initial commit.')
````
#### Push
````
repo.remotes.origin.push(refspec='master')
````
