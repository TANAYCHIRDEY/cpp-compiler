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

    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}',line={self.line})"

KEYWORDS = ["int" , "if" , "else" , "while" , "return","void"]


class Lexer:
    def __init__(self,source):
        self.source = source
        self.pos = 0
        self.line = 1
        self.tokens = []

    def current_char(self):
        if self.pos < len(self.source):
            return self.source[self.pos]
        return None
    
    def advance(self):
        if self.current_char() == '\n':
            self.line += 1 
        self.pos +=1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char() in  ' \t\n\r':
            self.advance()
    
    def skip_comment(self):
        if self.current_char() == '/' and self.pos + 1 < len(self.source):
            if self.source[self.pos + 1] == '/':
                while self.current_char() and self.current_char() != '\n' :
                    self.advance()
                return True
            
            if self.source[self.pos + 1] == '*':
                self.advance()
                self.advance()
                while self.current_char():
                    if self.current_char() == '*' and self.pos + 1 < len(self.source) and self.source[self.pos+1] == '/':
                        self.advance()
                        self.advance()
                        return True
                    self.advance()
                raise SyntaxError(f"Unterminated comment at line {self.line}")
        return False

    def read_identifier(self):
        start = self.pos 
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            self.advance()
        return self.source[start:self.pos] 
    
    def read_number(self):
        start = self.pos
        while self.current_char() and (self.current_char().isdigit() or self.current_char()=='_'):
            self.advance()
        return self.source[start:self.pos]

    
    def tokenize(self):
        while self.current_char():
            self.skip_whitespace()
            if self.skip_comment():
                continue
            if not self.current_char():
                break

            char = self.current_char()

            if char.isdigit():
                num = self.read_number()
                self.tokens.append(Token(TokenType.NUMBER,num,self.line))
            
            elif char.isalpha() or char == '_':
                word = self.read_identifier()
                if word in KEYWORDS:
                    self.tokens.append(Token(TokenType.KEYWORD,word,self.line))
                else :
                    self.tokens.append(Token(TokenType.IDENTIFIER,word,self.line))

            elif char == '=' and self.pos + 1 < len(self.source) and self.source[self.pos+1] == '=':
                self.tokens.append(Token(TokenType.EQ,'==',self.line))
                self.advance()
                self.advance()

            elif char == '!' and self.pos + 1 < len(self.source) and self.source[self.pos+1] == '=':
                self.tokens.append(Token(TokenType.NEQ,'!=',self.line))
                self.advance()
                self.advance()

            elif char == '=':
                self.tokens.append(Token(TokenType.ASSIGN, '=', self.line))
                self.advance()
            elif char == '+':
                self.tokens.append(Token(TokenType.PLUS, '+', self.line))
                self.advance()
            elif char == '-':
                self.tokens.append(Token(TokenType.MINUS, '-', self.line))
                self.advance()
            elif char == '*':
                self.tokens.append(Token(TokenType.STAR, '*', self.line))
                self.advance()
            elif char == '/':
                self.tokens.append(Token(TokenType.SLASH, '/', self.line))
                self.advance()
            elif char == '<':
                self.tokens.append(Token(TokenType.LT, '<', self.line))
                self.advance()
            elif char == '>':
                self.tokens.append(Token(TokenType.GT, '>', self.line))
                self.advance()
            # Delimiters
            elif char == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', self.line))
                self.advance()
            elif char == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', self.line))
                self.advance()
            elif char == '{':
                self.tokens.append(Token(TokenType.LBRACE, '{', self.line))
                self.advance()
            elif char == '}':
                self.tokens.append(Token(TokenType.RBRACE, '}', self.line))
                self.advance()
            elif char == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, ';', self.line))
                self.advance()
            elif char == ',':
                self.tokens.append(Token(TokenType.COMMA, ',', self.line))
                self.advance()

            else:
                raise SyntaxError(f"Unexpected character '{char}' at line {self.line}")
        self.tokens.append(Token(TokenType.EOF,'',self.line))
        return self.tokens