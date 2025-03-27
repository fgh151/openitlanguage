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
        elif type_name.endswith('[]'):  # Array type
            element_type = self.get_type(type_name[:-2])
            return ir.LiteralStructType([
                ir.PointerType(element_type),  # Data pointer
                ir.IntType(32)                 # Length
            ])
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
        elif stmt[0] == 'while':
            # Create the basic blocks for the while loop
            cond_block = self.current_function.append_basic_block('while_cond')
            body_block = self.current_function.append_basic_block('while_body')
            end_block = self.current_function.append_basic_block('while_end')
            
            # Jump to the condition block
            self.builder.branch(cond_block)
            
            # Emit the condition code
            self.builder.position_at_end(cond_block)
            cond = self.compile_expr(stmt[1])
            self.builder.cbranch(cond, body_block, end_block)
            
            # Emit the body code
            self.builder.position_at_end(body_block)
            for body_stmt in stmt[2]:
                self.compile_statement(body_stmt)
            self.builder.branch(cond_block)
            
            # Continue building from end block
            self.builder.position_at_end(end_block)
            return None
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
        if expr[0] == 'number':
            return ir.Constant(ir.DoubleType(), float(expr[1]))
        elif expr[0] == 'string':
            return self.create_string_constant(expr[1])
        elif expr[0] == 'variable':
            var_ptr = self.variables[expr[1]]
            if isinstance(var_ptr.type.pointee, ir.ArrayType):
                return var_ptr
            return self.builder.load(var_ptr)
        elif expr[0] == 'assignment':
            var_name = expr[1]
            value = self.compile_expr(expr[2])
            if var_name not in self.variables:
                if expr[2][0] == 'array_literal':
                    # Handle array literal assignment
                    elements = expr[2][1]
                    array_ptr = self.create_array(ir.DoubleType(), len(elements))
                    self.variables[var_name] = array_ptr
                    for i, element in enumerate(elements):
                        element_val = self.compile_expr(element)
                        element_ptr = self.builder.gep(array_ptr, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), i)])
                        self.builder.store(element_val, element_ptr)
                    return array_ptr
                else:
                    ptr = self.builder.alloca(value.type)
                    self.variables[var_name] = ptr
            self.builder.store(value, self.variables[var_name])
            return value
        elif expr[0] == 'array_literal':
            elements = [self.compile_expr(e) for e in expr[1]]
            if not elements:
                return None
            array_type = self.get_array_type(elements[0].type, len(elements))
            array_ptr = self.builder.alloca(array_type)
            for i, element in enumerate(elements):
                element_ptr = self.builder.gep(array_ptr, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), i)])
                self.builder.store(element, element_ptr)
            return array_ptr
        elif expr[0] == 'array_access':
            array = self.compile_expr(expr[1])
            index = self.compile_expr(expr[2])
            if isinstance(index.type, ir.DoubleType):
                index = self.builder.fptosi(index, ir.IntType(32))
            element_ptr = self.builder.gep(array, [ir.Constant(ir.IntType(32), 0), index])
            return self.builder.load(element_ptr)
        elif expr[0] == 'call':
            if expr[1] == 'print':
                return self.compile_print(expr[2])
            else:
                return None
        return None

    def get_string_value(self, ptr):
        # This is a helper method to get string value from a pointer
        # In a real implementation, this would need to handle string extraction from LLVM IR
        # For now, we'll just return a placeholder
        return ""

    def compile_to_binary(self, output_file):
        """Compile the LLVM IR to a binary executable file."""
        # Create a target machine
        target = llvm.Target.from_default_triple()
        target_machine = target.create_target_machine()
        
        # Create a module from the LLVM IR
        mod = llvm.parse_assembly(str(self.module))
        mod.verify()
        
        # Optimize the module
        pmb = llvm.create_pass_manager_builder()
        pmb.opt_level = 2  # Optimization level
        pm = llvm.create_module_pass_manager()
        pmb.populate(pm)
        pm.run(mod)
        
        # Write the object file
        with open(f"{output_file}.o", "wb") as o:
            o.write(target_machine.emit_object(mod))
        
        # Link the object file to create an executable
        import subprocess
        import sys
        
        if sys.platform == 'darwin':  # macOS
            subprocess.run(['clang', f'{output_file}.o', '-o', output_file])
        else:  # Linux and others
            subprocess.run(['cc', f'{output_file}.o', '-o', output_file])
        
        # Make the binary executable
        import os
        os.chmod(output_file, 0o755)
        
        # Clean up the object file
        os.remove(f"{output_file}.o")

    def create_array(self, elements, element_type):
        """Create an array from a list of elements."""
        # Create array struct type
        array_type = ir.LiteralStructType([
            ir.PointerType(element_type),  # Data pointer
            ir.IntType(32)                 # Length
        ])
        
        # Allocate array struct
        array_struct = self.builder.alloca(array_type)
        
        # Allocate array data
        length = len(elements)
        array_data = self.builder.alloca(element_type, size=ir.Constant(ir.IntType(32), length))
        
        # Store elements
        for i, element in enumerate(elements):
            ptr = self.builder.gep(array_data, [ir.Constant(ir.IntType(32), i)])
            self.builder.store(element, ptr)
        
        # Store array data pointer and length
        data_ptr = self.builder.gep(array_struct, [
            ir.Constant(ir.IntType(32), 0),
            ir.Constant(ir.IntType(32), 0)
        ])
        self.builder.store(array_data, data_ptr)
        
        length_ptr = self.builder.gep(array_struct, [
            ir.Constant(ir.IntType(32), 0),
            ir.Constant(ir.IntType(32), 1)
        ])
        self.builder.store(ir.Constant(ir.IntType(32), length), length_ptr)
        
        return array_struct

    def get_array_element(self, array_ptr, index):
        """Get an element from an array at the given index."""
        # Load array data pointer
        data_ptr = self.builder.gep(array_ptr, [
            ir.Constant(ir.IntType(32), 0),
            ir.Constant(ir.IntType(32), 0)
        ])
        data = self.builder.load(data_ptr)
        
        # Load array length
        length_ptr = self.builder.gep(array_ptr, [
            ir.Constant(ir.IntType(32), 0),
            ir.Constant(ir.IntType(32), 1)
        ])
        length = self.builder.load(length_ptr)
        
        # Check bounds
        is_in_bounds = self.builder.icmp_unsigned('<', index, length)
        with self.builder.if_else(is_in_bounds) as (then, otherwise):
            with then:
                # Get element pointer and load value
                element_ptr = self.builder.gep(data, [index])
                result = self.builder.load(element_ptr)
                self.builder.ret(result)
            with otherwise:
                # Handle out of bounds error
                error_msg = self.create_string_constant("Array index out of bounds")
                self.builder.call(self.printf, [error_msg])
                self.builder.ret(ir.Constant(data.type.pointee, None))

    def get_array_type(self, element_type, size):
        return ir.ArrayType(element_type, size)

    def create_array(self, element_type, length):
        array_type = self.get_array_type(element_type, length)
        array_ptr = self.builder.alloca(array_type)
        return array_ptr

    def compile_print(self, args):
        if not isinstance(args, list):
            args = [args]
        for arg in args:
            value = self.compile_expr(arg)
            if isinstance(value.type, ir.DoubleType):
                fmt = self.module.get_global("float_fmt")
                fmt_ptr = self.builder.gep(fmt, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])
                self.builder.call(self.printf, [fmt_ptr, value])
        return None 