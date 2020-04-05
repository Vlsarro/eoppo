import logging
import pickle
import numpy as np
from PIL import Image
from eippm.core.base import BaseImageProcessingModule


class RGB2Gray(BaseImageProcessingModule):

    def _process(self, image, callback=None, **kwargs):
        return np.dot(image[..., :3], [0.2989, 0.5870, 0.1140])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    rgb2gray = RGB2Gray()
    rgb2gray.initialize()

    filename = 'rbg2gray'

    rgb2gray.save(filename)
    with open(filename, 'rb') as f:
        loaded_rgb2gray = pickle.load(f)

    lenna_img = np.asarray(Image.open('1.jpg'))

    data = loaded_rgb2gray.process(lenna_img)
    lenna_img_grayscale = Image.fromarray(data)
    lenna_img_grayscale.show()
