# Changelog

## v0.5.1

- minor documentation and project description updates

## v0.5.0

- add `segments` sub-command with glyph segment line distance and arc length reporting
- performance improvement: removed `sys.stdout.isatty()` check from loops in stringbuilder module
- fix: do not apply ANSI color escapes when we are not in a TTY, includes cyan_text, cyan_bright_text, green_text, and red_text functions in the stringbuilder module
- add `--pretty` mypy option to Makefile type checking target
- add line length = 90 definition to the isort import sorting Makefile target
- bump fontTools dependency to v4.16.1

## v0.4.0

- add `contours` sub-command with glyph contour number reporting
- change bold cyan glyph name color to bright bold cyan for sub-commands that use this color
- add `stringbuilder.cyan_text` function
- add `stringbuilder.cyan_bright_text` function

## v0.3.1

- source cleanup
- remove report module
- remove unnecessary import statements
- fix README typo

## v0.3.0

- add `coordinates` sub-command with path begin, on-curve, off-curve, and end coordinate reporting
- refactor `stringbuilder.path_header` function to `stringbuilder.report_header`
- add `stringbuilder.green_text` function
- add `stringbuilder.red_text` function
- broaden type annotations across Python sources

## v0.2.0

- add `direction` sub-command with path direction reporting
- bump fontTools dependency to v4.16.0
- bump skia-pathops dependency to v0.5.1
- add `import-sort` Makefile target
- add NotoSans subset test files

## v0.1.0

- initial release with `path` sub-command
