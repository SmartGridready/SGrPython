# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [unreleased]

### Fixed

- fixed Modbus data types in write method
- fixed configuration parameter replacement in EID content when certain characters are used

### Added

- implemented Modbus address offset

### Changed

- requires updated SGr specification
- data point "{{value}}" placeholders must be replaced with "\[\[value\]\]"


## [0.3.1] - 2025-04-07

### Fixed

- fixed syntax errors in write method of Modbus interface

### Added

- implemented data point unit


## [0.3.0] - 2025-04-01

### Fixed

- fixed configuration parameter replacement in EID content when certain characters are used

### Added

- Initial "usable" release
- implemented basic Modbus interface
- implemented basic REST interface
- implemented framework for generic, contact and messaging interfaces


## Note about Releases prior to 0.3.0

Releases prior to version 0.3.0 were created in a different package namespace
and were never meant to be used in production.
