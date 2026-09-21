# Supertest for Python

```sh
python -m pip install schematic-supertest
```

From the [text-tools example](examples/text-tools):

```python
from schematic import *

from text_tools.text import collapse_spaces


@supertest
def collapsing_spaces_again_changes_nothing(text: str):
    once = collapse_spaces(text)
    twice = collapse_spaces(once)

    assert twice == once
```

See the [Getting Started Documentation](https://docs.schematic.tech/pup).

## Example

Try [text-tools](https://github.com/schematic-tech/supertest-python/tree/main/examples/text-tools). It includes a supertest
that finds a space-normalization bug.

## License

This library is available under either MIT or Apache-2.0, at your option.
