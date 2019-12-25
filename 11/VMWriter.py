class VMWriter:
    def __init__(self):
        pass

    def write_push(self, segment):
        pass

    def write_pop(self, segment):
        pass

    def write_arithmetic(self, command):
        pass

    def write_label(self, label):
        pass

    def write_goto(self, label):
        pass

    def write_if(self, label):
        pass

    def write_call(self, name, num_of_args):
        pass

    def write_function(self, name, num_of_locals):
        pass

    def write_return(self):
        pass

    def close(self):
        pass
