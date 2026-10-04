from enum import Enum, auto 
from dataclasses import dataclass

class TokenType(Enum):
    NUMBER= auto()
    IDENTIFIER = auto()
    KEYWORD = auto()

    PLUS = auto()
    MINUS = auto()
    STAR =auto()
    SLASH =auto()
    ASSIGN = auto()
    EQ = auto()
    NEQ = auto()
    LT = auto()
    LE = auto()
    GT = auto()

    #Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()
    COMMA = auto()

    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value : str
    line : int 

    def _repr_(self):
        return f"Token({self.type.name}, '{self.value}',line={self.line})"

KEYWORDS = ["int" , "if" , "else" , "while" , "return","void"]
