"""Shared test utilities for extracting functions from script-style modules."""

import ast
import os


def extract_functions(module_path):
    """Extract function definitions from a Python file without executing module-level code.

    Returns a namespace dict containing only the defined functions,
    with necessary imports available.
    """
    with open(module_path) as f:
        source = f.read()

    tree = ast.parse(source)

    # Collect import statements and function definitions
    import_stmts = []
    func_stmts = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            import_stmts.append(node)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func_stmts.append(node)

    # Build a new module with only imports + functions
    new_module = ast.Module(body=import_stmts + func_stmts, type_ignores=[])
    ast.fix_missing_locations(new_module)

    code = compile(new_module, module_path, "exec")
    namespace = {}
    exec(code, namespace)
    return namespace
