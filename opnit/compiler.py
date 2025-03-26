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
        target = llvm.Target.from_default_triple()
        target_machine = target.create_target_machine()
        backing_mod = llvm.parse_assembly("")
        self.engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
        
        # Initialize variables
        self.string_constants = {}
        self.functions = {}
        self.current_function = None
        self.variables = {}
        self.string_counter = 0
        
        # Add target triple and data layout
        self.module.triple = "unknown-unknown-unknown"
        self.module.data_layout = ""
        
        # Create printf function declaration
        printf_type = ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))], var_arg=True)
        self.printf = ir.Function(self.module, printf_type, name="printf")
        
        # Create format strings
        float_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), 6), bytearray("%.1f\n\0".encode()))
        str_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), 4), bytearray("%s\n\0".encode()))
        true_str = ir.Constant(ir.ArrayType(ir.IntType(8), 6), bytearray("true\n\0".encode()))
        false_str = ir.Constant(ir.ArrayType(ir.IntType(8), 7), bytearray("false\n\0".encode()))
        
        # Create global variables for format strings
        float_fmt_var = ir.GlobalVariable(self.module, float_fmt.type, name="float_fmt")
        float_fmt_var.global_constant = True
        float_fmt_var.initializer = float_fmt
        self.string_constants["float_fmt"] = float_fmt_var
        
        str_fmt_var = ir.GlobalVariable(self.module, str_fmt.type, name="str_fmt")
        str_fmt_var.global_constant = True
        str_fmt_var.initializer = str_fmt
        self.string_constants["str_fmt"] = str_fmt_var
        
        true_str_var = ir.GlobalVariable(self.module, true_str.type, name="true_str")
        true_str_var.global_constant = True
        true_str_var.initializer = true_str
        self.string_constants["true_str"] = true_str_var
        
        false_str_var = ir.GlobalVariable(self.module, false_str.type, name="false_str")
        false_str_var.global_constant = True
        false_str_var.initializer = false_str
        self.string_constants["false_str"] = false_str_var
        
        # Create type strings
        number_type = ir.Constant(ir.ArrayType(ir.IntType(8), 8), bytearray("number\n\0".encode()))
        string_type = ir.Constant(ir.ArrayType(ir.IntType(8), 8), bytearray("string\n\0".encode()))
        boolean_type = ir.Constant(ir.ArrayType(ir.IntType(8), 9), bytearray("boolean\n\0".encode()))
        
        # Create global variables for type strings
        number_type_var = ir.GlobalVariable(self.module, number_type.type, name="number_type")
        number_type_var.global_constant = True
        number_type_var.initializer = number_type
        self.string_constants["number_type"] = number_type_var
        
        string_type_var = ir.GlobalVariable(self.module, string_type.type, name="string_type")
        string_type_var.global_constant = True
        string_type_var.initializer = string_type
        self.string_constants["string_type"] = string_type_var
        
        boolean_type_var = ir.GlobalVariable(self.module, boolean_type.type, name="boolean_type")
        boolean_type_var.global_constant = True
        boolean_type_var.initializer = boolean_type
        self.string_constants["boolean_type"] = boolean_type_var
        
        # Create input buffer
        input_buffer = ir.Constant(ir.ArrayType(ir.IntType(8), 1025), [0] * 1025)
        input_buffer_var = ir.GlobalVariable(self.module, input_buffer.type, name="input_buffer")
        input_buffer_var.global_constant = True
        input_buffer_var.initializer = input_buffer
        self.string_constants["input_buffer"] = input_buffer_var
        
        # Create dummy function to avoid empty module
        dummy_type = ir.FunctionType(ir.IntType(32), [])
        dummy_func = ir.Function(self.module, dummy_type, name="dummy")
        block = dummy_func.append_basic_block(name="entry")
        builder = ir.IRBuilder(block)
        builder.ret(ir.Constant(ir.IntType(32), 0))
        
        # Initialize builder with a dummy block that will be replaced
        self.builder = ir.IRBuilder(dummy_func.append_basic_block(name="entry"))
        self.builder.ret(ir.Constant(ir.IntType(32), 0))  # Add proper return

    def add_string_constant(self, string, name):
        string_bytes = string.encode("utf8") + b'\0'
        const = ir.Constant(ir.ArrayType(ir.IntType(8), len(string_bytes)), 
                          bytearray(string_bytes))
        global_const = ir.GlobalVariable(self.module, const.type, name=name)
        global_const.global_constant = True
        global_const.initializer = const
        self.string_constants[name] = global_const

    def create_string_constant(self, string):
        # Convert string to bytes and add null terminator
        string_bytes = string.encode('utf-8') + b'\0'
        
        # Create constant array with the string data
        string_type = ir.ArrayType(ir.IntType(8), len(string_bytes))
        string_const = ir.GlobalVariable(self.module, string_type, name=f"str_{len(self.string_constants)}")
        string_const.global_constant = True
        string_const.initializer = ir.Constant(string_type, list(string_bytes))
        
        # Get a pointer to the first element of the array
        zero = ir.Constant(ir.IntType(32), 0)
        return self.builder.gep(string_const, [zero, zero], inbounds=True)

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
            
            # Get the main function
            main_func = self.functions.get('main')
            if main_func is None:
                raise ValueError("No main function found")
            
            # Verify the module
            llvm.parse_assembly(str(self.module))
            
            print("Generated LLVM IR:")  # Debug
            print(str(self.module))  # Debug
            return str(self.module)

    def compile_statement(self, stmt):
        if stmt is None:
            return None
        
        if stmt[0] == 'statement':
            return self.compile_expr(stmt[1])
        elif stmt[0] == 'return':
            if len(stmt) > 1:
                retval = self.compile_expr(stmt[1])
                return self.builder.ret(retval)
            else:
                return self.builder.ret_void()
        elif stmt[0] == 'function':
            return self.compile_function(stmt)
        else:
            raise ValueError(f"Unknown statement type: {stmt[0]}")

    def compile_function(self, node):
        print(f"Compiling function: {node}")
        func_name = node[1]
        params = node[2]
        return_type_name = node[3]
        body = node[4]

        # Determine return type
        if func_name == 'main':
            return_type = ir.IntType(32)  # main always returns int
        elif return_type_name == 'number':
            return_type = ir.DoubleType()
        elif return_type_name == 'string':
            return_type = ir.PointerType(ir.IntType(8))
        elif return_type_name == 'boolean':
            return_type = ir.IntType(1)
        else:
            raise TypeError(f"Unknown return type: {return_type_name}")

        # Create function type
        param_types = []
        for param_name, param_type in params:
            if param_type == 'number':
                param_types.append(ir.DoubleType())
            elif param_type == 'string':
                param_types.append(ir.PointerType(ir.IntType(8)))
            elif param_type == 'boolean':
                param_types.append(ir.IntType(1))
            else:
                raise TypeError(f"Unknown parameter type: {param_type}")
        
        func_type = ir.FunctionType(return_type, param_types)
        
        # Create function
        if func_name in self.module.globals:
            func = self.module.get_global(func_name)
            if not isinstance(func, ir.Function):
                raise TypeError(f"{func_name} already defined as non-function")
            if not func.is_declaration:
                raise TypeError(f"{func_name} already defined")
        else:
            func = ir.Function(self.module, func_type, func_name)
            self.functions[func_name] = func  # Store the function

        # Create entry block
        block = func.append_basic_block('entry')
        
        # Store previous state
        old_builder = self.builder
        old_vars = self.variables
        old_function = self.current_function
        
        # Create new builder and variable context
        self.builder = ir.IRBuilder(block)
        self.variables = {}
        self.current_function = func
        
        # Allocate parameters
        for i, ((param_name, _), arg) in enumerate(zip(params, func.args)):
            var = self.builder.alloca(arg.type, name=param_name)
            self.builder.store(arg, var)
            self.variables[param_name] = var

        # Compile body
        for stmt in body:
            if stmt is not None:  # Skip None statements
                if stmt[0] == 'return':
                    if len(stmt) > 1:
                        retval = self.compile_expr(stmt[1])
                        if func_name == 'main':
                            # Convert float to int for main's return
                            if isinstance(retval.type, ir.DoubleType):
                                retval = self.builder.fptosi(retval, ir.IntType(32))
                        self.builder.ret(retval)
                    else:
                        self.builder.ret_void()
                else:
                    self.compile_statement(stmt)

        # Add return if function is not terminated
        if not self.builder.block.is_terminated:
            if isinstance(return_type, ir.VoidType):
                self.builder.ret_void()
            elif isinstance(return_type, ir.IntType) and return_type.width == 32:
                self.builder.ret(ir.Constant(ir.IntType(32), 0))
            elif isinstance(return_type, ir.DoubleType):
                self.builder.ret(ir.Constant(ir.DoubleType(), 0.0))
            elif isinstance(return_type, ir.IntType) and return_type.width == 1:
                self.builder.ret(ir.Constant(ir.IntType(1), 0))
            else:
                self.builder.ret(ir.Constant(return_type, None))

        # Restore previous state
        self.builder = old_builder
        self.variables = old_vars
        self.current_function = old_function

        return func

    def compile_expr(self, expr):
        if expr[0] == 'variable':
            var_name = expr[1]
            if var_name not in self.variables:
                raise NameError(f"Variable {var_name} not found")
            var_ptr = self.variables[var_name]
            return self.builder.load(var_ptr)
        elif expr[0] == 'number':
            return ir.Constant(ir.DoubleType(), float(expr[1]))
        elif expr[0] == 'string':
            return self.create_string_constant(expr[1])
        elif expr[0] == 'boolean':
            return ir.Constant(ir.IntType(1), 1 if expr[1] else 0)
        elif expr[0] == 'binary':
            op = expr[1]
            left = self.compile_expr(expr[2])
            right = self.compile_expr(expr[3])
            
            if op == '+':
                if isinstance(left.type, ir.DoubleType) and isinstance(right.type, ir.DoubleType):
                    return self.builder.fadd(left, right)
                elif isinstance(left.type, ir.IntType) and isinstance(right.type, ir.IntType):
                    return self.builder.add(left, right)
                else:
                    raise TypeError(f"Unsupported operand types for +: {left.type} and {right.type}")
            elif op == '-':
                return self.builder.fsub(left, right)
            elif op == '*':
                return self.builder.fmul(left, right)
            elif op == '/':
                return self.builder.fdiv(left, right)
            else:
                raise ValueError(f"Unknown binary operator: {op}")
        elif expr[0] == 'call':
            func_name = expr[1]
            args = [self.compile_expr(arg) for arg in expr[2]]
            
            if func_name == 'print':
                # Handle print function
                for arg in args:
                    if isinstance(arg.type, ir.DoubleType):
                        fmt = self.module.get_global('float_fmt')
                        fmt_ptr = self.builder.gep(fmt, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])
                        self.builder.call(self.printf, [fmt_ptr, arg])
                    elif isinstance(arg.type, ir.IntType) and arg.type.width == 1:
                        # Boolean case
                        true_str = self.module.get_global('true_str')
                        false_str = self.module.get_global('false_str')
                        fmt = self.module.get_global('str_fmt')
                        fmt_ptr = self.builder.gep(fmt, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])
                        cond = self.builder.icmp_unsigned('!=', arg, ir.Constant(ir.IntType(1), 0))
                        str_ptr = self.builder.select(cond, 
                            self.builder.gep(true_str, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)]),
                            self.builder.gep(false_str, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)]))
                        self.builder.call(self.printf, [fmt_ptr, str_ptr])
                    elif isinstance(arg.type, ir.PointerType):
                        # String case
                        fmt = self.module.get_global('str_fmt')
                        fmt_ptr = self.builder.gep(fmt, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])
                        self.builder.call(self.printf, [fmt_ptr, arg])
                    else:
                        raise TypeError(f"Unsupported type for print: {arg.type}")
                return None
            else:
                # Handle other function calls
                func = self.module.get_global(func_name)
                if not func:
                    raise NameError(f"Function {func_name} not found")
                return self.builder.call(func, args)
        else:
            raise ValueError(f"Unknown expression type: {expr[0]}")

    def get_string_value(self, ptr):
        # This is a helper method to get string value from a pointer
        # In a real implementation, this would need to handle string extraction from LLVM IR
        # For now, we'll just return a placeholder
        return "" 