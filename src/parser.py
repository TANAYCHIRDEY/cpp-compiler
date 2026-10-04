from dataclasses import dataclass,field
from typing import List,Optional
from lexer import TokenType
# ------ AST Node Definitions -----

@dataclass
class NumberLiteral:
    value : int

@dataclass
class Identifier:
    name : str

@dataclass
class BinaryOp:
    left : object 
    op : str
    right : object 

@dataclass 
class Assignment :
    name : str 
    expr : object 

@dataclass 
class VarDeclaration :
    var_type : str 
    name : str
    initializer : object = None

@dataclass
class FunctionCall : 
    name : str
    args : list 

@dataclass
class FunctionDeclaration :
    return_type : str 
    name : str 
    params : list
    body : list 

@dataclass
class Program : 
    functions : list 

@dataclass 
class ReturnStatement :
    expr : object 

@dataclass
class IfStatement:
    condition : object
    then_body : list 
    else_body : list =field(default_factory=list)

@dataclass
class WhileStatement:
    condition : object 
    body : list 



class Parser:
    def __init__(self,tokens):
        self.tokens = tokens 
        self.pos = 0
    
    def current(self):
        return self.tokens[self.pos]
    
    def eat(self,token_type,value=None):
        token = self.current()
        if token.type != token_type:
            raise SyntaxError("Expected {token_type}, got {token.type} ('{token.value}') at {token.line}")
        if value and token.value != value :
            raise SyntaxError(f"Expected '{value}', got {token.value} at line {token.line}")
        self.pos +=1
        return token

    def parse_function(self):
        return_type = self.eat(TokenType.KEYWORD).value
        name = self.eat(TokenType.IDENTIFIER).value
        self.eat(TokenType.LPAREN)
        params = self.parse_params()
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.LBRACE)
        body=self.eat(TokenType.RBRACE)
        return FunctionDeclaration(return_type,name,params,body)
    
    def parse_params(self):
        params=[]
        if self.current().type == TokenType.RPAREN:
            return params
        param_type = self.eat(TokenType.KEYWORD).value
        param_name = self.eat(TokenType.IDENTIFIER).value
        params.append((param_type,param_name))
        while self.current().type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            param_type = self.eat(TokenType.KEYWORD).value
            param_name = self.eat(TokenType.IDENTIFIER).value
            params.append((param_type,param_name))
        return params
    
    def parse_block(self):
        statements = []

        while self.current().type !=TokenType.RBRACE:
            statements.append(self.parse_statement())
        return statements

    