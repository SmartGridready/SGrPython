# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2025-10-01

### Fixed

- validator is chosen according to data point type
- REST interface can return JSON as string

### Added

- implemented REST interface basic authentication
- implemented dynamic parameters in REST calls
- scaling of Modbus data point values
- implemented MQTT messaging interface
- implemented JMESpath mappings in response queries and message filters
- implemented regex in response queries and message filters

### Changed

- requires updated SGr specification `2.1.20250902`
- updated dependencies
- modified `subscribe()` method to provide reference to data point
- improved bearer authentication process


## [0.3.1] - 2025-04-16

### Fixed

- fixed syntax errors in write method of Modbus interface
- fixed Modbus data types in write method
- fixed configuration parameter substitution in EID content when certain characters are used

### Added

- implemented data point unit

## Changed

- data point "{{value}}" placeholders must be replaced with "\[\[value\]\]"
- implemented Modbus address offset


## [0.3.0] - 2025-04-01

### Fixed

- fixed configuration parameter substitution in EID content when certain characters are used

### Added

- Initial "usable" release
- implemented basic Modbus interface
- implemented basic REST interface
- implemented framework for generic, contact and messaging interfaces


## Note about Releases prior to 0.3.0

Releases prior to version 0.3.0 were created in a different package namespace
and were never meant to be used in production.
