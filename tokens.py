from enum import Enum
from dataclasses import dataclass


class TokenType(Enum):
    KEYWORD = 1
    OPERATION = 2
    VARIABLE = 3
    FUNCTION = 4
    STD_VARIABLE = 5
    STD_FUNCTION = 6
    UNKNOWN = 7
    TYPE = 8
    NEWLINE = 9
    LITERAL_STRING = 10
    LITERAL_NUMBER = 11
    LITERAL_FLOAT = 12
    LITERAL_BOOLEAN = 13

    def __str__(self):
        return self.name


@dataclass
class Token:
    type: TokenType
    value: str = None


class TokenList(list):
    def extract(self):  # TODO: Add recursive extracting
        return
