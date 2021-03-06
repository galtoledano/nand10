class SymbolTable:
    def __init__(self):
        self.__class_scoop = {}  # static / field
        self.__subroutine_scoop = {}  # arg / var
        self.__counters = {"static": 0, "field": 0, "arg": 0, "var": 0}

    def start_subroutine(self):
        # delete all names at the privies subroutine scoop
        self.__subroutine_scoop = {}

    def define(self, name, this_type, kind):
        index = self.__counters[this_type]
        self.__counters[this_type] += 1
        if this_type == "static" or this_type == "field":
            self.__class_scoop[name] = [kind, this_type, index]
        else:
            self.__subroutine_scoop[name] = [kind, this_type, index]

    def var_count(self, kind):
        # returns int
        return self.__counters[kind]  # todo kind in uppercase ?

    def kind_of(self, name):
        # return kind
        if name in self.__subroutine_scoop.keys():
            return self.__subroutine_scoop[name][0]
        elif name in self.__class_scoop.keys():
            return self.__class_scoop[name][0]
        return "NONE"  # todo not a string ?

    def type_of(self, name):
        if name in self.__subroutine_scoop.keys():
            return self.__subroutine_scoop[name][1]
        elif name in self.__class_scoop.keys():
            return self.__class_scoop[name][1]
        return "NONE"  # todo not a string ?

    def index_of(self, name):
        if name in self.__subroutine_scoop.keys():
            return self.__subroutine_scoop[name][2]
        elif name in self.__class_scoop.keys():
            return self.__class_scoop[name][2]
        return "NONE"  # todo not a string ?
