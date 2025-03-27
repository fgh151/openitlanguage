"""Base class for built-in functions."""

from abc import ABC, abstractmethod
from llvmlite import ir

class BuiltinFunction(ABC):
    """Abstract base class for all built-in functions."""
    
    @abstractmethod
    def register(self, module, builder, string_constants):
        """Register the function in the module and return the function object.
        
        Args:
            module (ir.Module): The LLVM module to register the function in.
            builder (ir.IRBuilder): The current IR builder.
            string_constants (dict): Dictionary of string constants used by the compiler.
            
        Returns:
            ir.Function: The registered function object.
        """
        pass
    
    @abstractmethod
    def compile_call(self, builder, args, string_constants):
        """Compile a call to this function.
        
        Args:
            builder (ir.IRBuilder): The current IR builder.
            args (list): List of compiled argument values.
            string_constants (dict): Dictionary of string constants used by the compiler.
            
        Returns:
            ir.Value: The result of the function call, or None.
        """
        pass 