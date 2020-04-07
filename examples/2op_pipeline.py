import os
from eippm.core.base import BaseImageProcessingModule
from eippm.core.pipeline import ImageProcessingModulesPipeline


EXAMPLES_DIR = os.path.dirname(__file__)


class RotationOperator(BaseImageProcessingModule):

    # rotation code is from https://codereview.stackexchange.com/a/41903

    _dependencies = ('numpy',)

    def _process(self, image, callback=None, angle=90, **kwargs):
        return self._rotate_image(image, angle * self._pkgs['numpy'].pi / 180, 100, 100)

    def _initialize(self, **kwargs) -> None:
        super(RotationOperator, self)._initialize()
        import numpy
        self._pkgs['numpy'] = numpy

    def _rotate_coords(self, x, y, theta, ox, oy):
        """Rotate arrays of coordinates x and y by theta radians about the
        point (ox, oy).
        """
        s, c = self._pkgs['numpy'].sin(theta), self._pkgs['numpy'].cos(theta)
        x, y = self._pkgs['numpy'].asarray(x) - ox, self._pkgs['numpy'].asarray(y) - oy
        return x * c - y * s + ox, x * s + y * c + oy

    def _rotate_image(self, src, theta, ox, oy, fill=255):
        """Rotate the image src by theta radians about (ox, oy).
        Pixels in the result that don't correspond to pixels in src are
        replaced by the value fill.
        """
        # Images have origin at the top left, so negate the angle.
        theta = -theta

        # Dimensions of source image. Note that scipy.misc.imread loads
        # images in row-major order, so src.shape gives (height, width).
        sh, sw = src.shape

        # Rotated positions of the corners of the source image.
        cx, cy = self._rotate_coords([0, sw, sw, 0], [0, 0, sh, sh], theta, ox, oy)

        # Determine dimensions of destination image.
        dw, dh = (int(self._pkgs['numpy'].ceil(c.max() - c.min())) for c in (cx, cy))

        # Coordinates of pixels in destination image.
        dx, dy = self._pkgs['numpy'].meshgrid(self._pkgs['numpy'].arange(dw), self._pkgs['numpy'].arange(dh))

        # Corresponding coordinates in source image. Since we are
        # transforming dest-to-src here, the rotation is negated.
        sx, sy = self._rotate_coords(dx + cx.min(), dy + cy.min(), -theta, ox, oy)

        # Select nearest neighbour.
        sx, sy = sx.round().astype(int), sy.round().astype(int)

        # Mask for valid coordinates.
        mask = (0 <= sx) & (sx < sw) & (0 <= sy) & (sy < sh)

        # Create destination image.
        dest = self._pkgs['numpy'].empty(shape=(dh, dw), dtype=src.dtype)

        # Copy valid coordinates from source image.
        dest[dy[mask], dx[mask]] = src[sy[mask], sx[mask]]

        # Fill invalid coordinates.
        dest[dy[~mask], dx[~mask]] = fill

        return dest


class RGB2GrayOperator(BaseImageProcessingModule):

    _dependencies = ('numpy',)

    def _process(self, image, callback=None, **kwargs):
        numpy = self._pkgs['numpy']
        return numpy.dot(image[..., :3], [0.2989, 0.5870, 0.1140])

    def _initialize(self, **kwargs) -> None:
        super(RGB2GrayOperator, self)._initialize()
        import numpy
        self._pkgs['numpy'] = numpy


if __name__ == '__main__':
    import logging
    import pickle
    import numpy as np
    from PIL import Image

    logging.basicConfig(level=logging.DEBUG)

    pipeline = ImageProcessingModulesPipeline([RGB2GrayOperator(), RotationOperator()])

    test_img = np.asarray(Image.open(os.path.join(EXAMPLES_DIR, '1.jpg')))

    result = pipeline.run(test_img)

    test_img_rotated_grayscale = Image.fromarray(result)
    test_img_rotated_grayscale.show()

    pipeline_filepath = os.path.join(EXAMPLES_DIR, '2op_pipeline')

    pipeline.save(pipeline_filepath)
    with open(pipeline_filepath, 'rb') as f:
        loaded_pipeline = pickle.load(f)

    result = pipeline.run(test_img, call_params={
        1: {
            'params': {'angle': 210}
        }
    })

    test_img_rotated_grayscale = Image.fromarray(result)
    test_img_rotated_grayscale.show()

    try:
        os.remove(pipeline_filepath)
    except OSError:
        pass
