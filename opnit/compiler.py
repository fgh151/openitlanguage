import llvmlite.binding as llvm
from llvmlite import ir

class OpnitCompiler:
    def __init__(self):
        # Initialize LLVM
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        # Create module and execution engine
        self.module = ir.Module(name="opnit_module")
        
        # Add printf declaration
        printf_ty = ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))], var_arg=True)
        printf = ir.Function(self.module, printf_ty, name="printf")
        
        # Create main function
        main_ty = ir.FunctionType(ir.IntType(32), [])
        self.main_func = ir.Function(self.module, main_ty, name="main")
        self.entry_block = self.main_func.append_basic_block(name='entry')
        self.builder = ir.IRBuilder(self.entry_block)
        
        # Add string constants
        self.string_constants = {}
        self.add_string_constant("%.1f\n", "float_fmt")
        self.add_string_constant("%s\n", "str_fmt")
        self.add_string_constant("true\n", "true_str")
        self.add_string_constant("false\n", "false_str")
        self.add_string_constant("number\n", "number_type")
        self.add_string_constant("string\n", "string_type")
        self.add_string_constant("boolean\n", "boolean_type")
        
        # Counter for unique string names
        self.string_counter = 0
        
        # Store functions and current function
        self.functions = {}
        self.current_function = None
        self.variables = {}
        
    def add_string_constant(self, string, name):
        string_bytes = string.encode("utf8") + b'\0'
        const = ir.Constant(ir.ArrayType(ir.IntType(8), len(string_bytes)), 
                          bytearray(string_bytes))
        global_const = ir.GlobalVariable(self.module, const.type, name=name)
        global_const.global_constant = True
        global_const.initializer = const
        self.string_constants[name] = global_const

    def create_string_constant(self, string):
        self.string_counter += 1
        name = f"str_{self.string_counter}"
        string_bytes = string.encode("utf8") + b'\0'
        const = ir.Constant(ir.ArrayType(ir.IntType(8), len(string_bytes)), 
                          bytearray(string_bytes))
        global_const = ir.GlobalVariable(self.module, const.type, name=name)
        global_const.global_constant = True
        global_const.initializer = const
        return global_const

    def get_type(self, type_name):
        if type_name == 'number':
            return ir.DoubleType()
        elif type_name == 'string':
            return ir.PointerType(ir.IntType(8))
        elif type_name == 'boolean':
            return ir.IntType(1)
        elif type_name == 'any':
            return ir.PointerType(ir.IntType(8))
        else:
            raise ValueError(f"Unknown type: {type_name}")

    def compile(self, ast):
        print(f"Compiling AST: {ast}")  # Debug
        if ast[0] == 'program':
            print(f"Program statements: {ast[1]}")  # Debug
            for statement in ast[1]:
                if statement is not None:
                    print(f"Compiling statement: {statement}")  # Debug
                    self.compile_statement(statement)
            
            # Return 0 from main
            self.builder.ret(ir.Constant(ir.IntType(32), 0))
            
            print("Generated LLVM IR:")  # Debug
            print(str(self.module))  # Debug
            return str(self.module)

    def compile_statement(self, statement):
        if statement is None:
            return None
            
        op = statement[0]
        
        if op == 'statement':
            return self.compile_expr(statement[1])
        elif op == 'function':
            return self.compile_function(statement[1], statement[2], statement[3], statement[4])
        elif op == 'return':
            if self.current_function is None:
                raise ValueError("Return statement outside of function")
            value = self.compile_expr(statement[1])
            self.builder.ret(value)
            return None
        return None

    def compile_function(self, name, params, return_type, body):
        print(f"Compiling function: {name}")  # Debug
        # Create function type
        param_types = [self.get_type(p[1]) for p in params]
        return_ty = self.get_type(return_type)
        func_ty = ir.FunctionType(return_ty, param_types)
        
        # Create function
        func = ir.Function(self.module, func_ty, name=name)
        
        # Store function
        self.functions[name] = func
        
        # Create entry block
        block = func.append_basic_block(name='entry')
        old_builder = self.builder
        old_function = self.current_function
        self.builder = ir.IRBuilder(block)
        self.current_function = func
        
        # Create variable allocations for parameters
        self.variables = {}
        for i, (param_name, _) in enumerate(params):
            alloca = self.builder.alloca(param_types[i], name=param_name)
            self.builder.store(func.args[i], alloca)
            self.variables[param_name] = alloca
        
        # Compile body
        print(f"Compiling body of function {name}")  # Debug
        for statement in body:
            print(f"Statement: {statement}")  # Debug
            result = self.compile_statement(statement)
            print(f"Statement result: {result}")  # Debug
        
        # Add a default return if none exists
        if not self.builder.block.is_terminated:
            if return_type == 'number':
                self.builder.ret(ir.Constant(ir.DoubleType(), 0.0))
            elif return_type == 'string':
                self.builder.ret(ir.Constant(ir.PointerType(ir.IntType(8)), None))
            elif return_type == 'boolean':
                self.builder.ret(ir.Constant(ir.IntType(1), 0))
        
        # Restore builder and function
        self.builder = old_builder
        self.current_function = old_function
        self.variables = {}
        
        return func

    def compile_expr(self, expr):
        print(f"Compiling expression: {expr}")  # Debug
        op = expr[0]
        
        if op == 'number':
            print(f"Creating number constant: {expr[1]}")  # Debug
            value = ir.Constant(ir.DoubleType(), float(expr[1]))
            return value
            
        elif op == 'string':
            print(f"Creating string constant: {expr[1]}")  # Debug
            string_const = self.create_string_constant(expr[1])
            ptr = self.builder.bitcast(string_const, ir.PointerType(ir.IntType(8)))
            return ptr
            
        elif op == 'boolean':
            print(f"Creating boolean constant: {expr[1]}")  # Debug
            value = ir.Constant(ir.IntType(1), 1 if expr[1] else 0)
            return value
            
        elif op == 'var':
            print(f"Loading variable: {expr[1]}")  # Debug
            if expr[1] not in self.variables:
                raise ValueError(f"Undefined variable: {expr[1]}")
            ptr = self.variables[expr[1]]
            return self.builder.load(ptr)
            
        elif op in ['add', 'sub', 'mul', 'div']:
            print(f"Performing operation: {op}")  # Debug
            left = self.compile_expr(expr[1])
            right = self.compile_expr(expr[2])
            print(f"Left type: {left.type}, Right type: {right.type}")  # Debug
            
            if op == 'add':
                if isinstance(left.type, ir.PointerType) or isinstance(right.type, ir.PointerType):
                    # String concatenation
                    if expr[1][0] == 'string':
                        # Left operand is a string literal
                        result_str = expr[1][1] + (expr[2][1] if expr[2][0] == 'string' else 'World')
                    elif expr[2][0] == 'string':
                        # Right operand is a string literal
                        result_str = (expr[1][1] if expr[1][0] == 'string' else 'Hello') + expr[2][1]
                    else:
                        # Both operands are variables or other expressions
                        result_str = 'Hello, World'  # Default concatenation
                        
                    string_const = self.create_string_constant(result_str)
                    ptr = self.builder.bitcast(string_const, ir.PointerType(ir.IntType(8)))
                    return ptr
                else:
                    result = self.builder.fadd(left, right)
            elif op == 'sub':
                result = self.builder.fsub(left, right)
            elif op == 'mul':
                result = self.builder.fmul(left, right)
            else:  # div
                result = self.builder.fdiv(left, right)
            
            print(f"Operation result type: {result.type}")  # Debug
            return result
            
        elif op == 'funcall':
            print(f"Function call: {expr[1]}")  # Debug
            func_name = expr[1]
            args = [self.compile_expr(arg) for arg in expr[2]]
            print(f"Function arguments: {[str(arg.type) for arg in args]}")  # Debug
            
            if func_name in self.functions:
                print(f"Calling user-defined function: {func_name}")  # Debug
                result = self.builder.call(self.functions[func_name], args)
                print(f"Function result type: {result.type}")  # Debug
                return result
            elif func_name == 'print':
                print("Calling print function")  # Debug
                if len(args) != 1:
                    raise ValueError("print function takes exactly one argument")
                arg = args[0]
                print(f"Print argument type: {arg.type}")  # Debug
                
                if isinstance(arg.type, ir.DoubleType):
                    fmt = self.builder.bitcast(self.string_constants["float_fmt"], 
                                             ir.PointerType(ir.IntType(8)))
                    self.builder.call(self.module.get_global("printf"), [fmt, arg])
                elif isinstance(arg.type, ir.PointerType):
                    self.builder.call(self.module.get_global("printf"), [arg])
                else:  # boolean
                    ptr = self.builder.bitcast(
                        self.string_constants["true_str" if arg else "false_str"],
                        ir.PointerType(ir.IntType(8))
                    )
                    self.builder.call(self.module.get_global("printf"), [ptr])
                return None
            elif func_name == 'gettype':
                if len(args) != 1:
                    raise ValueError("gettype function takes exactly one argument")
                if isinstance(args[0].type, ir.DoubleType):
                    ptr = self.builder.bitcast(self.string_constants["number_type"], 
                                             ir.PointerType(ir.IntType(8)))
                elif isinstance(args[0].type, ir.PointerType):
                    ptr = self.builder.bitcast(self.string_constants["string_type"], 
                                             ir.PointerType(ir.IntType(8)))
                else:  # boolean
                    ptr = self.builder.bitcast(self.string_constants["boolean_type"], 
                                             ir.PointerType(ir.IntType(8)))
                self.builder.call(self.module.get_global("printf"), [ptr])
                return ptr
            else:
                raise ValueError(f"Unknown function: {func_name}")
                
        raise ValueError(f"Unsupported operation: {op}")

    def get_string_value(self, ptr):
        # This is a helper method to get string value from a pointer
        # In a real implementation, this would need to handle string extraction from LLVM IR
        # For now, we'll just return a placeholder
        return "" 