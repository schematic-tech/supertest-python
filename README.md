# Supertest for Python

The distribution is `schematic-supertest`; import it as `schematic`.
Install from this repository until a registry release exists:

```sh
python3 -m pip install -e .
```

```python
from schematic import *

@supertest
def integer_division_is_bounded(value: int, divisor: int):
    assume(value >= 0 and divisor > 0)
    assert value // divisor <= value
```

Explicit imports (`from schematic import assume, supertest`) and qualified names
(`@schematic.supertest`, `schematic.assume(...)`) also work at runtime. Current Pup
documentation requires the star import for discovery of the bare decorator.

The decorator preserves the original callable and attaches immutable metadata.
`is_supertest` and `metadata_of` expose it; duplicate markers and marker arguments
are rejected. Marked functions are excluded from pytest collection.

A true assumption continues. `assume(False, message=None)` raises `AssumptionNotMet`,
a `SystemExit` subclass with `code == 0`. Uncaught on the main thread, it exits
successfully without a traceback. The optional message is available as `.message`.
Run one input per process; this does not generate inputs or prove properties.

Python caveat: `SystemExit` can be intercepted, cleanup in `finally` blocks still
runs, and raising it on a worker thread only terminates that thread. Use the main
thread without catching `SystemExit`/`BaseException`, or explicitly catch
`AssumptionNotMet` in a runner that classifies rejected inputs. Ordinary
`except Exception` handlers do not catch it. This changes the base class from the
old library, which treated rejection as an ordinary exception.

```sh
python3 -m unittest discover -s tests -v
```

Requires Python 3.11+. Adapted from `schematic-tech/schematic-supertests` at
`b6ccba3b5e0d42ea2846d0476eeb9496afb4a7f4`.

## Distribution

The public package name is singular: `schematic-supertest` on PyPI.

```sh
python -m pip install schematic-supertest
```

It supplies the same `schematic` import package. Releases contain a platform-neutral
wheel and a source distribution, each carrying both license texts and typing metadata.
See [release automation and PyPI setup](RELEASING.md).

## License

This interoperability library is available under either [MIT](LICENSE-MIT) or
[Apache-2.0](LICENSE-APACHE), at your option.
