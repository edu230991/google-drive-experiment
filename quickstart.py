# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START drive_quickstart]

import os

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import file, client, tools
from mimetypes import guess_type

# If modifying these scopes, delete the file token.json.


def get_service(scope='readonly'):
    SCOPES = 'https://www.googleapis.com/auth/drive'
    
    if scope!='full':
        SCOPES += f'.{scope}'

    store = file.Storage(f'{scope}.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))
    return service


def read_files(service):
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
    return items


def upload_file(local_path, name, service, parent_folder_id):
    file_metadata = {
        'name': name,
        'parents': [parent_folder_id]
    }
    media = MediaFileUpload(os.path.join(local_path, name),
                            mimetype=guess_type(name)[0])
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    return file


def find_id(items, name):
    items_dict = {item['name']: item['id'] for item in items}
    return items_dict[name]


if __name__ == '__main__':
    service = get_service(scope='full')
    items = read_files(service)
    
    # with open('file.txt', 'w') as f:
    #     for i in range(10):
    #         f.write(f"This is line {i+1}\r\n")
    
    # upload_file('.', 'file.txt', service, find_id(items, 'test folder'))

    # read_files(service)