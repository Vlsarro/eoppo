from eippm.core.base import BaseImageProcessingModule


class RGB2Gray(BaseImageProcessingModule):

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
    import pickle
    import numpy as np
    from PIL import Image

    logging.basicConfig(level=logging.DEBUG)

    rgb2gray = RGB2Gray()
    rgb2gray.initialize()

    filename = 'rbg2gray'

    rgb2gray.save(filename)
    with open(filename, 'rb') as f:
        loaded_rgb2gray = pickle.load(f)

    test_img = np.asarray(Image.open('1.jpg'))

    data = loaded_rgb2gray.process(test_img)
    test_img_grayscale = Image.fromarray(data)
    test_img_grayscale.show()
