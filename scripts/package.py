#!/usr/bin/env python3
"""Build and test the wheel and sdist that will be released."""
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import venv
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def run(*args):
    subprocess.run(args, cwd=ROOT, check=True)


run(sys.executable, "scripts/release.py", "check")
run(sys.executable, "-m", "build")
artifacts = [*ROOT.glob("dist/*.whl"), *ROOT.glob("dist/schematic_supertest-*.tar.gz")]
assert len(artifacts) == 2, "clean dist/ before building a release"
run(sys.executable, "-m", "twine", "check", *map(str, artifacts))
wheel = next(ROOT.glob("dist/*.whl"))
with zipfile.ZipFile(wheel) as package:
    names = package.namelist()
    for suffix in ("schematic/py.typed", "/licenses/LICENSE-MIT", "/licenses/LICENSE-APACHE"):
        assert any(name.endswith(suffix) for name in names), suffix
sdist = next(ROOT.glob("dist/schematic_supertest-*.tar.gz"))
with tarfile.open(sdist) as package:
    names = package.getnames()
    assert any(name.endswith("/tests/test_authoring.py") for name in names)
    assert any(name.endswith("/LICENSE-MIT") for name in names)
    assert any(name.endswith("/LICENSE-APACHE") for name in names)
for artifact in artifacts:
    with tempfile.TemporaryDirectory(prefix="supertest-python-install-") as temporary:
        environment = Path(temporary) / "venv"
        venv.EnvBuilder(with_pip=True).create(environment)
        python = environment / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
        run(str(python), "-m", "pip", "install", str(artifact))
        run(str(python), "-m", "unittest", "discover", "-s", "tests", "-v")
