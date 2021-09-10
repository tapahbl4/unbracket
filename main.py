import fileops
import lexer

if __name__ == '__main__':
    source_code = fileops.read('example.krl')
    token_line_list = lexer.parse_tokens(source_code)
    # print(token_line_list)
