"""Built-in print function implementation."""

from llvmlite import ir
from .base import BuiltinFunction

class PrintFunction(BuiltinFunction):
    """Built-in print function that can print numbers, strings, and booleans."""
    
    def register(self, module, builder, string_constants):
        """Register the printf function in the module."""
        # Create printf function declaration
        printf_type = ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))], var_arg=True)
        self.printf = ir.Function(module, printf_type, name="printf")
        return self.printf
    
    def compile_call(self, builder, args, string_constants):
        """Compile a call to the print function."""
        for value in args:
            # Get the appropriate format string based on the value type
            if isinstance(value.type, ir.DoubleType):
                fmt = string_constants["float_fmt"]
            elif isinstance(value.type, ir.IntType) and value.type.width == 1:
                fmt = string_constants["true_str" if value else "false_str"]
            else:
                fmt = string_constants["str_fmt"]
            
            # Get pointer to format string
            zero = ir.Constant(ir.IntType(32), 0)
            fmt_ptr = builder.gep(fmt, [zero, zero], inbounds=True)
            
            # Call printf
            if isinstance(value.type, ir.DoubleType):
                builder.call(self.printf, [fmt_ptr, value])
            elif isinstance(value.type, ir.IntType) and value.type.width == 1:
                builder.call(self.printf, [fmt_ptr])
            else:
                builder.call(self.printf, [fmt_ptr, value])
        
        return None 