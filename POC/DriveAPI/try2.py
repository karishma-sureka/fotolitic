import httplib2
from oauth2client.appengine import AppAssertionCredentials
from apiclient.discovery import build

def createDriveService():
    """Builds and returns a Drive service object authorized with the
       application's service account.
       Returns:
           Drive service object.
    """

    credentials = AppAssertionCredentials(scope='https://www.googleapis.com/auth/drive')
    http = httplib2.Http()
    http = credentials.authorize(http)
    return build('drive', 'v1', http=http, developerKey='AIzaSyA9j1GWqNWUjpBA6DhRQzAQYeJQalfJSWs')

service = createDriveService()
