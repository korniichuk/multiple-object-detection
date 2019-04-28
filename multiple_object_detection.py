# -*- coding: utf-8 -*-
# Version: 0.1a7

from os.path import exists, isfile

import cv2 as cv
import imutils
import numpy as np
from matplotlib import pyplot as plt

def multiple_objects_detection(template, image, scale=1.0,
        method='cv.TM_CCOEFF_NORMED', threshold=0.7, mode='hide'):
    """Multiple object detection. Function compares template against overlapped
       source image regions.
    Input:
        template -- template. Template must be not greater than the source
                    image and have the same data type (required | type: str);
        image -- source image. Source image must be 8-bit or 32-bit
                 floating-point (required | type: str);
        scale -- scale between source image and template. For example 0.5 scale
                 means proportional ratio of source image to template as 1:2
                 (not required | type: float | default: 1.0);
        method -- template matching method of OpenCV Python library
                  (not required | type: str | default: 'cv.TM_CCOEFF_NORMED');

        threshold -- value of thresholding. For example 0.7 threshold means
                     with best matches from 0.7 to 1.0 (>=0.7 and <=1.0);
        mode -- visualization mode. No visualization in 'hide' mode.
                Visualization in Matplotlib with 'matplotlib' mode.
                Visualization in OpenCV with 'opencv' mode (not required |
                type: str | default: 'hide').
    Output:
        result -- coordinates of top left and bottom right points of matched
                  template. Example [[(1, 1), (2, 2)], [(3, 1), (4, 2)]]
                  (type: list);

    """

    result = []
    color = (255, 0, 0) # RGB color model
    thickness = 8 # thickness of line

    # Verify 'method' param
    if method in ('cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
            'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED'):
        method = eval(method)
    else:
        return 1
    # Load template from file
    if exists(template) and isfile(template):
        tmpl = cv.imread(template)
    else:
        return 1
    # Load source image from file
    if exists(image) and isfile(image):
        img = cv.imread(image)
    else:
        return 1
    # Convert template to grayscale color model
    tmpl = cv.cvtColor(tmpl, cv.COLOR_BGR2GRAY)
    # Convert source image to grayscale color model
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Get width and height of template
    th, tw = tmpl.shape
    # Get width and height of source image
    ih, iw = img.shape
    # Check 'scale' param
    if scale == 1:
        resized = tmpl
        rh, rw = th, tw
        r = 1
    else:
        width = int(tw * scale)
        # Resize
        resized = imutils.resize(tmpl, width=width)
        # Get width and height of resized template
        rh, rw = resized.shape
        r = tw / rw
    # If template is bigger than source image, then return empty result
    if (rh > ih) or (rw > iw):
         return result
    # Match template
    match = cv.matchTemplate(img, resized, method)
    # Check 'threshold' param
    if method in [cv.TM_CCOEFF, cv.TM_CCORR, cv.TM_SQDIFF]:
        return result
    elif method  == cv.TM_SQDIFF_NORMED:
        threshold = 1 - threshold
        loc = np.where(match <= threshold)
    else:
        loc = np.where(match >= threshold)
    # Store results of match to 'result'
    for el in zip(*loc[::-1]):
        start_x, start_y = el
        end_x, end_y = int(start_x + tw/r), int(start_y + th/r)
        result.append([(start_x, start_y), (end_x, end_y)])
    # Visualization in Matplotlib
    if mode == 'matplotlib':
        visualization = cv.cvtColor(img, cv.COLOR_GRAY2RGB)
        for el in result:
            start, end = el
            cv.rectangle(visualization, start, end, color, thickness)
        plt.imshow(visualization)
        plt.title('Scale: %s' % scale)
        plt.show()
    return result
