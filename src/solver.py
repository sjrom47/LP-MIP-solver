# module for building the pyomo model
import pyomo.environ as pe

# module for solving the pyomo model
import pyomo.opt as po

import itertools


class Solver:
    def __init__(self) -> None:
        self.model = pe.ConcreteModel()

    def add_set(self, set_name, set_values):
        setattr(self.model, set_name, pe.Set(initialize=set_values))

    def add_params(self, params_names, params_values):
        setattr(
            self.model,
            "_".join(params_names),
            pe.Param(*params_names, initialize=params_values),
        )

    def add_variable(self, variable_name, variable_dependencies, variable_range):
        setattr(
            self.model,
            variable_name,
            pe.Var(*variable_dependencies, within=variable_range),
        )

    def add_objective_function(self, obj_func, sense=pe.minimize):
        setattr(self.model, "cost", pe.Objective(rule=obj_func), sense=sense)

    def add_constraint(self, constraint_list, function, iterables):
        if not getattr(self.model, constraint_list, None):
            setattr(self.model, constraint_list, pe.ConstraintList())
        model_iterables = [
            getattr(self.model, iterable) for iterable in iterables.copy()
        ]

        for combination in itertools(model_iterables):
            constraint_expr = function(*combination)
            # TODO: check if this syntax works (maybe getattr.add?)
            self.model.constraint_list.add(constraint_expr)

    def solve(self, solver="gurobi"):
        solver = po.SolverFactory(solver)
        results = solver.solve(self.model, tee=True)
        print(f"Optimal value {pe.value(self.model.cost)}")

    # TODO: check conditions
    def show_results(variable, iterables):
        pass
