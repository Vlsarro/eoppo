import os
import logging
import pickle
import numpy as np
from PIL import Image
from eippm.core.base import BaseImageProcessingModule


EXAMPLES_DIR = os.path.dirname(__file__)


class RGB2Gray(BaseImageProcessingModule):

    def _process(self, image, callback=None, **kwargs):
        return np.dot(image[..., :3], [0.2989, 0.5870, 0.1140])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    rgb2gray = RGB2Gray()

    img_processing_module_filepath = os.path.join(EXAMPLES_DIR, 'rbg2gray')

    rgb2gray.save(img_processing_module_filepath)
    with open(img_processing_module_filepath, 'rb') as f:
        loaded_rgb2gray = pickle.load(f)

    test_img = np.asarray(Image.open(os.path.join(EXAMPLES_DIR, '1.jpg')))

    data = loaded_rgb2gray.process(test_img)
    test_img_grayscale = Image.fromarray(data)
    test_img_grayscale.show()
