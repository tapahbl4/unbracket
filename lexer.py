import re
from enum import Enum
from dataclasses import dataclass

KEYWORDS = ['let', 'function', 'print', 'return', 'import', 'input', 'if', 'then', 'else', 'elif', 'switch', 'case',
            'default', 'for', 'end', 'while', 'do', 'to', 'and', 'or', 'not']
OPS = ['==', '=', '+', '-', '*', '/', '%', '^', ':', '(', ')', '[', ']']
TYPES = ['number', 'string', 'float', 'boolean']
ESCAPED_STRING = '__ESCAPED_STRING__'

regexps = {
    'escaped': r'\'[\w\s]+\'\s*$',
    'var_name': r'^[a-zA-Z_]+[\w_]*$',
    'literal_number': r'^\-?\d+$',
    'literal_string': r'^\'.*\'$',
    'literal_float': r'^\-?\d*\.\d*$',
    'literal_boolean': r'^true|false$',
}


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


def parse_tokens(string_list):
    token_line_list = []
    escaped_strings = []
    escaped_counter = 0
    prev_token = None
    for line in string_list:
        escaped = re.search(regexps['escaped'], line)
        if escaped:
            escaped_strings.append(escaped.group(0))
            line = re.sub(regexps['escaped'], ESCAPED_STRING, line)
        line = re.sub(regexps['escaped'], ESCAPED_STRING, line)
        for op in OPS:
            line = str(line).replace(op, f' %s ' % op)
        pre_tokens = str(line).split()
        tokens = []
        for token in pre_tokens:
            if token == ESCAPED_STRING:
                token = escaped_strings[escaped_counter]
                escaped_counter = + 1
            tokens.append(get_token_type(token, prev_token))
            prev_token = token
        tokens.append(Token(type=TokenType.NEWLINE))
        token_line_list.append(tokens)
        print(tokens) # TODO: Remove on prod
    return token_line_list


def is_correct_var_name(value):
    return re.match(regexps['var_name'], str(value))


def is_literal(value):
    t_type = TokenType.UNKNOWN
    if re.match(regexps['literal_number'], value):
        t_type = TokenType.LITERAL_NUMBER
    elif re.match(regexps['literal_string'], value):
        t_type = TokenType.LITERAL_STRING
    elif re.match(regexps['literal_float'], value):
        t_type = TokenType.LITERAL_FLOAT
    elif re.match(regexps['literal_boolean'], value):
        t_type = TokenType.LITERAL_BOOLEAN
    return Token(type=t_type, value=value)


def get_token_type(value, prev_token=None):
    if value in KEYWORDS:
        return Token(type=TokenType.KEYWORD, value=value)
    elif value in OPS:
        return Token(type=TokenType.OPERATION, value=value)
    elif value in TYPES:
        return Token(type=TokenType.TYPE, value=value)
    elif is_correct_var_name(value):
        if prev_token == 'function':
            return Token(type=TokenType.FUNCTION, value=value)
        return Token(type=TokenType.VARIABLE, value=value)
    else:
        return is_literal(value)
