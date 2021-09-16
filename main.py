import fileops
import lexer
from rpn import eval_string

if __name__ == '__main__':
    source_code = fileops.read('example.unb')
    token_line_list = lexer.parse_tokens(source_code)
    # print(eval_string('3 4 + 4 * 7 3 - 5 * -'))
