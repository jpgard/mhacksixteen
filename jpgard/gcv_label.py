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



def detect_labels(photo_file, print_output = False, nl = 1):
    """
    Run a label request on a single image

    :param photo_file:
    :param print_output:
    :param nl:
    :return:
    """

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
        try:
            labels = [x['description'] for x in response['responses'][0]['labelAnnotations']]
        except KeyError:
            pass
        if print_output:
            print('Found labels in %s:\n \n %s \n \n' % (photo_file, '\n'.join(labels)))

        return labels


def detect_text(photo_file, print_output = False):
    """
    Run OCR request on a single image.
    :param photo_file:
    :param print_output:
    :return:
    """
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
                    'maxResults': 10
                }]
            }]
        })
        response = service_request.execute()
        import ipdb;ipdb.set_trace()
        try:
            full_text = response['responses'][0]['textAnnotations'][0]['description']
        except KeyError:
            pass

        if print_output and full_text:
            print('Found text in %s:\n \n %s' % (photo_file, full_text))

        elif print_output:
            print('No text found in your image.')

        return full_text

def detect_image_info(photo_file, print_output = False, nlab = 1, nlogo = 1):
    """
    Detect text and labels in photo_file.
    :param photo_file:
    :param print_output:
    :param nlab:
    :param nlogo:
    :return:

    TODO: implement this function
    """
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)

    with open(photo_file, 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [
                {
                    'type': 'LABEL_DETECTION',
                    'maxResults': nlab
                },
                {
                    'type': 'TEXT_DETECTION',
                    'maxResults': 1
                },
                {
                    'type': 'LOGO_DETECTION',
                    'maxResults': nlogo
                }
                ]
            }]
        })
        response = service_request.execute()

        try:
            full_text = response['responses'][0]['textAnnotations'][0]['description']
        except KeyError:
            pass
        try:
            labels = [x['description'] for x in response['responses'][0]['labelAnnotations']]
        except KeyError:
            pass
        try:
            logos = [x['description'] for x in response['responses'][0]['logoAnnotations']]
        except KeyError:
            pass

        if print_output:
            if labels:
                print('Found labels in %s:\n \n %s \n \n' % (photo_file, '\n'.join(labels)))
            if full_text:
                print('Found text in %s:\n \n %s' % (photo_file, full_text))
            if logos:
                print('Found logos in %s:\n \n %s \n \n' % (photo_file, '\n'.join(logos)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', help='The image you\'d like to label.')
    parser.add_argument('-nla', help='The number of labels you\'d like returned', default = 10)
    parser.add_argument('-nlo', help='The number of logos you\'d like returned', default = 10)
    args = parser.parse_args()
    # detect_labels(args.image_file, print_output = True, nl = args.nl)
    # detect_text(args.image_file, print_output=True)
    detect_image_info(args.image_file, print_output=True, nlab = args.nla, nlogo = args.nlo)

