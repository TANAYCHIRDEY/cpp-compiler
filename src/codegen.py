from parser import (
    NumberLiteral, Identifier, BinaryOp, Assignment,
    VarDeclaration, ReturnStatement, IfStatement,
    WhileStatement, FunctionCall, FunctionDeclaration, Program
)



class CodeGenerator:
    def __init__(self):
        self.output = []
        self.indent_level = 0

    def indent(self):
        return "   " * self.indent_level

    def emit(self,line):
        self.output.append(self.indent()+line)

    def generate(self,node):
        if isinstance(node,Program):
            return self.gen_program(node)
        raise TypeError(f"Unknown node type: {type(node)}")
    
    def gen_program(self,node):
        for func in node.functions:
            self.gen_function(func)
        self.emit("")
        self.emit('if __name__ == "__main__":')
        self.indent_level+=1
        self.emit("main()")
        self.indent_level-=1
        return "\n".join(self.output)

    def gen_function(self,node):
        params = ", ".join(name for _, name in node.params)
        self.emit(f"def {node.name} ({params}):")
        self.indent_level +=1
        if not node.body:
            self.emit("pass")
        for stmt in node.body:
            self.gen_statement(stmt)
        self.indent_level -=1
        self.emit("")
    
    def gen_statement(self,node):
        if isinstance(node,VarDeclaration):
            if node.initializer:
                expr = self.gen_expression(node.initializer)
                self.emit(f"{node.name} = {expr}")

            else :
                self.emit(f"{node.name} = 0")

        elif isinstance(node,Assignment):
            expr = self.gen_expression(node.expr)
            self.emit(f"{node.name} = {expr}")

        elif isinstance(node,ReturnStatement):
            if node.expr:
                expr = self.gen_expression(node.condition)
                self.emit(f"{node.name} = {expr}")
            else :
                self.emit("return")
        elif isinstance(node, IfStatement):
            cond = self.gen_expression(node.condition)
            self.emit(f"if {cond}:")
            self.indent_level += 1
            if not node.then_body:
                self.emit("pass")
            for stmt in node.then_body:
                self.gen_statement(stmt)
            self.indent_level -= 1
            if node.else_body:
                self.emit("else:")
                self.indent_level += 1
                for stmt in node.else_body:
                    self.gen_statement(stmt)
                self.indent_level -= 1
        elif isinstance(node, WhileStatement):
            cond = self.gen_expression(node.condition)
            self.emit(f"while {cond}:")
            self.indent_level += 1
            if not node.body:
                self.emit("pass")
            for stmt in node.body:
                self.gen_statement(stmt)
            self.indent_level -= 1
        elif isinstance(node, FunctionCall):
            args = ", ".join(self.gen_expression(a) for a in node.args)
            # Map C++ print to Python print
            if node.name == "print":
                self.emit(f"print({args})")
            else:
                self.emit(f"{node.name}({args})")
        else:
            raise TypeError(f"Unknown statement: {type(node)}")

            
    def gen_expression(self, node):
        if isinstance(node, NumberLiteral):
            return str(node.value)
        elif isinstance(node, Identifier):
            return node.name
        elif isinstance(node, BinaryOp):
            left = self.gen_expression(node.left)
            right = self.gen_expression(node.right)
            return f"({left} {node.op} {right})"
        elif isinstance(node, FunctionCall):
            args = ", ".join(self.gen_expression(a) for a in node.args)
            if node.name == "print":
                return f"print({args})"
            return f"{node.name}({args})"
        else:
            raise TypeError(f"Unknown expression: {type(node)}")
