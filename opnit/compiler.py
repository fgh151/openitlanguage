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

    def compile(self, ast):
        if ast[0] == 'program':
            for statement in ast[1]:
                if statement is not None:
                    self.compile_statement(statement)
            
            # Return 0 from main
            self.builder.ret(ir.Constant(ir.IntType(32), 0))
            
            return str(self.module)

    def compile_statement(self, statement):
        if statement[0] == 'statement':
            return self.compile_expr(statement[1])
        return None

    def compile_expr(self, expr):
        op = expr[0]
        
        if op == 'number':
            value = ir.Constant(ir.DoubleType(), float(expr[1]))
            # Print the number
            fmt = self.builder.bitcast(self.string_constants["float_fmt"], 
                                     ir.PointerType(ir.IntType(8)))
            self.builder.call(self.module.get_global("printf"), [fmt, value])
            return value
            
        elif op == 'string':
            # Create string constant with null terminator
            string_const = self.create_string_constant(expr[1] + "\n")
            
            # Print the string
            ptr = self.builder.bitcast(string_const, ir.PointerType(ir.IntType(8)))
            self.builder.call(self.module.get_global("printf"), [ptr])
            return ptr
            
        elif op == 'boolean':
            # Print true/false
            ptr = self.builder.bitcast(
                self.string_constants["true_str" if expr[1] else "false_str"],
                ir.PointerType(ir.IntType(8))
            )
            self.builder.call(self.module.get_global("printf"), [ptr])
            return ptr
            
        elif op in ['add', 'sub', 'mul', 'div']:
            left = self.compile_expr(expr[1])
            right = self.compile_expr(expr[2])
            
            if op == 'add':
                if isinstance(left.type, ir.PointerType) or isinstance(right.type, ir.PointerType):
                    # String concatenation
                    # Create a new string constant for concatenated result
                    left_str = expr[1][1] if expr[1][0] == 'string' else str(expr[1][1])
                    right_str = expr[2][1] if expr[2][0] == 'string' else str(expr[2][1])
                    result_str = left_str + right_str
                    
                    # Create string constant
                    string_const = self.create_string_constant(result_str + "\n")
                    
                    # Print the string
                    ptr = self.builder.bitcast(string_const, ir.PointerType(ir.IntType(8)))
                    self.builder.call(self.module.get_global("printf"), [ptr])
                    return ptr
                else:
                    result = self.builder.fadd(left, right)
            elif op == 'sub':
                result = self.builder.fsub(left, right)
            elif op == 'mul':
                result = self.builder.fmul(left, right)
            else:  # div
                result = self.builder.fdiv(left, right)
                
            # Print the result
            fmt = self.builder.bitcast(self.string_constants["float_fmt"], 
                                     ir.PointerType(ir.IntType(8)))
            self.builder.call(self.module.get_global("printf"), [fmt, result])
            return result
            
        elif op == 'funcall':
            func_name = expr[1]
            arg = self.compile_expr(expr[2])
            
            if func_name == 'print':
                if isinstance(arg.type, ir.DoubleType):
                    fmt = self.builder.bitcast(self.string_constants["float_fmt"], 
                                             ir.PointerType(ir.IntType(8)))
                    self.builder.call(self.module.get_global("printf"), [fmt, arg])
                else:
                    self.builder.call(self.module.get_global("printf"), [arg])
                return None
                
            elif func_name == 'gettype':
                # Print type based on argument type
                if isinstance(arg.type, ir.DoubleType):
                    ptr = self.builder.bitcast(self.string_constants["number_type"], 
                                             ir.PointerType(ir.IntType(8)))
                elif isinstance(arg.type, ir.PointerType):
                    ptr = self.builder.bitcast(self.string_constants["string_type"], 
                                             ir.PointerType(ir.IntType(8)))
                else:  # boolean
                    ptr = self.builder.bitcast(self.string_constants["boolean_type"], 
                                             ir.PointerType(ir.IntType(8)))
                self.builder.call(self.module.get_global("printf"), [ptr])
                return ptr
                
        raise ValueError(f"Unsupported operation: {op}")

    def get_string_value(self, ptr):
        # This is a helper method to get string value from a pointer
        # In a real implementation, this would need to handle string extraction from LLVM IR
        # For now, we'll just return a placeholder
        return "" 