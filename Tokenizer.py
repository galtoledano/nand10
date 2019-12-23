import os


class Tokenizer:
    keyWords = ("class", "constructor", "function", "method", "field", "static", "var", "int", "char",
                "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return")
    symbols = ("(", ")", "{", "}", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~")

    def __init__(self, file):
        self.__file = []
        self.__index = 0
        self.__current_token = self.advance()
        self.__current_token_type = self.token_type()
        self.__read_file(file)

    def __remove_invalid_syntax(self, line):
        if str(os.path.sep) in line:
            index = line.find(str(os.path.sep))
            line = line[:index]
        line = line.replace("\n", "")
        line = line.rstrip()
        return line

    def __read_file(self, original_file):
        file = open(original_file, 'r')
        line = file.readline()
        while line:
            current_line = self.__remove_invalid_syntax(line)
            if current_line != "":
                self.__file.append(current_line)
            line = file.readline()
        file.close()

    def has_more_tokens(self):
        if self.__index != len(self.__file):
            return True

    def advance(self):
        # gets the next token from the input
        return "as33"

    def token_type(self):
        # returns the token's type. dict ?
        if self.__current_token in self.keyWords:
            return "keyWord"
        elif self.__current_token in self.symbols:
            return "symbol"
        elif self.__current_token.isdigit():
            return "intVal"
        elif self.__current_token[0] == '"' and self.__current_token[-1] == '"':
            return "stringVal"
        else:
            return "identifier"


    def keyword(self):
        # return keyword
        pass

    def symbol(self):
        # return char
        return chr(self.__current_token)

    def identifier(self):
        # returns string
        return str(self.__current_token)

    def int_val(self):
        return int(self.__current_token)

    def string_val(self):
        return str(self.__current_token)
