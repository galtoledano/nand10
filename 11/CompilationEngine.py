from Tokenizer import Tokenizer
from VMWriter import VMWriter
from SymbolTable import SymbolTable


class CompilationEngine:
    XML_LINE = "<{0}> {1} </{0}>\n"
    COMPARE_SYM_REPLACER = {'<': "&lt;", '>': "&gt;", '"': "&quot;", '&': "&amp;"}
    KEYWORD_CONSTANT = ("true", "false", "null", "this")

    def __init__(self, input_stream, output_stream):
        """
        constructor of the Compilation Engine object
        :param input_stream: the input stream
        :param output_stream: the output stream
        """
        self.__tokenizer = Tokenizer(input_stream)  # Tokenizer object
        self.__output = VMWriter(output_stream)
        self.__symbol = SymbolTable()
        self.__class_name = ""
        self.__statements = {"let": self.compile_let, "if": self.compile_if, "while": self.compile_while,
                             "do": self.compile_do, "return": self.compile_return}
        self.compile_class()
        # self.__output.close()

    def write_xml(self):
        """
        writing xml line
        """
        if self.__tokenizer.token_type() == "stringConstant":
            self.__output.write(self.XML_LINE.format(self.__tokenizer.token_type(), self.__tokenizer.string_val()))
        elif self.__tokenizer.get_value() in self.COMPARE_SYM_REPLACER:
            xml_val = self.COMPARE_SYM_REPLACER[self.__tokenizer.get_value()]
            self.__output.write(self.XML_LINE.format(self.__tokenizer.token_type(), xml_val))
        else:
            self.__output.write(self.XML_LINE.format(self.__tokenizer.token_type(), self.__tokenizer.get_value()))

    def compile_class(self):
        """
        compiling the program from the class definition
        """
        # self.__output.write("<class>\n")
        # self.write_xml()
        self.__tokenizer.advance()  # skip "class"
        self.__class_name = self.__tokenizer.get_value()
        # self.write_xml()
        self.__tokenizer.advance()  # skip class name
        # self.write_xml()
        self.__tokenizer.advance()  # skip {
        current_token = self.__tokenizer.get_value()
        while current_token == "static" or current_token == "field":
            self.compile_class_var_dec()
            current_token = self.__tokenizer.get_value()
        while current_token == "constructor" or current_token == "function" or current_token == "method":
            self.compile_subroutine_dec()
            current_token = self.__tokenizer.get_value()
        # self.write_xml()
        # self.__output.write("</class>\n")
        self.__output.close()

    def compile_class_var_dec(self):
        """
        compiling the program from the class's declaration on vars
        """
        current_token = self.__tokenizer.get_value()
        while current_token == "static" or current_token == "field":
            # self.__output.write("<classVarDec>\n")
            # self.write_xml()
            index = self.__symbol.var_count(current_token)
            self.__tokenizer.advance() # get token type
            token_type = self.__tokenizer.get_value()
            self.__output.write_push(current_token, index)
            self.__tokenizer.advance() # get token name
            token_name = self.__tokenizer.get_value()
            self.__symbol.define(token_name, token_type, current_token)
            self.__tokenizer.advance()
            # self.write_xml()
            # self.__tokenizer.advance()
            # self.write_xml()
            # self.__tokenizer.advance()
            while self.__tokenizer.get_value() == ",":
                # self.write_xml()  # write ,
                self.__tokenizer.advance() # get token name
                token_name = self.__tokenizer.get_value()
                index = self.__symbol.var_count(current_token) # get new index
                self.__output.write_push(current_token, index)
                self.__symbol.define(token_name, token_type, current_token)
                self.__tokenizer.advance()
                # self.write_xml()  # write value
                # self.__tokenizer.advance()
            # self.write_xml()
            self.__tokenizer.advance()
            current_token = self.__tokenizer.get_value()
            # self.__output.write("</classVarDec>\n")

    def compile_subroutine_body(self):
        """
        compiling the program's subroutine body
        """
        # self.__output.write("<subroutineBody>\n")
        # self.write_xml()  # write {
        self.__tokenizer.advance()  # skip {
        while self.__tokenizer.get_value() == "var":
            self.compile_var_dec()
        self.compile_statements()
        # self.write_xml()  # write }
        self.__tokenizer.advance()  # skip }
        # self.__output.write("</subroutineBody>\n")

    def compile_subroutine_dec(self):
        """
        compiling the program's subroutine declaration
        """
        # self.__output.write("<subroutineDec>\n")
        # self.write_xml()  # write constructor/function/method

        self.__tokenizer.advance()  # skip constructor/function/method
        return_value = self.__tokenizer.get_value()
        self.__tokenizer.advance()
        func_name = self.__tokenizer.get_value()
        self.__tokenizer.advance()
        func_args = self.compile_parameter_list()
        self.__output.write_function(func_name, func_args)
        self.compile_subroutine_body()
        if return_value == "void":
            self.__output.write_pop("temp", "0")
        # self.__output.write("</subroutineDec>\n")

    def compile_parameter_list(self):
        """
        compiling a parameter list
        """
        # todo returns the number og args !
        # self.write_xml()  # write (
        counter = 0
        self.__tokenizer.advance()  # skip (
        # self.__output.write("<parameterList>\n")
        if self.__tokenizer.get_value() != ")":
            # self.write_xml()  # write type
            self.__tokenizer.advance()  # skip type
            # self.write_xml()  # write varName
            self.__tokenizer.advance()  # skip var name
            counter += 1
            while self.__tokenizer.get_value() == ",":
                # self.write_xml()  # write ,
                self.__tokenizer.advance()  # skip ,
                # self.write_xml()  # type
                self.__tokenizer.advance()  # skip type
                # self.write_xml()  # varName
                self.__tokenizer.advance()  # skip varName
                counter += 1
        # self.__output.write("</parameterList>\n")
        # self.write_xml()  # write )
        self.__tokenizer.advance()
        return counter

    def compile_var_dec(self):
        """
        compiling function's var declaration
        """
        # self.__output.write("<varDec>\n")
        # self.write_xml()  # write var
        token_kind = self.__tokenizer.get_value()
        self.__tokenizer.advance()
        # self.write_xml()  # write type
        token_type = self.__tokenizer.get_value()
        self.__tokenizer.advance()
        # self.write_xml()  # write varName
        token_name = self.__tokenizer.get_value()
        self.__tokenizer.advance()
        index = self.__symbol.var_count(token_kind)
        self.__output.write_push(token_kind, index)
        self.__symbol.define(token_name, token_type, token_kind)
        while self.__tokenizer.get_value() == ",":
            # self.write_xml()  # write ,
            self.__tokenizer.advance()  # skip ,
            # self.write_xml()
            token_name = self.__tokenizer.get_value()
            index = self.__symbol.var_count(token_kind)
            self.__output.write_push(token_kind, index)
            self.__symbol.define(token_name, token_type, token_kind)
            self.__tokenizer.advance()
        # self.write_xml()  # write ;
        self.__tokenizer.advance()  # skip ;
        # self.__output.write("</varDec>\n")

    def compile_statements(self):
        """
        compiling statements
        """
        key = self.__tokenizer.get_value()
        # self.__output.write("<statements>\n")
        if key != "}":
            while key in self.__statements:
                self.__statements[self.__tokenizer.get_value()]()
                key = self.__tokenizer.get_value()
        # self.__output.write("</statements>\n")

    def compile_do(self):
        """
        compiling do call
        """
        # self.__output.write("<doStatement>\n")
        # self.write_xml()  # write do
        self.__tokenizer.advance()  # skip do
        self.subroutine_call()
        # self.write_xml()  # write ;
        self.__tokenizer.advance()  # skip ;
        # self.__output.write("</doStatement>\n")

    def compile_let(self):
        """
        compiling let call
        """
        # self.__output.write("<letStatement>\n")
        # self.write_xml()  # write let
        self.__tokenizer.advance()  # skip let
        # self.write_xml()  # write varName
        var_name = self.__tokenizer.get_value()
        self.__tokenizer.advance()
        # if self.__tokenizer.get_value() == "[":  # todo handle array
        #     self.write_xml()  # write [
        #     self.__tokenizer.advance()
        #     self.compile_expression()
        #     self.write_xml()  # write ]
        #     self.__tokenizer.advance()
        # self.write_xml()  # write =
        self.__tokenizer.advance()  # skip =
        self.compile_expression()  # todo push the value to the stack
        # self.write_xml()  # write ;
        self.__tokenizer.advance()  # skip ;
        # self.__output.write("</letStatement>\n")
        var_kind = self.__symbol.kind_of(var_name)
        var_index = self.__symbol.index_of(var_name)
        self.__output.write_pop(var_kind, var_index)

    def compile_while(self):
        """
        compiling while loop call
        """
        self.__output.write("<whileStatement>\n")
        self.write_xml()  # write while
        self.__tokenizer.advance()
        self.write_xml()  # write (
        self.__tokenizer.advance()
        self.compile_expression()
        self.write_xml()  # write )
        self.__tokenizer.advance()
        self.write_xml()  # write {
        self.__tokenizer.advance()
        self.compile_statements()
        self.write_xml()  # write }
        self.__tokenizer.advance()
        self.__output.write("</whileStatement>\n")

    def compile_return(self):
        """
        compiling return statement
        """
        self.__output.write("<returnStatement>\n")
        self.write_xml()  # write return
        self.__tokenizer.advance()
        if self.__tokenizer.get_value() != ";":
            self.compile_expression()
        self.write_xml()  # write ;
        self.__tokenizer.advance()
        self.__output.write("</returnStatement>\n")

    def compile_if(self):
        """
        compiling if condition
        """
        self.__output.write("<ifStatement>\n")
        self.write_xml()  # write if
        self.__tokenizer.advance()
        self.write_xml()  # write (
        self.__tokenizer.advance()
        self.compile_expression()
        self.write_xml()  # write )
        self.__tokenizer.advance()
        self.write_xml()  # write {
        self.__tokenizer.advance()
        self.compile_statements()
        self.write_xml()  # write }
        self.__tokenizer.advance()
        if self.__tokenizer.get_value() == "else":
            self.write_xml()  # write else
            self.__tokenizer.advance()
            self.write_xml()  # write {
            self.__tokenizer.advance()
            self.compile_statements()
            self.write_xml()  # write }
            self.__tokenizer.advance()
        self.__output.write("</ifStatement>\n")

    def compile_expression(self):
        """
        compiling expressions
        """
        self.__output.write("<expression>\n")
        self.compile_term()
        while self.__tokenizer.is_operator():
            self.write_xml()  # write the operator
            self.__tokenizer.advance()
            self.compile_term()
        self.__output.write("</expression>\n")

    def compile_term(self):
        """
        compiling any kind of terms
        """
        # dealing with unknown token
        self.__output.write("<term>\n")
        curr_type = self.__tokenizer.token_type()
        # handle consts
        if curr_type == "integerConstant" or curr_type == "stringConstant":
            self.write_xml()  # write the int \ string
            self.__tokenizer.advance()

        # handle const keyword
        elif curr_type == "keyword" and self.__tokenizer.get_value() in self.KEYWORD_CONSTANT:
            self.__tokenizer.set_type("keywordConstant")
            self.write_xml()  # write key word
            self.__tokenizer.advance()

        elif curr_type == "identifier":
            # handle var names
            if self.__tokenizer.get_next_token() != "(" and self.__tokenizer.get_next_token() != ".":
                self.write_xml()  # write the var name
                self.__tokenizer.advance()
                if self.__tokenizer.get_value() == "[":
                    self.write_xml()  # write [
                    self.__tokenizer.advance()
                    self.compile_expression()
                    self.write_xml()  # write ]
                    self.__tokenizer.advance()
            # handle function calls
            else:
                self.subroutine_call()
        # handle expression
        elif curr_type == "symbol" and self.__tokenizer.get_value() == "(":
            self.write_xml()  # write (
            self.__tokenizer.advance()
            self.compile_expression()
            self.write_xml()  # write )
            self.__tokenizer.advance()

        # handle - \ ~
        elif self.__tokenizer.get_value() == "-" or self.__tokenizer.get_value() == "~":
            self.write_xml()  # write -\~
            self.__tokenizer.advance()
            self.compile_term()
        self.__output.write("</term>\n")

    def subroutine_call(self):
        """
        compiling the program's subroutine call
        """
        if self.__tokenizer.get_next_token() == ".":
            self.write_xml()  # write name
            self.__tokenizer.advance()
            self.write_xml()  # write .
            self.__tokenizer.advance()
        self.write_xml()  # write name
        self.__tokenizer.advance()
        self.write_xml()  # write (
        self.__tokenizer.advance()
        self.compile_expression_list()
        self.write_xml()  # write )
        self.__tokenizer.advance()

    def compile_expression_list(self):
        """
        compiling expression list
        """
        self.__output.write("<expressionList>\n")
        if self.__tokenizer.get_value() != ")":
            self.compile_expression()
            while self.__tokenizer.get_value() == ",":
                self.write_xml()  # write ,
                self.__tokenizer.advance()
                self.compile_expression()
        self.__output.write("</expressionList>\n")


