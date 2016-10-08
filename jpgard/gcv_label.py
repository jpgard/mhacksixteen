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
import httplib2

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from google.cloud import translate

def gt(text, api_key, print_output = False, dest_lang = None):
    """
    Translates text to dest_lang using Google Translate API.
    """

    # Instantiates a client
    translate_client = translate.Client(api_key)
    # translates with client
    translation = translate_client.translate(text, target_language=dest_lang)

    return translation

def gnl(text, print_output = False, dest_lang = None, api_key = None):
    """
    Connect to Google Natural Language API; fetch named entities and translate (if dest_lang does not match language of text).
    See Google sample scripts here for more information: https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/language/ocr_nl/main.py

    :param text:
    :param print_output:
    :param dest_lang:
    :param api_key: Optional API key for google translate API (required for translation)
    """
    response_out = None
    entities = None
    entities_dict = None
    lang = None
    
    # get credentials and connect to GNL API
    credentials = GoogleCredentials.get_application_default()
    scoped_credentials = credentials.create_scoped(['https://www.googleapis.com/auth/cloud-platform'])
    http = httplib2.Http()
    scoped_credentials.authorize(http)
    service = discovery.build('language', 'v1beta1', http=http)

    # fetch named entities
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        },
        'encodingType': 'UTF8',
    }
    entities = []
    try:
        request = service.documents().analyzeEntities(body=body)
        response = request.execute()
        entities = response['entities']
        entities_dict = {e.get('name'): e.get('type') for e in entities}
        wikipedia_dict = {e.get('name'): e.get('metadata').get('wikipedia_url') for e in entities
                          if e.get('metadata').get('wikipedia_url')}
        lang = response.get('language')
    # except errors.HttpError as e:
    #     #TODO
    #     pass
    except KeyError as e2:
        #TODO
        pass

    if dest_lang != lang:
        translation = gt(text, api_key)

    import ipdb; ipdb.set_trace()


    # if dest_lang != text language, translate to text_lang

    # build response

    return response_out


def gcv(photo_file, print_output = False, nlab = 1, nlogo = 1, return_type = 'json', translate =
None):
    """
    Detect text and labels in photo_file.
    :param photo_file:
    :param print_output:
    :param nlab:
    :param nlogo:
    :param translate: language to translate text to (if text is already in this language,
    returns untranslated text).
    :return:

    """
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)
    # initialize output variables
    full_text = None
    labels = None
    logos = None

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
        gcv_response = service_request.execute()
        # check if error in GCV response; if so, return a response with the error message
        if 'error' in gcv_response['responses']:
            response_out = {
                'status': 'error',
                'data': None,
                'message': response['error']['message']
            }

            return response_out

        # extract relevant data from gcv response
        try:
            full_text = gcv_response['responses'][0]['textAnnotations'][0]['description']
        except KeyError:
            pass
        try:
            labels = [x['description'] for x in gcv_response['responses'][0]['labelAnnotations']]
        except KeyError:
            pass
        try:
            logos = [x['description'] for x in gcv_response['responses'][0]['logoAnnotations']]
        except KeyError:
            pass


        # get named entitites and translate text, if requested
        if full_text:
            clean_text = full_text.replace('\n', ' ')
            response_gnl = gnl(full_text, print_output=True, dest_lang='CN')


        # construct JSEND-compliant JSON response (see https://labs.omniti.com/labs/jsend for
        # more info on this format)

        response_out = {
            'status': 'success',
            'data': {
                'full_text': full_text,
                'labels': labels,
                'logos': logos
            },
            'message': None
        }

        # print output; if requested
        if print_output:
            if labels:
                print('Found labels in %s:\n \n%s \n \n' % (photo_file, '\n'.join(labels)))
            else:
                print('No labels found.')
            if full_text:
                print('Found text in %s:\n \n%s' % (photo_file, full_text))
            else:
                print('No text found.')
            if logos:
                print('Found logos in %s:\n \n%s \n \n' % (photo_file, '\n'.join(logos)))
            else:
                print('No logos found.')

        return response_out


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', help='The image you\'d like to label.')
    parser.add_argument('-nla', help='The number of labels you\'d like returned', default = 10)
    parser.add_argument('-nlo', help='The number of logos you\'d like returned', default = 10)
    parser.add_argument('-r', help='The return type; currently only json is supported', default=
    'json')
    parser.add_argument('-d', help='Destination language')
    parse.add_argument('-k', help = 'Google Translate API Key', required = True)
    args = parser.parse_args()
    response_out = gcv(args.image_file, print_output=True,nlab = args.nla,
                                     nlogo = args.nlo, return_type = args.r)
    import ipdb; ipdb.set_trace()

