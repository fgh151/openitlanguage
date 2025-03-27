# Opnit Language Plugin for IntelliJ

This plugin provides support for the Opnit programming language in IntelliJ-based IDEs.

## Features

- Syntax highlighting for `.opnit` files
- Basic language support
- File type recognition

## Installation

### From Source

1. Clone this repository
2. Open the project in IntelliJ IDEA
3. Run `./gradlew buildPlugin`
4. Install the plugin from disk:
   - Go to Settings/Preferences > Plugins
   - Click on the gear icon
   - Choose "Install Plugin from Disk..."
   - Select the generated ZIP file from `build/distributions`

## Development

### Prerequisites

- IntelliJ IDEA
- JDK 17 or later
- Kotlin 1.9.20 or later

### Building

```bash
./gradlew build
```

### Running the IDE with the Plugin

```bash
./gradlew runIde
```

## Language Features

The Opnit language supports:
- Basic types: boolean, string, number, any
- Built-in functions: gettype(variable: any), print(str: any)
- Basic operations: +, -, /, *

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 