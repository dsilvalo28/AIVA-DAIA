import cv2
import os, sys
import numpy as np

save_path = 'images/train/'


# Helpful functions #
def save_image(name, img):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    cv2.imwrite(save_path+name+'.tif', np.array(img, dtype=np.uint8))


def get_api_key():
    if len(sys.argv) is 2:
        print('Reading API key from input argument')
        return sys.argv.pop()
    else:
        try:
            import credentials
            if hasattr(credentials, 'GOOGLE_MAPS_API_KEY'):
                print('Reading API key from credentials.py')
                return credentials.GOOGLE_MAPS_API_KEY
        except:
            if 'GOOGLE_MAPS_API_KEY' in os.environ:
                print('Reading API key from environment')
                return os.environ['GOOGLE_MAPS_API_KEY']
            else:
                print('API Key not found.')
                sys.exit(1)