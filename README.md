# Azure DevOps Variable group updates

It's nearly impossible to update only required variables at the Azure DevOps Variable group
from the API. This script updates _only_ the selected values.

The authentication can be personal access token or e.g. Azure DevOps pipeline 
`System.AccessToken`.

## Usage

```
usage: 
    This scripts updates only the variables at the variable group which has been 
    listed a the values.

    E.g. 

    ./bin/update-variable.py -u my.identityt@example.com \
        -p ExamplePersonaolToken \
            -o example \
            -r project \
            -g 17 \
            var1=my_value \
            'var2=my multipart value'
        
        

Update the variables at the Azure DevOps variable group.

positional arguments:
  value pair            name value pairs which will be added or replaced. e.g.
                        test=1234

optional arguments:
  -h, --help            show this help message and exit
  --user [USER], -u [USER]
                        Username for the BASIC Auth
  --password [PASSWORD], -p [PASSWORD]
                        Password for the BASIC Auth
  --password-env [PASSWORD_ENV], -v [PASSWORD_ENV]
                        Environment variable name for password for the BASIC
                        Auth
  --token [TOKEN], -t [TOKEN]
                        Token from Azure DevOps pipeline for Bearer
                        authentication
  --token-env [TOKEN_ENV], -e [TOKEN_ENV]
                        Environment variable name for token from Azure DevOps
                        pipeline
  --organization ORGANIZATION, -o ORGANIZATION
                        Organization where the variable group is (e.g.
                        badboysofquality)
  --project PROJECT, -r PROJECT
                        Name of the project where the variable group is (e.g.
                        opensource)
  --group-id GROUP_ID, -g GROUP_ID
                        Numbert id of the variable group.
```

### Usage from Azure DevOps pipeline

Currently to use from the Azure DevOps pipeline you need following snippet:

```yaml
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.x' 
    addToPath: true
- script: |    
    pip3 install requests
    curl -o update-variable.py https://raw.githubusercontent.com/TheProjectAurora/azure-devops-variable-updater/main/bin/update-variable.py
    python3 update-variable.py -t $(System.AccessToken) \
      -o <organiozation name> \
      -r <project> \
      -g  <group variable id>\
      latest_test=$(Build.BuildNumber)
```

## Installation

At the moment pip-package is not generated.

```
pip install
```
