"""Loads spreadsheet from google API.

@author: Andréas andreas@tenoli.org
"""
# coding: utf-8
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.tools import argparser

import pandas as pd

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def load_monitoring_data():
    """Returns the spreadsheet data into a pandas dataframe.

    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1mzkBPmrraYCx7tL5jVW8G30FPBMucz0QKYOOt2qPamA' #'1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'

    # VALUES
    rangeName = 'A2:M'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    # COLUMNS
    rangeName = 'A1:M1'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    columns = result.get('values', [])[0]

    #DATAFRAME
    df = pd.DataFrame(values, columns=columns)

    rename_columns = {'Clave': 'store_id',
                      'Tienda': 'name', 
                      'Tendero': 'storekeeper', 
                      u'Invitación': 'invitation', 
                      'Taller 1': 'workshop1',
                      'Focos recibidos': 'spotlights_received', 
                      'Focos colocados': 'spotlights_placed', 
                      'Taller 2': 'workshop2', 
                      'Pintura recibida': 'paint_received',
                      'Pintura colocada': 'paint_placed', 
                      'Taller 3': 'workshop3', 
                      'Lona recibida': 'cover_received', 
                      'Lona colocada': 'cover_placed'}

    df = df.rename(columns=rename_columns)
    df = df.set_index('store_id')

    replace_values = {'SI': True, 'NO': False}
    df = df.replace(replace_values)

    df = df.loc[df.index.drop_duplicates()]

    return df


if __name__ == '__main__':
    df = load_monitoring_data()
