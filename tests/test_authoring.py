from __future__ import annotations

import subprocess
import sys
import unittest

import schematic


class AuthoringTests(unittest.TestCase):
    def test_decorator_preserves_and_marks_function(self) -> None:
        def original(value: int) -> int:
            return value + 1

        decorated = schematic.supertest(original)

        self.assertIs(decorated, original)
        self.assertEqual(decorated(2), 3)
        self.assertTrue(schematic.is_supertest(original))
        self.assertIs(original.__test__, False)
        self.assertEqual(schematic.metadata_of(original), schematic.SupertestMetadata())

    def test_star_import_exports_authoring_vocabulary(self) -> None:
        namespace: dict[str, object] = {}
        exec("from schematic import *", namespace)

        self.assertIs(namespace["supertest"], schematic.supertest)
        self.assertIs(namespace["assume"], schematic.assume)

    def test_qualified_decorator_is_supported(self) -> None:
        @schematic.supertest
        def claim(value: int) -> None:
            assert value == value

        self.assertTrue(schematic.is_supertest(claim))

    def test_duplicate_marker_is_rejected(self) -> None:
        @schematic.supertest
        def claim() -> None:
            return None

        with self.assertRaisesRegex(ValueError, "more than one"):
            schematic.supertest(claim)

    def test_decorator_arguments_are_rejected(self) -> None:
        with self.assertRaises(TypeError):
            schematic.supertest()  # type: ignore[call-arg]
        with self.assertRaises(TypeError):
            schematic.supertest(description="claim")  # type: ignore[call-arg]

    def test_assume_accepts_admitted_input(self) -> None:
        self.assertIsNone(schematic.assume(True))

    def test_assume_rejects_out_of_domain_input(self) -> None:
        with self.assertRaisesRegex(schematic.AssumptionNotMet, "positive input") as raised:
            schematic.assume(False, "positive input required")
        self.assertIsInstance(raised.exception, SystemExit)
        self.assertNotIsInstance(raised.exception, Exception)
        self.assertEqual(raised.exception.code, 0)

    def test_false_assumption_exits_successfully(self) -> None:
        result = subprocess.run(
            [sys.executable, "-c", """
from schematic import assume, supertest

def helper() -> int:
    assume(False, 'positive input required')
    raise AssertionError('helper continued')

@supertest
def claim() -> None:
    try:
        helper()
    except Exception:
        print('caught as failure')
    print('continued')
    raise SystemExit(91)

print('entered')
claim()
raise SystemExit(92)
"""],
            capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "entered\n")
        self.assertEqual(result.stderr, "")

    def test_assumption_does_not_suppress_assertions(self) -> None:
        result = subprocess.run(
            [sys.executable, "-c", "from schematic import assume; assume(True); "
             "assert False, 'ordinary assertion failure'"],
            capture_output=True, text=True, timeout=10,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ordinary assertion failure", result.stderr)

    def test_metadata_of_rejects_an_ordinary_function(self) -> None:
        def ordinary() -> None:
            return None

        with self.assertRaisesRegex(TypeError, "not a Schematic Supertest"):
            schematic.metadata_of(ordinary)


if __name__ == "__main__":
    unittest.main()
