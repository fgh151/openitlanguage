# Opnit Programming Language

Opnit is a simple yet powerful programming language that supports basic arithmetic operations, string manipulation, and function definitions.

## Features

### Basic Types
- `number`: Floating-point numbers (e.g., `42`, `3.14`)
- `string`: Text strings (e.g., `"Hello, World"`)
- `boolean`: True/false values (e.g., `true`, `false`)
- `array`: Ordered collections of values (e.g., `[1, 2, 3]`, `["hello", "world"]`)

### Constants

Constants are immutable values that are evaluated at compile time. They are defined using the `const` keyword followed by a name, type, and value. Constants can be of any basic type and can include expressions that can be evaluated at compile time.

#### Constant Declaration
```opnit
const PI: number = 3.14159;
const GREETING: string = "Hello, World!";
const IS_DEBUG: boolean = true;
```

#### Constant Expressions
Constants can be defined using expressions involving other constants or literal values:

```opnit
const PI: number = 3.14159;
const RADIUS: number = 25.0;
const CIRCLE_AREA: number = PI * RADIUS * RADIUS;  # Evaluated at compile time

const FIRST: string = "Hello";
const SECOND: string = "World";
const COMBINED: string = FIRST + " " + SECOND;     # String concatenation at compile time
```

#### Type Inference with 'any'
Constants can use the `any` type for flexible type handling:

```opnit
const ANY_NUMBER: any = 42.0;
const ANY_STRING: any = "This is a string";
const ANY_BOOL: any = false;
```

#### Using Constants
Constants can be used anywhere a literal value is expected:

```opnit
function calculate_area(radius: number) : number {
    return PI * radius * radius;  # Using PI constant
}

print(GREETING);  # Using string constant
if (IS_DEBUG) {   # Using boolean constant
    print("Debug mode is on");
}
```

### Arrays

#### Array Declaration and Initialization
Arrays can be declared and initialized using square brackets:
```opnit
var numbers = [1, 2, 3];           # Array of numbers
var words = ["hello", "world"];     # Array of strings
var empty = [];                     # Empty array
```

#### Array Access
Elements in an array can be accessed using zero-based indexing:
```opnit
var numbers = [1, 2, 3];
print(numbers[0]);     # Outputs: 1.0 (first element)
print(numbers[2]);     # Outputs: 3.0 (last element)
```

#### Array Length
Use the `len()` function to get the number of elements in an array:
```opnit
var numbers = [1, 2, 3, 4, 5];
var size = len(numbers);    # Returns: 5
```

#### Array Parameters in Functions
Functions can accept arrays as parameters:
```opnit
function sum_array(numbers: number[]) : number {
    // Array processing code here
    return 0;
}
```

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

## Installation

1. Make sure you have Python 3.6+ installed
2. Install the required dependencies:
```bash
pip install llvmlite
```
3. Make sure you have a C compiler installed:
   - On macOS: Install Xcode Command Line Tools (`xcode-select --install`)
   - On Linux: Install GCC (`sudo apt-get install gcc` on Ubuntu/Debian)

## Usage

### Running Programs

There are three ways to run Opnit programs:

1. **Direct Execution** - Run the program directly without generating a binary:
```bash
python -m opnit your_program.opnit
```

2. **Compile to Binary** - Create a native executable:
```bash
python -m opnit your_program.opnit -o output_binary
./output_binary  # Run the compiled program
```

3. **View LLVM IR** - See the generated LLVM intermediate representation:
```bash
python -m opnit your_program.opnit --emit-llvm
```

If you don't specify an output name with `-o`, the compiler will use the input filename without the `.opnit` extension.

## Example Programs

### Basic Functions Example
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

### Array Operations Example
```opnit
# Function to calculate the sum of array elements
function array_sum(numbers: number[]) : number {
    var sum = 0;
    var i = 0;
    while (i < len(numbers)) {
        sum = sum + numbers[i];
        i = i + 1;
    }
    return sum;
}

# Using arrays
var numbers = [1, 2, 3, 4, 5];
print(numbers[0]);           # Outputs: 1.0 (first element)
print(array_sum(numbers));   # Outputs: 15.0 (sum of all elements)

var words = ["hello", "world"];
print(words[1]);            # Outputs: world
print(len(words));          # Outputs: 2
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