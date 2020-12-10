import numpy as np
import cv2
import urllib
import os
import re
import requests
import csv
import pandas as pd 

class ISICApi(object):
    def __init__(self,
                 hostname='https://isic-archive.com',
                 username=None,
                 password=None):
        self.baseUrl = f'{hostname}/api/v1'
        self.authToken = None

        if username is not None:
            if password is None:
                password = input(f'Password for user "{username}":')
            self.authToken = self._login(username, password)

    def _makeUrl(self, endpoint):
        return f'{self.baseUrl}/{endpoint}'

    def _login(self, username, password):
        authResponse = requests.get(
            self._makeUrl('user/authentication'), auth=(username, password))
        if not authResponse.ok:
            raise Exception(f'Login error: {authResponse.json()["message"]}')

        authToken = authResponse.json()['authToken']['token']
        return authToken

    def get(self, endpoint):
        url = self._makeUrl(endpoint)
        headers = {'Girder-Token': self.authToken} if self.authToken else None
        return requests.get(url, headers=headers)

    def getJson(self, endpoint):
        return self.get(endpoint).json()

    def getJsonList(self, endpoint):
        endpoint += '&' if '?' in endpoint else '?'
        LIMIT = 50
        offset = 0
        while True:
            resp = self.get(
                f'{endpoint}limit={LIMIT:d}&offset={offset:d}').json()
            if not resp:
                break
            for elem in resp:
                yield elem
            offset += LIMIT

# Initialize the API; no login is necessary for public data
#Image Download
def imagedata():

  api = ISICApi()
  savePath = 'imageTrain/'

  if not os.path.exists(savePath):
    os.makedirs(savePath)

  imageList = api.getJson('image?limit=400&offset=0&sort=name')

  print('Downloading %s images' % len(imageList))
  imageDetails = []
  for image in imageList:
    print(image['_id'])
    imageFileResp = api.get('image/%s/download' % image['_id'])
    imageFileResp.raise_for_status()
    imageFileOutputPath = os.path.join(savePath, '%s.jpg' % image['name'])

    with open(imageFileOutputPath, 'wb') as imageFileOutputStream:
      for chunk in imageFileResp:
        imageFileOutputStream.write(chunk)

  #Get Image MetaData
  outputFileName = 'imagedata'
  for image in imageList:
      # Fetch the full image details
      imageDetail = api.getJson('image/%s' % image['_id'])
      imageDetails.append(imageDetail)

  # Determine the union of all image metadata fields
  metadataFields = set(field 
    for imageDetail in imageDetails
    for field in imageDetail['meta']['clinical'].keys())
  metadataFields = ['isic_id'] + sorted(metadataFields)

  # Write the metadata to a CSV
  with open(outputFileName + '.csv', 'w') as outputStream:
      csvWriter = csv.DictWriter(outputStream, metadataFields)
      csvWriter.writeheader()
      for imageDetail in imageDetails:
          rowDict = imageDetail['meta']['clinical'].copy()
          rowDict['isic_id'] = imageDetail['name']
          csvWriter.writerow(rowDict)

  #splits the dataframe in to different groups (.csv files)
  filename = "imagedata.csv"
  data = pd.read_csv(filename)
  df = pd.DataFrame(data, columns=['isic_id', 'benign_malignant'])
  
  sort = df.groupby('benign_malignant').count()
  print(sort)

  sort_new  = df.sort_values('benign_malignant').assign(NewColumn='NewColumnValue')

  print(sort_new)

  for i, g in df.groupby('benign_malignant'):
    g.to_csv('{}.csv'.format(i), header=False, index_label=False)


