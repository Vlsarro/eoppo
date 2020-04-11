import os
import logging
from eoppo.core.base import BaseObjectProcessingOperator
from eoppo.exceptions import ObjectOperatorError


EXAMPLES_DIR = os.path.dirname(__file__)


class MobilenetV2Classifier(BaseObjectProcessingOperator):

    _dependencies = ('torch==1.4.0', 'torchvision==0.5.0')

    def _initialize(self, device='cpu', **kwargs) -> None:
        super(MobilenetV2Classifier, self)._initialize()

        import torch
        from torchvision import transforms
        self._pkgs['torch'] = torch

        self.device = device
        self.model = torch.hub.load('pytorch/vision:v0.5.0', 'mobilenet_v2', pretrained=True)
        self.model.eval().to(self.device)

        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def _process(self, image, callback=None, **kwargs):
        tensor_img = self.transform(image)
        tensor_img = tensor_img.unsqueeze(0)
        output = self.model(tensor_img.to(self.device))
        label = self._pkgs['torch'].argmax(output, dim=1).cpu().numpy()
        if callback:
            callback(data=label)
        return image


if __name__ == '__main__':
    from PIL import Image

    logging.basicConfig(level=logging.DEBUG)

    mobilenet_v2_classifier = MobilenetV2Classifier()

    test_img = Image.open(os.path.join(EXAMPLES_DIR, '1.jpg'))

    result = []

    try:
        out = mobilenet_v2_classifier.process(ob=test_img, callback=lambda **kwargs: result.append(kwargs))
    except ObjectOperatorError:
        logging.error('Error occurred', exc_info=True)

    mobilenet_v2_classifier.ignore_processing_errors = True
    mobilenet_v2_classifier.process(ob=test_img, callback=lambda **kwargs: result.append(kwargs)).show()

    logging.info('Finished!')
    logging.info(result)
