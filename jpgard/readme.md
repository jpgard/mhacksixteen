# Google Cloud Vision  - Python Scripts

This set of scripts will (hopefully) power the back end of an image-recognition application. These scripts should be compatible with a cloud hosting API service like AWS.

# gcv_label.py

This script fetches labels, text, logos, named entities, relevant wikipedia links, and translated text into a specified destination language from an image.

### Usage example:

`$ python gcv_label.py ./img/article.jpg -d ko -k AIzaSyBHdeK5TxbfowdrbBYw-IclID0oIC5dHaA`
 
<img src = "https://github.com/jpgard/mhacksixteen/blob/master/jpgard/img/article.jpg" width = "175">

```
IMAGE_RESULTS: 


{'data': {'dest_lang': 'ko',
          'entities': {'New York Times': 'ORGANIZATION',
                       'Oriana Koren': 'PERSON',
                       'SABRINA TAVERNISE': 'PERSON',
                       'Verizon': 'ORGANIZATION'},
          'full_text': 'ooo Verizon\n'
                       '10:39 PM\n'
                       'By SABRINA TAVERNISE APRIL 20, 2016\n'
                       'Oriana Koren for The New York Times\n'
                       '<strong>Misconception:\n'
                       'strong> Juice cleansing can\n'
                       'remove toxins from wour\n'
                       'system.\n'
                       'Actually: To say that drinking juice\n'
                       "detoxifies the body isn't quite the\n"
                       'same as claiming leeches suck out\n'
                       "poisons, but it's fairly close.\n",
          'labels': ['color',
                     'font',
                     'product',
                     'circle',
                     'brand',
                     'shape',
                     'presentation'],
          'lang': 'en',
          'logos': None,
          'translation': 'OOO 버라이존 뉴욕 타임즈 <strong>오해에</strong> 대한 SABRINA '
                         'TAVERNISE 2016년 4월 20일 오리 아나 코렌으로 10:39 오후 <strong>: '
                         '강한&gt; 주스 클렌징 wour 시스템에서 독소를 제거 할 수 있습니다. 사실 : 주스를 '
                         '마시는 것은 몸에 거머리가 독을 빨아 주장과 완전히 동일하지 해독, 그러나 그것은 '
                         '사실이다라고합니다.</strong>',
          'wikipedia': {'New York Times': 'http://en.wikipedia.org/wiki/The_New_York_Times',
                        'Verizon': 'http://en.wikipedia.org/wiki/Verizon_Communications'}},
 'message': None,
 'status': 'success'}

```

# JSON response format

The response returned is a [JSEND-compliant](https://labs.omniti.com/labs/jsend) JSON response; an example is shown above.

* status: the status of your response (hopefully 'success', otherwise 'error').
* message: an error message, if applicable; otherwise None.
* data: nested field of any data returned for the response (logos, text, labels, etc.).
  * entities: [named entities](https://en.wikipedia.org/wiki/Named-entity_recognition) recognized in the image text.
  * wikipedia: wikipedia links for relevant named entities.
  * full_text: the full text detected in the image.
  * labels: labels associated with the image or objects detected within the image (i.e., 'car', 'automobile', 'driver', 'person').
  * lang: language of the text.
  * logos: names of any brand logos detected within the image.
  * dest_lang: destination language (the language the user requested the text to be translated into).
  * translation: text translated into destination language.


 
If you are interested in writing a similar script, here are some resources I used to get started (in no particular order):

https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/language/ocr_nl/main.py
https://cloud.google.com/natural-language/
https://cloud.google.com/translate/v2/quickstart#translate-text
https://cloud.google.com/vision/docs/best-practices
https://cloud.google.com/translate/docs/reference/libraries
https://cloud.google.com/vision/docs/
https://cloud.google.com/vision/docs/samples
https://cloud.google.com/vision/docs/requests-and-responses#types_of_vision_api_requests
