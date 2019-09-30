class indent:
    shift = 2
    value = 0

    @staticmethod
    def str():
        return indent.value * " "

    @staticmethod
    def incr():
        indent.value += indent.shift

    @staticmethod
    def decr():
        indent.value -= indent.shift
