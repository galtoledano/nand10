from Tokenizer import Tokenizer


class CompilationEngine:
    XML_LINE = "<{0}> {1} </{0}> \n"

    def __init__(self, input_stream, output_stream):
        """

        :param input_stream:
        :param output_stream:
        """
        self.__tokenizer = Tokenizer(input_stream)  # Tokenizer object
        self.__output = open(output_stream + ".xml", "w")
        self.compile_class()

    def write_xml(self):
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
        if currToken == "static" or currToken == "filed":
            self.compile_class_var_dec()
        currToken = self.__tokenizer.get_value()
        if currToken == "constructor" or currToken == "function" or currToken == "method":
            self.compile_subroutine_dec()
        self.write_xml()
        self.__output.write("</class> \n")

    def compile_class_var_dec(self):
        currToken = self.__tokenizer.get_value()
        self.__output.write("<classVarDec>\n")  # todo : ok ?
        while currToken == "static" or currToken == "filed":
            self.write_xml()
            self.__tokenizer.advance()
            self.write_xml()
            self.__tokenizer.advance()
            self.write_xml()
            self.__tokenizer.advance()

            while self.__tokenizer.get_value() == ",":
                self.__tokenizer.advance()  # todo need to write , ?
                self.write_xml()
                self.__tokenizer.advance()

            self.write_xml()
            self.__tokenizer.advance()
            currToken = self.__tokenizer.get_value()

        self.__output.write("</classVarDec>\n")

    def compile_subroutine_body(self):
        self.__output.write("<subroutineBody>\n")
        self.write_xml() # write {
        self.__tokenizer.advance()
        if self.__tokenizer.get_value() == "var":
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
        self.write_xml()  # write type
        self.__tokenizer.advance()
        self.write_xml()  # write varName
        self.__tokenizer.advance()
        while self.__tokenizer.get_value() == ",":
            self.__tokenizer.advance()  # todo need to write , ?
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
            self.__tokenizer.advance()  # todo need to write , ?
            self.write_xml()
            self.__tokenizer.advance()
        self.write_xml()  # write ;
        self.__tokenizer.advance()
        self.__output.write("</varDec>\n")

    def compile_statements(self):
        pass

    def compile_do(self):
        pass

    def compile_let(self):
        self.__output.write("<letStatement>\n")
        self.write_xml()  # write let
        self.__tokenizer.advance()
        self.write_xml()  # write varName
        self.__tokenizer.advance()
        if self.__tokenizer.get_value() == "[":
            self.compile_expression()  # todo add the [ outside ?
        self.write_xml()  # write =
        self.__tokenizer.advance()
        self.compile_expression()
        self.write_xml()  # write ;
        self.__tokenizer.advance()
        self.__output.write("</letStatement>\n")

    def compile_while(self):
        self.__output.write("<while>\n")  # todo whileStatement ?
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
        self.__output.write("</while>\n")

    def compile_return(self):
        self.__output.write("<return>\n")
        self.write_xml()  # write return
        self.__tokenizer.advance()
        if self.__tokenizer.get_value() != ";":
            self.compile_expression()  # todo not writing ;
        self.write_xml()  # write ;
        self.__tokenizer.advance()
        self.__output.write("</return>\n")

    def compile_if(self):
        self.__output.write("<if>\n")
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
        self.__output.write("</if>\n")

    def compile_expression(self):
        pass

    def compile_term(self):
        # dealing with unknown token
        pass

    def compile_expression_list(self):
        pass