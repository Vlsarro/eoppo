# Embeddable Object Processing Python Operator (EOPPO)
EOPPO is a lightweight library for constructing wrapper classes that do some operations on objects passed to them and pass them further. It is designed to provide a public interface for such classes with embedded exception handling and optional dependency check. It also provides an ability to combine your processing modules into a single pipeline.

Another feature to keep in mind is that each operator could be considered as a distinct module with it's own version and name. Operators are expected to be used for integration into other systems, but you are free to use them standalone.

## Installing
Install with pip:

`pip install git+https://git@github.com/Vlsarro/eoppo.git`

## A Simple Example

Following operator calculates the sum of integers and multiplies them by provided factor

```python
from typing import Callable, List

from eoppo.core.base import BaseObjectProcessingOperator
from eoppo.exceptions import ObjectProcessingError


class SumMultiplyOperator(BaseObjectProcessingOperator):

    def _process(self, ob: List[int], callback: Callable[..., None] = None, m_factor=1, **kwargs) -> int:
        if callback:
            callback(data=len(ob))
        return sum(ob) * m_factor


if __name__ == '__main__':
    op = SumMultiplyOperator()
    try:
        result = op.process([1, 2, 3, 4], m_factor=2, callback=lambda **kw: print(kw))
    except ObjectProcessingError:
        result = 0
```

For more practical examples you can take a look at `/examples` folder. At first this library was related solely to image processing, so examples are also associated with this area.

