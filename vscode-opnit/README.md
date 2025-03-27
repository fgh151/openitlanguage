# Opnit Language Support for Visual Studio Code

This extension provides syntax highlighting support for the Opnit programming language.

## Features

- Syntax highlighting for:
  - Keywords (`function`, `return`)
  - Built-in functions (`print`, `gettype`)
  - Types (`number`, `string`, `boolean`)
  - Operators (`+`, `-`, `*`, `/`, `:`)
  - String literals
  - Numeric literals
  - Comments
  - Function declarations and calls
  - Boolean literals (`true`, `false`)

## Installation

### Local Installation
1. Copy this folder to your VSCode extensions directory:
   - Windows: `%USERPROFILE%\.vscode\extensions`
   - macOS/Linux: `~/.vscode/extensions`
2. Restart VSCode

### From VSIX
1. Package the extension: `vsce package`
2. Install the generated `.vsix` file in VSCode

## Example

```opnit
# Function definition
function add(x: number, y: number): number {
    return x + y;
}

# String concatenation
function greet(name: string): string {
    return "Hello, " + name;
}

# Function calls
print(add(5, 3));           # Outputs: 8.0
print(greet("World"));      # Outputs: Hello, World
```

## Language Features

- Automatic bracket/quote closing
- Comment toggling (using `#`)
- Basic syntax error detection
- Smart indentation

## Contributing

Feel free to submit issues and enhancement requests on the GitHub repository. 