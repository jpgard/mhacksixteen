# Google Cloud Vision  - Python Scripts

This set of scripts will (hopefully) power the back end of an image-recognition application. These scripts should be compatible with a cloud hosting API service like AWS.

# gcv_label.py

This script fetches labels and text from an image. Currently, it fetches one label (this will be changed to a user-specified parameter), and returns all text detected in the image.

### Usage example:

`$ python gcv_label.py ./img/article.jpg -nl 10`

```
Found labels in ./img/article.jpg:
 
 color
font
product
circle
brand
shape
presentation 
 

Found text in ./img/article.jpg:
 
 ooo Verizon
10:39 PM
By SABRINA TAVERNISE APRIL 20, 2016
Oriana Koren for The New York Times
<strong>Misconception:
strong> Juice cleansing can
remove toxins from wour
system.
Actually: To say that drinking juice
detoxifies the body isn't quite the
same as claiming leeches suck out
poisons, but it's fairly close.
 ```
 
<img src = "https://github.com/jpgard/mhacksixteen/blob/master/jpgard/img/article.jpg" width = "175">

### Another example:

`$ python gcv_label.py ./img/motorcycle.jpg -nl 10`

```
Found labels in ./img/motorcycle.jpg:
 
 car
vehicle
land vehicle
motorcycle
motorcycling
stunt performer
automobile make
stunt
chopper 


No text found in your image.
```

<img src = "https://github.com/jpgard/mhacksixteen/blob/master/jpgard/img/motorcycle.jpg" width = "175">


# JSON response format

The response returned is a [JSEND-compliant](https://labs.omniti.com/labs/jsend) JSON response that looks like this:

```{'data': {'full_text': 'E adidas\n2558\n2011 BOSTON\nthe future is yours\n',
          'labels': ['human action',
                     'sports',
                     'jumping',
                     'endurance sports',
                     'athletics',
                     'physical exercise'],
          'logos': None},
 'message': None,
 'status': 'success'}
 ```
 * status: the status of your response (hopefully 'success', otherwise 'error').
 * data: nested field of any data returned for the response (logos, text, labels, etc.).
 * message: an error message, if applicable; otherwise None.
 

