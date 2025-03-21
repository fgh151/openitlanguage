# Opnit Language Support for JetBrains IDEs

This plugin provides syntax highlighting support for the Opnit programming language in JetBrains IDEs.

## Features

- Syntax highlighting for:
  - Keywords (`function`, `return`)
  - Built-in functions (`print`, `gettype`)
  - Types (`number`, `string`, `boolean`)
  - Operators (`+`, `-`, `*`, `/`, `->`)
  - String literals
  - Numeric literals
  - Comments
  - Function declarations and calls
  - Boolean literals (`true`, `false`)

## Installation

### From Source
1. Clone this repository
2. Run `./gradlew buildPlugin`
3. Install the generated plugin file from `build/distributions/opnit-1.0-SNAPSHOT.zip`

### Manual Installation
1. Download the latest release
2. In your JetBrains IDE, go to Settings/Preferences → Plugins
3. Click the gear icon and select "Install Plugin from Disk..."
4. Select the downloaded plugin file

## Usage

After installation, files with the `.opnit` extension will automatically be recognized and syntax highlighted.

### Example

```opnit
# Function definition
function add(x: number, y: number) -> number {
    return x + y;
}

# String concatenation
function greet(name: string) -> string {
    return "Hello, " + name;
}

# Function calls
print(add(5, 3));           # Outputs: 8.0
print(greet("World"));      # Outputs: Hello, World
```

## Development

### Requirements
- JDK 11 or later
- Gradle

### Building
```bash
./gradlew buildPlugin
```

### Testing
```bash
./gradlew test
```

## Contributing

Feel free to submit issues and enhancement requests on the GitHub repository. 