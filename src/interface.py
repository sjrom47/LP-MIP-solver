from src.solver import Solver
from src.latex_converter import LatexPyomoConverter
import itertools


class SetNotCreated(Exception):
    pass


class TerminalInterface:
    def __init__(self):
        print(
            """

      ___       ___           ___                       ___                    ___           ___           ___       ___           ___           ___     
     /\__\     /\  \         /\__\          ___        /\  \                  /\  \         /\  \         /\__\     /\__\         /\  \         /\  \    
    /:/  /    /::\  \       /::|  |        /\  \      /::\  \                /::\  \       /::\  \       /:/  /    /:/  /        /::\  \       /::\  \   
   /:/  /    /:/\:\  \     /:|:|  |        \:\  \    /:/\:\  \              /:/\ \  \     /:/\:\  \     /:/  /    /:/  /        /:/\:\  \     /:/\:\  \  
  /:/  /    /::\~\:\  \   /:/|:|__|__      /::\__\  /::\~\:\  \            _\:\~\ \  \   /:/  \:\  \   /:/  /    /:/__/  ___   /::\~\:\  \   /::\~\:\  \ 
 /:/__/    /:/\:\ \:\__\ /:/ |::::\__\  __/:/\/__/ /:/\:\ \:\__\          /\ \:\ \ \__\ /:/__/ \:\__\ /:/__/     |:|  | /\__\ /:/\:\ \:\__\ /:/\:\ \:\__\
 \:\  \    \/__\:\/:/  / \/__/~~/:/  / /\/:/  /    \/__\:\/:/  /          \:\ \:\ \/__/ \:\  \ /:/  / \:\  \     |:|  |/:/  / \:\~\:\ \/__/ \/_|::\/:/  /
  \:\  \        \::/  /        /:/  /  \::/__/          \::/  /            \:\ \:\__\    \:\  /:/  /   \:\  \    |:|__/:/  /   \:\ \:\__\      |:|::/  / 
   \:\  \        \/__/        /:/  /    \:\__\           \/__/              \:\/:/  /     \:\/:/  /     \:\  \    \::::/__/     \:\ \/__/      |:|\/__/  
    \:\__\                   /:/  /      \/__/                               \::/  /       \::/  /       \:\__\    ~~~~          \:\__\        |:|  |    
     \/__/                   \/__/                                            \/__/         \/__/         \/__/                   \/__/         \|__|    

"""
        )
        print("Welcome to LP-MIP solver!")
        self.solver = Solver()
        self.latex_converter = LatexPyomoConverter()
        self.create_problem()

    def create_problem(self):
        # TODO: create loop for unlimited sets
        self.create_set()
        # TODO: create loop for unlimited params
        self.create_params()

    def create_set(self):
        set_name = input("Enter the set name: ")
        set_values = (
            input("Enter the set values separated by comma: ")
            .replace(" ", "")
            .split(",")
        )
        set_values = [float(value) for value in set_values]
        self.solver.add_set(set_name, set_values)

    def create_params(self):
        params_names = input("Enter the params names separated by comma: ").split(",")
        set_values = [
            getattr(self.model, model_set, None) for model_set in params_names
        ]
        if None in set_values:
            raise SetNotCreated(
                "One or more sets not found in the model. Please create the sets first."
            )
        params_values = {}
        for combination in itertools.product():
            params_values[combination] = float(
                input(f"Enter the value for {params_names}: ")
            )
        self.solver.add_params(params_names, params_values)

    def create_variable(self):
        variable_name = input("Enter the variable name: ")
        variable_dependencies = input(
            "Enter the variable dependencies separated by comma: "
        ).split(",")
        variable_range = input(
            "Enter the variable range (Boolean, NonNegativeIntegers): "
        )
        self.solver.add_variable(variable_name, variable_dependencies, variable_range)
