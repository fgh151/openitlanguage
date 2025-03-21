import sys
from . import run

def main():
    if len(sys.argv) != 2:
        print("Usage: python -m opnit <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename, 'r') as f:
            code = f.read()
        if not code.endswith('\n'):
            code += '\n'  # Ensure the code ends with a newline
        run(code)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 