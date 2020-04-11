import os
from eoppo.core.base import BaseObjectProcessingOperator


EXAMPLES_DIR = os.path.dirname(__file__)


class RGB2Gray(BaseObjectProcessingOperator):

    _dependencies = ('numpy',)

    def _process(self, image, callback=None, **kwargs):
        numpy = self._pkgs['numpy']
        return numpy.dot(image[..., :3], [0.2989, 0.5870, 0.1140])

    def _initialize(self, **kwargs) -> None:
        super(RGB2Gray, self)._initialize()
        import numpy
        self._pkgs['numpy'] = numpy


if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.DEBUG)

    rgb2gray = RGB2Gray()

    import pickle
    import numpy as np
    from PIL import Image

    img_processing_module_filepath = os.path.join(EXAMPLES_DIR, 'rbg2gray')

    rgb2gray.save(img_processing_module_filepath)
    with open(img_processing_module_filepath, 'rb') as f:
        loaded_rgb2gray = pickle.load(f)

    test_img = np.asarray(Image.open(os.path.join(EXAMPLES_DIR, '1.jpg')))

    data = loaded_rgb2gray.process(test_img)
    test_img_grayscale = Image.fromarray(data)
    test_img_grayscale.show()

    try:
        os.remove(img_processing_module_filepath)
    except OSError:
        pass
