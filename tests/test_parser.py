from nose.tools import eq_, with_setup, nottest

from setlx2py.setlx_lexer import Lexer
from setlx2py.setlx_parser import Parser

######################--   TEST UTIL --######################

parser = Parser()

def setup_func():
    global parser
    parser = Parser()

def teardown_func():
    parser = None

@with_setup(setup_func, teardown_func)        
def parse_statements(text):    
    root = parser.parse(text) # FileAST
    return root # List of statements

def parse_single_statement(text):
    return parse_statements(text).stmt[0] # first statement after FileAST
    
def assert_binop(text, operator, left, right):
    node = parse_single_statement(text)
    eq_(node.op, operator)
    eq_(node.left.value, left)
    eq_( node.right.value, right)

def assert_binop_triade(text, op1, op2, left, middle, right):
    """
    Asserts whether an expression of three operands
    and two binary operations are parsed as expected.

    The tree representation tested looks like the following:

    BinaryOp: op2
      BinaryOp: op1
        Constant: left
        Constant: middle
      Constant: right
    """
    binop1 = parse_single_statement(text)
    binop2 = binop1.left
    const = binop1.right
    try:
        eq_(binop1.op, op2)
        eq_(binop2.op, op1)
        eq_(binop2.left.value, left)
        eq_(binop2.right.value, middle)
        eq_(binop1.right.value, right)
    except AssertionError as e:
        binop1.show()
        raise e
    
def assert_unop(text, operator, val):
    node = parse_single_statement(text)
    eq_(node.op, operator)
    eq_(node.expr.value, val)
    
######################--   TESTS     --######################

@with_setup(setup_func, teardown_func)        
def test_should_be_creatable():
    assert parser is not None

def test_atomic_value_int():
    node = parse_single_statement('42;')
    eq_(node.value, 42)

def test_atomic_value_double():
    node = parse_single_statement('42.0;')
    assert abs(node.value - 42.0) < .001

def test_atomic_value_true():
    node = parse_single_statement('true;')
    eq_(node.value, True)

def test_atomic_value_false():
    node = parse_single_statement('false;')
    eq_(node.value,  False)

# Binary Operations

def test_binop_boolean():
    assert_binop('true <==> true;', '<==>', True, True)
    assert_binop('true <!=> true;', '<!=>', True, True)    
    assert_binop('true => true;', '=>', True, True)    
    assert_binop('true || false;', '||', True, False)
    assert_binop('true && false;', '&&', True, False)
    assert_binop('true == false;', '==', True, False)
    assert_binop('true != false;', '!=', True, False)
    assert_binop('true <  false;',  '<', True, False)
    assert_binop('true <= false;', '<=', True, False)
    assert_binop('true >  false;',  '>', True, False)
    assert_binop('true >= false;', '>=', True, False)

def test_binop_contain():
    assert_binop('true    in false;',    'in', True, False)
    assert_binop('true notin false;', 'notin', True, False)

def test_binop_sum():
    assert_binop('42 + 43;', '+', 42, 43)
    assert_binop('42 - 43;', '-', 42, 43)

def test_binop_product():
    assert_binop('42 *  43;',  '*', 42, 43)
    assert_binop('42 /  43;',  '/', 42, 43)
    assert_binop('42 \  43;', '\\', 42, 43)
    assert_binop('42 %  43;',  '%', 42, 43)
    assert_binop('42 >< 43;', '><', 42, 43)
    assert_binop('42 ** 43;', '**', 42, 43)

def test_binop_reduce():
    assert_binop('42 +/ 43;', '+/', 42, 43)
    assert_binop('42 */ 43;', '*/', 42, 43)

# Unary operations

def test_unop_prefix():
    assert_unop('+/ 42;',  '+/', 42)
    assert_unop('*/ 42;',  '*/', 42)
    assert_unop('-  42;',   '-', 42)
    assert_unop('#  42;',   '#', 42)
    assert_unop('@  42;',   '@', 42)
    assert_unop('!true;', 'not', True)
    assert_unop('1337!;', 'fac', 1337)

def test_more_than_one_operand():
    assert_binop_triade('4 + 2 + 0;', '+', '+', 4, 2, 0)
    assert_binop_triade('true || false || true;', '||', '||', True, False, True)
    assert_binop_triade('true && false && true;', '&&', '&&', True, False, True)
    assert_binop_triade('4 % 2 * 0;', '%', '*', 4, 2, 0)
    assert_binop_triade('4 +/ 2 */ 0;', '+/', '*/', 4, 2, 0)

def test_more_than_one_statement():
    nodes = parse_statements("42 + 3; 1 + 3 + 3 + 7;")
    nodes.show()