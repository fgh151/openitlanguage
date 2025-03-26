import sys
import argparse
from . import run

def main():
    parser = argparse.ArgumentParser(description='Opnit Language Compiler')
    parser.add_argument('filename', help='Source file to compile')
    parser.add_argument('-o', '--output', help='Output binary file name')
    parser.add_argument('--emit-llvm', action='store_true', help='Emit LLVM IR instead of binary')
    args = parser.parse_args()

    try:
        with open(args.filename, 'r') as f:
            code = f.read()
        if not code.endswith('\n'):
            code += '\n'  # Ensure the code ends with a newline
        
        # Run the compiler
        if args.emit_llvm:
            # Just emit LLVM IR
            run(code)
        else:
            # Compile to binary
            output_file = args.output or args.filename.rsplit('.', 1)[0]
            run(code, output_file=output_file)
            print(f"Binary compiled to: {output_file}")
    except FileNotFoundError:
        print(f"Error: File '{args.filename}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 