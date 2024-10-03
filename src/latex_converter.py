class LatexPyomoConverter:
    def __init__(self):
        pass

    def convert(self, latex_string):
        lhs, forall_variables = latex_string.split("\\forall")
        iterables = self.extract_iterables(forall_variables)
        # TODO: turn sums into functions
        func = self.extract_function(lhs)
        return func, iterables

    def extract_iterables(self, forall_variables):
        return forall_variables.replace(" ", "").split(",")

    def extract_function(self, lhs):
        def inner_func(*args):
            pass

        return inner_func
