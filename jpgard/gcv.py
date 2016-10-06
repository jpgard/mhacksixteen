"""
Test script to communicate with Google Cloud Vision API and power image-to-text applications.

See also: 
https://cloud.google.com/vision/docs/quickstart
https://github.com/google/google-api-python-client/blob/master/samples/README.md
https://developers.google.com/api-client-library/python/apis/vision/v1
https://cloud.google.com/vision/docs/face-tutorial


(C) Josh Gardner, jpgard@umich.edu, using sources listed above. All rights reserved.
"""
from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials
import base64
import requests
import json
from PIL import Image
from PIL import ImageDraw


credentials = '../private/client_secret_449014054549-sjf6a30et1nv0ae3oi2qupt882ajvnqa.apps.googleusercontent.com.json'
DISCOVERY_URL='https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'

INPUT_FILE_TEST = 'face_input.jpg'
OUTPUT_FILE_TEST = 'face_output.jpg'

def label_detection():
	"""
	TODO: returns label detection results from GCV API.
	See GCV documentation here: https://cloud.google.com/vision/docs/requests-and-responses#types_of_vision_api_requests
	"""

	return None

def text_detection():
	"""
	TODO: returns text detection results from GCV API.
	See GCV documentation here: https://cloud.google.com/vision/docs/requests-and-responses#types_of_vision_api_requests
	"""


# Create the Service Object
def get_vision_service():
    credentials = GoogleCredentials.get_application_default()
    return discovery.build('vision', 'v1', credentials=credentials,
                           discoveryServiceUrl=DISCOVERY_URL)


# Send a Face Detection Request
def detect_face(face_file, max_results=4):
    """Uses the Vision API to detect faces in the given file.

    Args:
        face_file: A file-like object containing an image with faces.

    Returns:
        An array of dicts with information about the faces in the picture.
    """
    image_content = face_file.read()
    batch_request = [{
        'image': {
            'content': base64.b64encode(image_content).decode('UTF-8')
            },
        'features': [{
            'type': 'FACE_DETECTION',
            'maxResults': max_results,
            }]
        }]

    service = get_vision_service()
    request = service.images().annotate(body={
        'requests': batch_request,
        })
    response = request.execute()

    return response['responses'][0]['faceAnnotations']


def highlight_faces(image, faces, output_filename):
    """Draws a polygon around the faces, then saves to output_filename.

    Args:
      image: a file containing the image with the faces.
      faces: a list of faces found in the file. This should be in the format
          returned by the Vision API.
      output_filename: the name of the image file to be created, where the faces
          have polygons drawn around them.
    """
    im = Image.open(image)
    draw = ImageDraw.Draw(im)

    for face in faces:
        box = [(v.get('x', 0.0), v.get('y', 0.0)) for v in face['fdBoundingPoly']['vertices']]
        draw.line(box + [box[0]], width=5, fill='#00ff00')

    del draw
    im.save(output_filename)



def main(input_filename = INPUT_FILE_TEST, output_filename = OUTPUT_FILE_TEST, max_results = 1):
    with open(input_filename, 'rb') as image:
        faces = detect_face(image, max_results)
        print('Found %s face%s' % (len(faces), '' if len(faces) == 1 else 's'))

        print('Writing to file %s' % output_filename)
        # Reset the file pointer, so we can read the file again
        image.seek(0)
        highlight_faces(image, faces, output_filename)

if __name__ == 'main':

    main()
