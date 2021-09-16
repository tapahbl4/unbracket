from tokens import Token, TokenType, TokenList
from lexer import get_token_type


class RPNException(Exception):
    def __init__(self, message):
        super().__init__(message)


def eval_string(value: str):
    return eval_tokens(TokenList([get_token_type(x) for x in value.split()]))


def eval_tokens(token_list: TokenList):
    ops_len, lit_len = 0, 0
    for x in token_list:
        if x.type == TokenType.OPERATION:
            ops_len += 1
        elif x.type == TokenType.LITERAL_NUMBER or x.type == TokenType.LITERAL_FLOAT:
            lit_len += 1
    if ops_len + 1 != lit_len:
        raise RPNException('Invalid expression')
    stack = []
    for t in token_list:
        if t.type == TokenType.OPERATION:
            op2, op1 = stack.pop(), stack.pop()
            stack.append(str(eval(op1 + t.value + op2)))
        else:
            stack.append(t.value)
    return stack.pop()
