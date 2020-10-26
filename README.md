# Path Inspector

[![PyPI](https://img.shields.io/pypi/v/pathins?color=blueviolet&label=PyPI&logo=python&logoColor=white)](https://pypi.org/project/pathins)
![Python CI](https://github.com/source-foundry/path-inspector/workflows/Python%20CI/badge.svg)
![Python Lints](https://github.com/source-foundry/path-inspector/workflows/Python%20Lints/badge.svg)
![Python Type Checks](https://github.com/source-foundry/path-inspector/workflows/Python%20Type%20Checks/badge.svg)
[![codecov](https://codecov.io/gh/source-foundry/path-inspector/branch/master/graph/badge.svg)](https://codecov.io/gh/source-foundry/path-inspector)

Path Inspector is a quadratic font curve path inspection application.  The Python package installs the `pathins` command line executable and requires a Python v3.6+ interpreter.

The following sub-commands are available:

- `contours`: path contour number report (as of v0.4.0)
- `coordinates`: path coordinates report (as of v0.3.0)
- `direction`: outermost contour path direction report (as of v0.2.0)
- `path`: curve path report
- `segments`: curve segment report, with line distances and quadratic curve arc lengths (as of v0.5.0)

## Installation

pathins requires a Python 3.6+ interpreter.

Installation in a Python3 virtual environment is recommended.

Use any of the following installation approaches:

### pip install from PyPI

```
$ pip3 install pathins
```

### pip install from source

```
$ git clone https://github.com/source-foundry/path-inspector.git
$ cd path-inspector
$ pip3 install -r requirements.txt .
```

### Developer install from source

The following approach installs the project and associated optional developer dependencies, so that source changes are available without the need for re-installation.

```
$ git clone https://github.com/source-foundry/path-inspector.git
$ cd path-inspector
$ pip3 install --ignore-installed -r requirements.txt -e ".[dev]"
```

## Usage

```
$ pathins [OPTIONS] [FILEPATH] [OPTIONAL GLYPH NAME]
```

See `pathins --help` for additional details.

## Issues

Please report issues on the [project issue tracker](https://github.com/source-foundry/path-inspector/issues).

## Contributing

Contributions are warmly welcomed.  A development dependency environment can be installed in editable mode with the developer installation documentation above.

Please use the standard Github pull request approach to propose source changes.

### Source file linting

Python source files are linted with `flake8`.  See the Makefile `test-lint` target for details.

### Testing

The project runs continuous integration testing on the GitHub Actions service with the `pytest` toolchain.  Test modules are located in the `tests` directory of the repository.

Local testing by Python interpreter version can be performed with the following command executed from the root of the repository:

```
$ tox -e [PYTHON INTERPRETER VERSION]
```

Please see the `tox` documentation for additional details.

### Test coverage

Unit test coverage is executed with the `coverage` tool.  See the Makefile `test-coverage` target for details.

## Acknowledgments

The Path Inspector project is built with the fantastic [fontTools](https://github.com/fonttools/fonttools) and [skia-pathops](https://github.com/fonttools/skia-pathops) free software libraries.

## License

Copyright 2020 Source Foundry Authors and Contributors

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.