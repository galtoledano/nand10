class VMWriter:
    def __init__(self, output_path):
        self.__out = open(output_path, "w")

    def write_push(self, segment, index):
        self.__out.write("push {0} {1}".format(segment, index))

    def write_pop(self, segment, index):
        self.__out.write("pop {0} {1}".format(segment, index))

    def write_arithmetic(self, command):
        self.__out.write(command)  # todo lowercase ?

    def write_label(self, label):
        self.__out.write("({0})".format(label))

    def write_goto(self, label):
        self.__out.write("goto {0}".format(label))

    def write_if(self, label):
        self.__out.write("if-goto {0}".format(label))

    def write_call(self, name, num_of_args):
        self.__out.write("call {0} {1}".format(name, num_of_args))

    def write_function(self, name, num_of_locals):
        self.__out.write("function {0} {1}".format(name, num_of_locals))

    def write_return(self):
        self.__out.write("return")

    def close(self):
        self.__out.close()
