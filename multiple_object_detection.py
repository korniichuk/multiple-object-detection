# -*- coding: utf-8 -*-
# Version: 0.1a2

import cv2 as cv

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

    # Verify 'method'
    if method not in ('cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
            'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED'):
        return 1
    method = eval(method)
