# Opnit Programming Language

Opnit is a simple yet powerful programming language that supports basic arithmetic operations, string manipulation, and function definitions.

## Features

### Basic Types
- `number`: Floating-point numbers (e.g., `42`, `3.14`)
- `string`: Text strings (e.g., `"Hello, World"`)
- `boolean`: True/false values (e.g., `true`, `false`)

### Functions

#### Function Definition
Functions are defined using the `function` keyword, followed by:
- Function name
- Parameter list with types
- Return type (after `:`)
- Function body in curly braces

Example:
```opnit
function add(x: number, y: number) : number {
    return x + y;
}
```

#### Function Parameters
- Parameters are defined with a name and type: `paramName: type`
- Multiple parameters are separated by commas
- Parameters can be of any valid type (number, string, boolean)

Example:
```opnit
function greet(name: string) : string {
    return "Hello, " + name;
}
```

#### Return Values
- Functions must specify a return type using `:` after the parameter list
- The `return` statement is used to return values
- Return type must match the declared type

Example:
```opnit
function get_pi(): number {
    return 3.14159;
}
```

#### Function Calls
- Functions are called by name with arguments in parentheses
- Arguments can be literals, variables, or expressions
- Number of arguments must match the function definition

Example:
```opnit
print(add(5, 3));           # Outputs: 8.0
print(greet("World"));      # Outputs: Hello, World
print(get_pi());            # Outputs: 3.14159
```

#### Nested Function Calls
Functions can be nested and used in expressions:

```opnit
function multiply_and_add(a: number, b: number, c: number) : number {
    return add(a * b, c);
}

print(multiply_and_add(2, 3, 4));  # Outputs: 10.0 (2 * 3 + 4)
```

### Built-in Functions

#### print
Prints a value to the console:
```opnit
print(42);          # Prints a number
print("Hello");     # Prints a string
print(true);        # Prints a boolean
```

#### gettype
Returns the type of a value:
```opnit
gettype(42);        # Outputs: number
gettype("Hello");   # Outputs: string
gettype(true);      # Outputs: boolean
```

### Operators

#### Arithmetic Operators
- Addition: `+` (also used for string concatenation)
- Subtraction: `-`
- Multiplication: `*`
- Division: `/`

#### String Operations
- Concatenation: `+`
```opnit
print("Hello, " + "World");  # Outputs: Hello, World
```

## Usage

1. Create a file with `.opnit` extension
2. Write your Opnit code
3. Run using: `python3 -m opnit your_file.opnit`

## Example Program

```opnit
# Function to calculate area of a rectangle
function area(width: number, height: number) : number {
    return width * height;
}

# Function to create a greeting
function personalized_greeting(name: string) : string {
    return "Welcome, " + name + "!";
}

# Using the functions
print(area(5, 3));                    # Outputs: 15.0
print(personalized_greeting("Alice")); # Outputs: Welcome, Alice!
```

## Notes
- All statements must end with a semicolon (;)
- Function bodies must be enclosed in curly braces {}
- Comments start with #
- String literals use double quotes
- Numbers are always floating-point

## Installation
```bash
pip install -r requirements.txt
``` 