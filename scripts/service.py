import logging

import httplib2
import zerorpc
from oauth2client import client

import control


class mainRPC(object):
    def start(self, username, passwword, calendar_name, token):

        # Set path to the Web application client_secret_*.json file you downloaded from the
        # Google API Console: https://console.developers.google.com/apis/credentials
        CLIENT_SECRET_FILE = './client_secret_740285853573-95vasiof2bns329i8ve37ilaen77a39t.apps.googleusercontent.com.json'

        # Exchange auth code for access token, refresh token, and ID token
        credentials = client.credentials_from_clientsecrets_and_code(
            CLIENT_SECRET_FILE,
            ['https://www.googleapis.com/auth/calendar'],
            token)

        print("2")

        # Call Google API
        http_auth = credentials.authorize(httplib2.Http())

        # Call the calendar scraper
        result = control.main(username, passwword, calendar_name, credentials)
        return result


logging.basicConfig()
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
s = zerorpc.Server(mainRPC())
s.bind("tcp://0.0.0.0:4242")
s.run()