from dataclasses import dataclass,field
from typing import List,Optional

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
class FunctionnCall : 
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
    