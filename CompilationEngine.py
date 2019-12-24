from Tokenizer import Tokenizer


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
        self.__output = open(output_stream, "w")
        self.__statements = {"let": self.compile_let, "if": self.compile_if, "while": self.compile_while,
                             "do": self.compile_do, "return": self.compile_return}
        self.compile_class()
        self.__output.close()

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
        self.__output.write("<class>\n")
        self.write_xml()
        self.__tokenizer.advance()
        self.write_xml()
        self.__tokenizer.advance()
        self.write_xml()
        self.__tokenizer.advance()
        currToken = self.__tokenizer.get_value()
        while currToken == "static" or currToken == "field":
            self.compile_class_var_dec()
            currToken = self.__tokenizer.get_value()
        while currToken == "constructor" or currToken == "function" or currToken == "method":
            self.compile_subroutine_dec()
            currToken = self.__tokenizer.get_value()
        self.write_xml()
        self.__output.write("</class>\n")

    def compile_class_var_dec(self):
        currToken = self.__tokenizer.get_value()
        while currToken == "static" or currToken == "field":
            self.__output.write("<classVarDec>\n")
            self.write_xml()
            self.__tokenizer.advance()
            self.write_xml()
            self.__tokenizer.advance()
            self.write_xml()
            self.__tokenizer.advance()
            while self.__tokenizer.get_value() == ",":
                self.write_xml()  # write ,
                self.__tokenizer.advance()
                self.write_xml()  # write value
                self.__tokenizer.advance()
            self.write_xml()
            self.__tokenizer.advance()
            currToken = self.__tokenizer.get_value()
            self.__output.write("</classVarDec>\n")

    def compile_subroutine_body(self):
        self.__output.write("<subroutineBody>\n")
        self.write_xml()  # write {
        self.__tokenizer.advance()
        while self.__tokenizer.get_value() == "var":
            self.compile_var_dec()
        self.compile_statements()
        self.write_xml()  # write }
        self.__tokenizer.advance()
        self.__output.write("</subroutineBody>\n")

    def compile_subroutine_dec(self):
        self.__output.write("<subroutineDec>\n")
        self.write_xml() # write constructor/function/method
        self.__tokenizer.advance()
        self.write_xml() # write return type
        self.__tokenizer.advance()
        self.write_xml() # write identifier name
        self.__tokenizer.advance()
        self.compile_parameter_list()
        self.compile_subroutine_body()
        self.__output.write("</subroutineDec>\n")

    def compile_parameter_list(self):
        self.write_xml()  # write (
        self.__tokenizer.advance()
        self.__output.write("<parameterList>\n")
        if self.__tokenizer.get_value() != ")":
            self.write_xml()  # write type
            self.__tokenizer.advance()
            self.write_xml()  # write varName
            self.__tokenizer.advance()
            while self.__tokenizer.get_value() == ",":
                self.write_xml()  # write ,
                self.__tokenizer.advance()
                self.write_xml()  # type
                self.__tokenizer.advance()
                self.write_xml()  # varName
                self.__tokenizer.advance()
        self.__output.write("</parameterList>\n")
        self.write_xml()  # write )
        self.__tokenizer.advance()

    def compile_var_dec(self):
        self.__output.write("<varDec>\n")
        self.write_xml()  # write var
        self.__tokenizer.advance()
        self.write_xml()  # write type
        self.__tokenizer.advance()
        self.write_xml()  # write varName
        self.__tokenizer.advance()
        while self.__tokenizer.get_value() == ",":
            self.write_xml() # write ,
            self.__tokenizer.advance()
            self.write_xml()
            self.__tokenizer.advance()
        self.write_xml()  # write ;
        self.__tokenizer.advance()
        self.__output.write("</varDec>\n")

    def compile_statements(self):
        key = self.__tokenizer.get_value()
        self.__output.write("<statements>\n")
        if key != "}":
            while key in self.__statements:
                self.__statements[self.__tokenizer.get_value()]()
                key = self.__tokenizer.get_value()
        self.__output.write("</statements>\n")

    def compile_do(self):
        self.__output.write("<doStatement>\n")
        self.write_xml()  # write do
        self.__tokenizer.advance()
        self.subroutine_call()
        self.write_xml()  # write ;
        self.__tokenizer.advance()
        self.__output.write("</doStatement>\n")

    def compile_let(self):
        self.__output.write("<letStatement>\n")
        self.write_xml()  # write let
        self.__tokenizer.advance()
        self.write_xml()  # write varName
        self.__tokenizer.advance()
        if self.__tokenizer.get_value() == "[":
            self.write_xml()  # write [
            self.__tokenizer.advance()
            self.compile_expression()
            self.write_xml()  # write ]
            self.__tokenizer.advance()
        self.write_xml()  # write =
        self.__tokenizer.advance()
        self.compile_expression()
        self.write_xml()  # write ;
        self.__tokenizer.advance()
        self.__output.write("</letStatement>\n")

    def compile_while(self):
        self.__output.write("<whileStatement>\n")  # todo whileStatement ?
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
        self.__output.write("<returnStatement>\n")
        self.write_xml()  # write return
        self.__tokenizer.advance()
        if self.__tokenizer.get_value() != ";":
            self.compile_expression()  # todo not writing ;
        self.write_xml()  # write ;
        self.__tokenizer.advance()
        self.__output.write("</returnStatement>\n")

    def compile_if(self):
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
        self.__output.write("<expression>\n")
        self.compile_term()
        while self.__tokenizer.is_operator():
            self.write_xml()  # write the operator
            self.__tokenizer.advance()
            self.compile_term()
        self.__output.write("</expression>\n")

    def compile_term(self):
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
        self.__output.write("<expressionList>\n")
        if self.__tokenizer.get_value() != ")":
            self.compile_expression()
            while self.__tokenizer.get_value() == ",":
                self.write_xml()  # write ,
                self.__tokenizer.advance()
                self.compile_expression()
        self.__output.write("</expressionList>\n")


