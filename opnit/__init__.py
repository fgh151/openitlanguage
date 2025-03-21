from .lexer import OpnitLexer
from .parser import OpnitParser
from .compiler import OpnitCompiler

def run(code):
    lexer = OpnitLexer()
    parser = OpnitParser()
    compiler = OpnitCompiler()
    
    tokens = lexer.tokenize(code)
    tree = parser.parse(tokens)
    llvm_ir = compiler.compile(tree)
    
    # Initialize LLVM execution engine
    from llvmlite import binding as llvm
    
    # Create execution engine
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    
    # Create module from IR
    mod = llvm.parse_assembly(llvm_ir)
    mod.verify()
    
    # Add module to execution engine and finalize
    engine = llvm.create_mcjit_compiler(mod, target_machine)
    engine.finalize_object()
    
    # Run the main function
    main_addr = engine.get_function_address("main")
    from ctypes import CFUNCTYPE, c_int
    cfunc = CFUNCTYPE(c_int)(main_addr)
    cfunc() 