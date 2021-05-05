#!/usr/bin/env python3

import requests
import argparse
import os
import json
import sys

class ConnectionFactor:

    def __init__(self, args):
        self.args = args
        self.mode = None
        self.auth={
            'headers' : {'Content-type': 'application/json'},
        }

    def generateCredentials(self):
        if self.args.user and (self.args.password or self.args.password_env ):
            user = self.args.user
            if self.args.password:
                password = self.args.password
            else:
                password = os.environ[self.args.password_env]            
            self.auth['auth'] = (user, password)
        elif self.args.token or self.args.token_env:            
            if self.args.token:
                token = self.args.token
            else:
                token = os.environ[self.args.token_env]
            self.auth['headers']['Authorization']=f'Bearer {token}'
        else:
            print("Authentication data missing.")
            parse_arguments(True)

    def split(self, argument):
        (name, value) = argument.split("=",1)
        return (name, { "value" : value })

    def get_variable_group(self):
        url = f"https://dev.azure.com/{self.args.organization}/{self.args.project}/_apis/distributedtask/variablegroups/{self.args.group_id}?api-version=6.1-preview.2"
        response = requests.get(url, **self.auth)
        
        base = response.json()
        del base['createdBy']
        del base['createdOn']
        del base['modifiedBy']
        del base['modifiedOn']
        for arg in self.args.values:
            (varname, valuestruct) = self.split(arg)
            base['variables'][varname] = valuestruct
        result = requests.put(f'https://dev.azure.com/{self.args.organization}/_apis/distributedtask/variablegroups/{self.args.group_id}?api-version=6.0-preview.2',                     
                    data=json.dumps(base),                    
                    **self.auth)


def parse_arguments(quit=None):
    parser = argparse.ArgumentParser(description='Update the variables at the Azure DevOps variable group.',
        usage=f"""
    This scripts updates only the variables at the variable group which has been 
    listed a the values.

    E.g. 

    {sys.argv[0]} -u my.identityt@example.com \\
        -p ExamplePersonaolToken \\
            -o example \\
            -r project \\
            -g 17 \\
            var1=my_value \\
            'var2=my multipart value'
        
        """)
    parser.add_argument('values', metavar='value pair', type=str, nargs='+',
                    help='name value pairs which will be added or replaced. e.g. test=1234')
    parser.add_argument('--user', '-u', nargs='?', help='Username for the BASIC Auth')
    parser.add_argument('--password', '-p', nargs='?', help='Password for the BASIC Auth')
    parser.add_argument('--password-env', '-v', nargs='?', help='Environment variable name for password for the BASIC Auth')
    parser.add_argument('--token', '-t', nargs='?', help='Token from Azure DevOps pipeline for Bearer authentication')
    parser.add_argument('--token-env', '-e', nargs='?', help='Environment variable name for token from Azure DevOps pipeline')
    parser.add_argument('--organization', '-o', required=True, help='Organization where the variable group is (e.g. badboysofquality)')
    parser.add_argument('--project', '-r', required=True, help='Name of the project where the variable group is (e.g. opensource)')
    parser.add_argument('--group-id', '-g', required=True, type=int, help='Numbert id of the variable group.')
    if quit:
        parser.print_help()
        exit(1)
    return parser.parse_args()



def main():
    args = parse_arguments()
    connection = ConnectionFactor(args)
    connection.generateCredentials()
    connection.get_variable_group()

if __name__ == "__main__":
    main()

