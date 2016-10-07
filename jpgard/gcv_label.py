'''
Returns label from picture file.
Run the script on an image to get a label, E.g.:

 $   gcv.py <path-to-image>

Before running, make sure you have set up application default credentials as described here:
https://cloud.google.com/vision/docs/common/auth#using-api-manager

And then run:
$ export GOOGLE_APPLICATION_CREDENTIALS=<path_to_your_credentials>.json

Install dependencies using:
$ pip install --upgrade google-api-python-client
$ pip install Pillow

'''


import argparse
import base64

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials



def detect_labels(photo_file, nl):
    """Run a label request on a single image"""

    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)

    with open(photo_file, 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': nl
                }]
            }]
        })
        response = service_request.execute()
        labels = [x['description'] for x in response['responses'][0]['labelAnnotations']]
        print('Found labels in %s:\n \n %s \n \n' % (photo_file, '\n'.join(labels)))



def detect_text(photo_file):
    """Run OCR request on a single image."""
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)

    with open(photo_file, 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'TEXT_DETECTION',
                    'maxResults': 1
                }]
            }]
        })
        response = service_request.execute()
        try:
            full_text = response['responses'][0]['textAnnotations'][0]['description']
            print('Found text in %s:\n \n %s' % (photo_file, full_text))
        except KeyError:
            print('No text found in your image.')



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', help='The image you\'d like to label.')
    parser.add_argument('-nl', help='The number of labels you\'d like returned')
    args = parser.parse_args()
    detect_labels(args.image_file, args.nl)
    detect_text(args.image_file)

