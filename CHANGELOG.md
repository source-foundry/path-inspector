# Changelog

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
