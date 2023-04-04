#!/usr/bin/env python3

import requests
import json
from prettytable import PrettyTable

from .config import Config
from .functions import printError, printWarn

class Tokens(object):

    def __init__(self, config):
        self.config = config
        self.tokens = None

        self.table = PrettyTable()
        self.table.field_names = ['Token']

    def fetchData(self):
        """Retrieve the list of all tokens"""

        # if data is already downloaded, use cached data
        if self.tokens != None:
            return True

        # check if headers are correctly set for authorization
        if not self.config.headers():
            return False

        if self.config.debug:
            print('GET', self.config.endpoint + 'token?', self.config.params())

        # Make request to API endpoint
        response = requests.get(self.config.endpoint + 'token', params=self.config.params(), headers=self.config.headers())

        # Check status code of response
        if response.status_code == 200:
            # Get list of tokens from response
            json = response.json()
            if 'tokens' in json:
                self.tokens = response.json()['tokens']
                return True
            else:
                self.tokens = None
                return False
        else:
            printError('An error occurred:', response.status_code)
            self.tokens = None
            return False

    def list(self, token: str = '', format: str = 'table', delimiter: str = ';'):
        """Iterate through list of tokens and print details"""

        if self.fetchData():
            if self.tokens != None:

                # if JSON was requested and no filters, then just print it without iterating through
                if (format == 'json' and not token):
                    print(json.dumps(self.tokens, indent=4))
                    return

                for token in self.tokens:
                    if token:
                        if token['token'] == token:
                            self.print(token)
                            break
                    else:
                        self.print(token)

            if (format == 'table'):
                print(self.table)
            elif (format == 'csv'):
                print(self.table.get_csv_string(delimiter=delimiter))

    def token(self):
        """Print the data of first token"""

        if self.fetchData() and len(self.tokens) > 0:
            return self.tokens[0]['token']

    def create(self):
        """Create a new token"""

        # check if headers are correctly set for authorization
        if not self.config.headers():
            return False

        if self.config.debug:
            print('POST', self.config.endpoint + 'token', self.config.params())

        if self.config.readonly:
            return False

        response = requests.post(self.config.endpoint + 'token',  headers=self.config.headers())

        # Check status code of response
        if response.status_code == 200:
            print('Created token')
            return True
        else:
            printError('Failed to create token with response code:', response.status_code)
            return False

    def print(self, token, format: str = 'table'):
        """Print the data of the specified token"""

        if (format == 'json'):
            print(json.dumps(token, indent=4))
        else:
            token = token['token']
            self.table.add_row([token])
