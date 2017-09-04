import os

import httplib2
from apiclient import discovery, errors
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


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
    credential_path = os.path.join(credential_dir, 'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def delete_file(service, file_id):
    try:
        print file_id
        # service.files().delete(fileId=file_id).execute()
    except errors.HttpError, error:
        print 'An error occurred: %s' % error


def delete_all_my_files(service):
    page_token = None
    file_handler = service.files()
    while True:
        print 'Querying...'
        try:
            files = file_handler.list(
                pageToken=page_token, orderBy='quotaBytesUsed desc', q="'YOUR_EMAIL_ADDRESS_HERE' in owners").execute()
            items = files['items']
            if not items:
                break
            for item in items:
                file_id = item['id']
                try:
                    file_handler.delete(fileId=file_id).execute()
                except errors.HttpError, error:
                    print 'An error occurred: %s' % error
                else:
                    print 'Deleted file: %s' % item['title']

            page_token = files.get('nextPageToken')
            if not page_token:
                break
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            break


def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http)

    delete_all_my_files(service)


if __name__ == '__main__':
    main()
