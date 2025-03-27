"""Built-in len function implementation."""

from llvmlite import ir
from .base import BuiltinFunction

class LenFunction(BuiltinFunction):
    """Built-in len function that returns the length of arrays."""
    
    def register(self, module, builder, string_constants):
        """Register the len function in the module."""
        # Create len function type: takes array pointer, returns double
        len_type = ir.FunctionType(ir.DoubleType(), [ir.PointerType(ir.ArrayType(ir.DoubleType(), 0))])
        self.len_func = ir.Function(module, len_type, name="len")
        return self.len_func
    
    def compile_call(self, builder, args, string_constants):
        """Compile a call to the len function."""
        if len(args) != 1:
            raise ValueError("len function expects exactly one argument")
            
        array = args[0]
        if not isinstance(array.type, ir.PointerType) or not isinstance(array.type.pointee, ir.ArrayType):
            raise ValueError("len function expects an array argument")
            
        # Return array length as double
        length = ir.Constant(ir.DoubleType(), array.type.pointee.count)
        return length 