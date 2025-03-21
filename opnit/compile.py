import sys
import os
import tempfile
import subprocess
import llvmlite.binding as llvm

from .lexer import OpnitLexer
from .parser import OpnitParser
from .compiler import OpnitCompiler

def compile_to_native(input_file, output_file=None):
    # Read input file
    with open(input_file, 'r') as f:
        code = f.read()
    if not code.endswith('\n'):
        code += '\n'

    # Parse the code
    lexer = OpnitLexer()
    parser = OpnitParser()
    compiler = OpnitCompiler()

    # Generate LLVM IR
    tokens = lexer.tokenize(code)
    ast = parser.parse(tokens)
    llvm_ir = compiler.compile(ast)
    
    # Print LLVM IR for debugging
    print("Generated LLVM IR:")
    print(llvm_ir)

    # Initialize LLVM
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()

    # Create a target machine
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()

    # Create a module from the IR
    mod = llvm.parse_assembly(llvm_ir)
    mod.verify()

    # Optimize the module
    pmb = llvm.create_pass_manager_builder()
    pmb.opt_level = 2
    pm = llvm.create_module_pass_manager()
    pmb.populate(pm)
    pm.run(mod)

    # Generate object code
    obj_file = tempfile.NamedTemporaryFile(suffix='.o', delete=False)
    obj_file.close()
    
    with open(obj_file.name, 'wb') as f:
        f.write(target_machine.emit_object(mod))

    # Generate output filename if not provided
    if output_file is None:
        output_file = os.path.splitext(input_file)[0]
        if sys.platform == 'win32':
            output_file += '.exe'

    # Link the object file
    cc = os.environ.get('CC', 'cc')
    subprocess.run([cc, obj_file.name, '-o', output_file])

    # Clean up
    os.unlink(obj_file.name)
    
    return output_file

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m opnit.compile <input_file> [output_file]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        output = compile_to_native(input_file, output_file)
        print(f"Successfully compiled to: {output}")
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 