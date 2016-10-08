# Google Cloud Vision  - Python Scripts

This set of scripts will (hopefully) power the back end of an image-recognition application. These scripts should be compatible with a cloud hosting API service like AWS.

# gcv_label.py

This script fetches labels, text, logos, named entities, relevant wikipedia links, and translated text into a specified destination language from an image.

### Usage example:

`$ python gcv_label.py ./img/article.jpg -d ko -k AIzaSyBHdeK5TxbfowdrbBYw-IclID0oIC5dHaA`
 
<img src = "https://github.com/jpgard/mhacksixteen/blob/master/jpgard/img/article.jpg" width = "175">

```
IMAGE_RESULTS: 


{'data': {'entities': {'New York Times': 'ORGANIZATION',
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
.* entities
.* full_text
.* labels
.* lang
.* logos
.* translation
.* wikipedia


 

