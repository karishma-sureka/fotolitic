from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from apiclient import errors
from apiclient import http
import io
import json

# Routine to change to the current directory
def changeToPresentDirectory():
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

changeToPresentDirectory()

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# print flags
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

dumpPath = '/Users/manishdwibedy/Documents/Codes/Hackathon/HackPoly/photolytiq/dumpDir/'

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
                                   'drive-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
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

def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    results = service.files().list(
        pageSize=10,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        # for item in items:
        item = items[0]
        print('{0} ({1})'.format(item['name'], item['id']))
        print_file_metadata(service, item['id'])

        download_file(service, item['id'], open(dumpPath + item['name'], 'a'))
        print('\n\n')
            #
            # file_id = item['id']
            # request = service.files().get_media(fileId=file_id)
            # fh = io.BytesIO()
            # downloader = MediaIoBaseDownload(fh, request)
            # done = False
            # while done is False:
            #     status, done = downloader.next_chunk()
            #     # print "Download %d." % int(status.progress() * 100)

def print_file_metadata(service, file_id):
  """Print a file's metadata.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to print metadata for.
  """
  try:
    file = service.files().get(fileId=file_id).execute()

    # print(type(file))
    for key, value in file.iteritems():
        print(key + ':' + value)
    # print('Title: %s' % file['title'])
    # print('MIME type: %s' % file['mimeType'])
  except errors.HttpError, error:
    print('An error occurred: %s' % error)

def download_file(service, file_id, local_fd):
  """Download a Drive file's content to the local filesystem.

  Args:
    service: Drive API Service instance.
    file_id: ID of the Drive file that will downloaded.
    local_fd: io.Base or file object, the stream that the Drive file's
        contents will be written to.
  """
  request = service.files().get_media(fileId=file_id)
  media_request = http.MediaIoBaseDownload(local_fd, request)

  while True:
    try:
      download_progress, done = media_request.next_chunk()
    except errors.HttpError, error:
      print('An error occurred: %s' % error)
      print(json.loads(errors.HttpError.content.decode('utf-8'))['error']['message'])  # works

      return
    if download_progress:
      print('Download Progress: %d%%' % int(download_progress.progress() * 100))
    if done:
      print('Download Complete')
      return

if __name__ == '__main__':
    main()
