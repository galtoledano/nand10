import os


class Tokenizer:
    keyWords = ("class", "constructor", "function", "method", "field", "static", "var", "int", "char",
                "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return")
    symbols = ("(", ")", "{", "}", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~")

    def __init__(self, file):
        self.__file = []
        self.__index = 0
        self.__current_token = None
        self.__current_token_type = None
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
                # add spaces between symbols
                for char in current_line:
                    if char in self.symbols:
                        current_line = current_line.replace(char, " " + char + " ")
                self.__file += current_line.split()
            line = file.readline()
        file.close()
        self.find_string()

    def find_string(self):
        final_file = []
        is_word = False
        temp = ""
        for i in range(len(self.__file)):
            x = self.__file[i]
            if is_word:
                temp += self.__file[i] + " "
                if self.__file[i].endswith('"'):
                    is_word = False
                    final_file.append(temp)
            else:
                if self.__file[i].startswith('"'):
                    is_word = True
                    temp = self.__file[i] + " "
                else:
                    final_file.append(self.__file[i])
        self.__file = final_file
        print(self.__file)

    def has_more_tokens(self):
        if self.__index != len(self.__file) - 1:
            return True
        if len(self.__current_token) == 1 and self.__current_token == "}": #todo check that it not hidding bags
            return False
        return True

    def advance(self):
        check = self.__file[self.__index]
        if check in self.keyWords or check in self.symbols:
            self.__current_token = check
        elif check[0] in self.symbols:
            temp1 = check[0]
            temp2 = check[1:]

        self.__index += 1
        self.token_type()

    def token_type(self):
        # returns the token's type.
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
        return str(self.__current_token)

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


    def find_string2(self):
        lst = self.__file
        is_word = False
        temp = ""
        counter = 0
        i = 0
        while i < len(lst):
            x = lst[i]
            if is_word:
                temp += lst[i] + " "
                counter += 1
                if lst[i].endswith('"'):
                    is_word = False
                    i = i + counter
                    self.__file = self.__file[:index] + [temp] + self.__file[i:]
                    counter = 0
                else:
                    i += 1

            else:
                if lst[i].startswith('"'):
                    is_word = True
                    index = i
                    temp = lst[i] + " "
                i += 1
        print(self.__file)