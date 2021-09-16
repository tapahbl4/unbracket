import re
from tokens import Token, TokenType, TokenList

KEYWORDS = ['let', 'function', 'print', 'return', 'import', 'input', 'if', 'then', 'else', 'elif', 'switch', 'case',
            'default', 'for', 'end', 'while', 'do', 'to', 'and', 'or', 'not', 'break', 'continue', 'array']
OPS = ['==', '=', '+', '-', '*', '/', '%', '^', ':']
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


def parse_tokens(string_list):
    token_line_list, escaped_strings, escaped_counter, prev_token = [], [], 0, None
    for line in string_list:
        escaped = re.search(regexps['escaped'], line)
        if escaped:
            escaped_strings.append(escaped.group(0))
            line = re.sub(regexps['escaped'], ESCAPED_STRING, line)
        line = re.sub(regexps['escaped'], ESCAPED_STRING, line)
        for op in OPS:
            line = str(line).replace(op, f' %s ' % op)
        pre_tokens = str(line).split()
        tokens = TokenList()
        for t in pre_tokens:
            if t == ESCAPED_STRING:
                t = escaped_strings[escaped_counter]
                escaped_counter = + 1
            tokens.append(get_token_type(t, prev_token))
            prev_token = t
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
