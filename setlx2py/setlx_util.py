#------------------------------------------------------------------------------
# setlx2py: setlx_util.py
#
# Central place for functions which are needed in at least
# two different files
#
# Copyright (C) 2014, Jan-Christoph Klie
# License: Apache v2
#------------------------------------------------------------------------------

import sys
import re

from cStringIO import StringIO

from setlx2py.setlx_parser import Parser
from setlx2py.setlx_ast_transformer import AstTransformer
from setlx2py.setlx_codegen import Codegen

from setlx2py.setlx_builtin import *

HEADER = """
from setlx2py.builtin.setlx_functions import *
from setlx2py.builtin.setlx_set import SetlxSet
from setlx2py.builtin.setlx_list import SetlxList
from setlx2py.builtin.setlx_string import SetlxString

"""

parser = Parser()
transformer = AstTransformer()
generator = Codegen()

def error_msg(source, compiled=None, e=None):
    msg = 'Could not run stuff:\n'
    msg += 'Source:\n' + source + '\n'
    
    if compiled:
        msg += 'Compiled:\n' + compiled
    if e:
        msg += 'Reason:\n'
        msg += e.__class__.__name__ + '\n'
        msg += str(e) + '\n'
        msg += 'Line: ' + str(get_exception_line(e))
    return msg

def get_exception_line(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    return exc_tb.tb_lineno

def compile_setlx(source, verbose=False, print_ast=False):
    ast = parser.parse(source)
    transformer.visit(ast)
    
    if verbose:
        print('Source: \n' + source)

    if print_ast:
        print(ast)

    compiled = generator.visit(ast)
    
    compiled = HEADER + compiled
    if verbose:
        print('Compliled: \n' + compiled)
    return compiled


def run(source, ns={}, verbose=False, print_ast=False):
    compiled = compile_setlx(source, verbose, print_ast)
    
    try:
        code = compile(compiled, '<string>', 'exec')    
        exec(code, ns)
    except Exception as e:
        msg = error_msg(source, compiled, e=e)
        raise AssertionError(msg)

def parse_statements(text, verbose=False):
    ast = parser.parse(text) # FileAST
    if verbose: print(ast)
    transformer.visit(ast)
    if verbose: print(ast)
    return ast # List of statements

def parse_single_statement(text):
    return parse_statements(text).stmts[0] # first statement after FileAST
        