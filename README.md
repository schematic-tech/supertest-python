# Supertest for Python

```sh
python -m pip install schematic-supertest
```

```python
from schematic import *

@supertest
def integer_division_is_bounded(value: int, divisor: int):
    assume(value >= 0 and divisor > 0)
    assert value // divisor <= value
```

See the [Getting Started Documentation](https://docs.schematic.tech/pup).

## License

This library is available under either MIT or Apache-2.0, at your option.
