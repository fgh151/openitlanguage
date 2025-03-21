class OpnitInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {
            'print': self.print_func,
            'gettype': self.gettype_func
        }

    def print_func(self, value):
        print(value)
        return None

    def gettype_func(self, value):
        if isinstance(value, bool):
            return 'boolean'
        elif isinstance(value, str):
            return 'string'
        elif isinstance(value, (int, float)):
            return 'number'
        return 'any'

    def evaluate(self, tree):
        if tree is None:
            return None

        operation = tree[0]

        if operation == 'program':
            last_result = None
            for statement in tree[1]:
                if statement is not None:  # Skip None statements (empty lines)
                    last_result = self.evaluate(statement)
            return last_result

        elif operation == 'statement':
            return self.evaluate(tree[1])

        elif operation == 'number':
            return tree[1]
        elif operation == 'string':
            return tree[1]
        elif operation == 'boolean':
            return tree[1]
        elif operation == 'add':
            return self.evaluate(tree[1]) + self.evaluate(tree[2])
        elif operation == 'sub':
            return self.evaluate(tree[1]) - self.evaluate(tree[2])
        elif operation == 'mul':
            return self.evaluate(tree[1]) * self.evaluate(tree[2])
        elif operation == 'div':
            return self.evaluate(tree[1]) / self.evaluate(tree[2])
        elif operation == 'funcall':
            func_name = tree[1]
            arg = self.evaluate(tree[2])
            if func_name in self.functions:
                return self.functions[func_name](arg)
            raise NameError(f"Function '{func_name}' is not defined")
        elif operation == 'funcall2':
            func_name = tree[1]
            arg1 = self.evaluate(tree[2])
            arg2 = self.evaluate(tree[3])
            if func_name in self.functions:
                return self.functions[func_name](arg1, arg2)
            raise NameError(f"Function '{func_name}' is not defined") 