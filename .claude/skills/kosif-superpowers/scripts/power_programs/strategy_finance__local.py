"""PROD-17 PuLP linear/integer program (env_scope=local: needs pip pulp + a solver such as highspy)."""
from __future__ import annotations
from ._mind_common import save, eq


def prod17(work):
    import pulp
    solver = pulp.getSolver(pulp.listSolvers(onlyAvailable=True)[0], msg=False)
    m = pulp.LpProblem("budget", pulp.LpMaximize)
    # finite bounds: CP-SAT refuses unbounded integers, the others do not mind
    a, b = m.add_variable("a", 0, 1000, cat="Integer"), m.add_variable("b", 0, 1000, cat="Integer")
    m += 3 * a + 2 * b
    m += a + b <= 100
    m += a <= 60
    status = m.solve(solver)
    res = {"a": a.value(), "b": b.value(), "objective": pulp.value(m.objective),
           "status": getattr(getattr(status, "status", status), "name", str(status)),
           "solver": solver.name, "pulp": pulp.__version__}
    save(work, "lp.json", res)
    return [eq("status", res["status"], "Optimal"), eq("objective", res["objective"], 260.0, tol=1e-6),
            eq("a", res["a"], 60.0, tol=1e-6), eq("b", res["b"], 40.0, tol=1e-6)]


PROGRAMS = {"PROD-17": prod17}
