"""Supertest markers and successful termination for rejected inputs."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")
SupertestFunction = Callable[P, R]
_METADATA_ATTRIBUTE = "__schematic_supertest__"


class AssumptionNotMet(SystemExit):
    """Reject an input with exit status zero, without an assertion failure.

    Like SystemExit, this can be intercepted explicitly by a local runner.
    Ordinary ``except Exception`` handlers do not catch it.
    """

    def __init__(self, message: str | None = None) -> None:
        super().__init__(0)
        self.message = message or "Supertest assumption not met"

    def __str__(self) -> str:
        return self.message


@dataclass(frozen=True, slots=True)
class SupertestMetadata:
    """Immutable marker metadata attached to an otherwise unchanged function."""


def supertest(
    function: SupertestFunction[P, R],
    /,
) -> SupertestFunction[P, R]:
    """Mark a function as a Supertest without wrapping or executing it."""

    if not callable(function):
        raise TypeError("@schematic.supertest can decorate only callables")
    if hasattr(function, _METADATA_ATTRIBUTE):
        raise ValueError("a function cannot carry more than one @schematic.supertest")
    setattr(function, _METADATA_ATTRIBUTE, SupertestMetadata())
    function.__test__ = False  # type: ignore[attr-defined]
    return function


def assume(condition: bool, message: str | None = None) -> None:
    """Continue if true; otherwise raise AssumptionNotMet with exit status zero.

    Run one input per process, on its main thread, without intercepting SystemExit.
    Python still executes finally blocks while unwinding.
    """

    if not condition:
        raise AssumptionNotMet(message)


def is_supertest(function: object) -> bool:
    """Return whether a callable carries Schematic Supertest metadata."""

    return isinstance(getattr(function, _METADATA_ATTRIBUTE, None), SupertestMetadata)


def metadata_of(function: object) -> SupertestMetadata:
    """Return marker metadata from a Supertest callable."""

    metadata = getattr(function, _METADATA_ATTRIBUTE, None)
    if not isinstance(metadata, SupertestMetadata):
        raise TypeError("object is not a Schematic Supertest")
    return metadata
