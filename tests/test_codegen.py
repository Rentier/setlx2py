#------------------------------------------------------------------------------
# setlx2py: test_codegen.py
#
# Unit tests for the Codegen class in setlx_codegen.py
# These are very shallow and cover only a small area
# Acceptance tests for code generation is seperate
#
# Copyright (C) 2014, Jan-Christoph Klie
# License: Apache v2
#------------------------------------------------------------------------------

from string import Template

from nose.tools import nottest, eq_

from setlx2py.setlx_builtin import builtin
from setlx2py.setlx_parser import Parser
from setlx2py.setlx_codegen import Codegen

generator = Codegen()
parser = Parser()

##
## Hack redefines
## 

set = frozenset

try:
    xrange(0,2)
    range = xrange
except:
    pass


##
## Helper methods
##

def error_msg(source, compiled=None, e=None):
    msg = 'Could not run stuff:\n'
    
    msg += 'Source:\n' + source + '\n'
    if compiled:
        msg += 'Compiled:\n' + compiled
    if e:
        msg += 'Reason:\n'
        msg += e.__class__.__name__ + '\n'
        msg += e.message + '\n'
    return msg

def run(source, ns={}, verbose=False):
    ns.update(builtin)
    ast = parser.parse(source)
    compiled = generator.visit(ast)
    if verbose:
        print('Source: \n' + source)
        print('Target: \n' + compiled)

    try:
        code = compile(compiled, '<string>', 'exec')
        exec(code, ns)
    except Exception, e:
        msg = error_msg(source, compiled, e=e)
        raise AssertionError(msg)

def assert_res(source, variables, verbose=False):
    ns = {}
    run(source, ns, verbose)
    for key, value in variables.items():
        eq_(ns.get(key, None), value)
                
##
## Tests
##

def test_is_creatable():
    assert generator is not None

def test_identifier():
    ns = {'a' : 42}
    run('a;', ns)

def test_constant_int():
    run('42;')

def test_constant_str():
    assert_res('x := "foo";', {'x' : "foo"}, True)

def test_constant_literal():
    assert_res("x := 'foo';", {'x' : "foo"})
    

## Assignment

def test_assignment_simple():
    assert_res('x := 1;', {'x' : 1})

def test_assignment_augmented():
    assert_res('x := 1; x += 2;', {'x' : 3})
    assert_res('x := 3; x -= 2;', {'x' : 1})
    assert_res('x := 1; x *= 2;', {'x' : 2})
    assert_res('x := 6; x /= 2;', {'x' : 3})
    assert_res('x := 5; x %= 2;', {'x' : 1})

##
## Collections
##

# Syntax sugar for creating

def test_set():
    assert_res('x := {};', {'x' : set([])})
    assert_res('x := {1};', {'x' : set([1])})
    assert_res('x := {1,2};', {'x' : set([1,2])})
    assert_res('x := {1,2,3};', {'x' : set([1,2,3])})
    assert_res('x := {1+3,2-4,3**0};', {'x' : set([4,-2,1])})    

def test_list():
    assert_res('x := [];', {'x' :[]})
    assert_res('x := [1];', {'x' : [1]})
    assert_res('x := [1,2];', {'x' : [1,2]})
    assert_res('x := [1,2,3];', {'x' : [1,2,3]})
    assert_res('x := [1+3,2-4,3**0];', {'x' : [4,-2,1]})

# Range

def test_range_set():
    assert_res('x := {1..16};', {'x' : set(range(1,16+1)) })
    assert_res('x := {1..-1};', {'x' : set([]) })
    assert_res('x := {1,3..10};', {'x' : set([1,3,5,7,9]) })
    assert_res('x := {10,8..1};', {'x' : set([10,8,6,4,2]) })

def test_range_list():
    assert_res('x := [1..16];', {'x' : list(range(1,16+1)) })
    assert_res('x := [1..-1];', {'x' : list([]) })
    assert_res('x := [1,3..10];', {'x' : [1,3,5,7,9] })
    assert_res('x := [10,8..1];', {'x' : [10,8,6,4,2] })

## Binop

def test_binop_simple():
    assert_res('x := 1;', {'x' : 1})

def test_binop_add_three():
    assert_res('x := 1 + 2 + 3;', {'x' : 6})
    
def test_binop_mult_before_add():
    assert_res('x := 4 + 3 * 2;', {'x' : 10})
    assert_res('x := (4 + 3) * 2;', {'x' : 14})

def test_binop_power():
    assert_res('x :=  2 * 3  ** 2;', {'x' : 18})
    assert_res('x := (2 * 3) ** 2;', {'x' : 36})

def test_binop_precedence():
    assert_res('x := 2 +3 * 4;'   , {'x' : 2 + ( 3 * 4)})
    assert_res('x := 10 - 4 - 2;' , {'x' : ( 10 - 4 ) - 2})
    assert_res('x := 12 / 3 + 3;' , {'x' : (12 / 3) + 3})
    assert_res('x := 2 ** 3 + 3;' , {'x' : (2 ** 3) + 3 })
    assert_res('x := 12 / 2 * 3;' , {'x' : (12 / 2) * 3})
    assert_res('x := 12 / 2 / 3;' , {'x' : (12 / 2) / 3})
    assert_res('x := 18 / 3 ** 2;', {'x' : 18 /( 3 **2 )})

def test_binop_comparison():
    assert_res('x := 1 > 2;', {'x' : False})
    assert_res('x := 1 < 2;', {'x' : True})
    assert_res('x := 1 >= 1;', {'x' : True})
    assert_res('x := 1 <= 1;', {'x' : True})
    assert_res('x := 1 == 2;', {'x' : False})
    assert_res('x := 1 != 2;', {'x' : True})

def test_binop_logic_basic():
    assert_res('x := true && false;', {'x' : False})
    assert_res('x := true || false;', {'x' : True})

def test_binop_logic_complex():
    assert_res('x := true => false;',    {'x' : False})
    assert_res('x := false <==> false;', {'x' : True})
    assert_res('x := true <!=> false;',  {'x' : True})

def test_binop_comparison_set():
    assert_res('x := 2 in {1..42};', {'x' : True})

def test_unary_simple():
    assert_res('x := 5!;', {'x' : 120})
    assert_res('x := -5;', {'x' : -5})

##  
## Compund statements
##

# If-No-Else

def test_if_no_else_minimal():
    assert_res('if(true) {}', {})
    
def test_if_no_else_single():
    s = """
    x := 42;
    if(x >= 5) { y := 3; }
    """
    assert_res(s, {'x' : 42, 'y' : 3})

def test_if_no_else_double():
    s = """
    x := 6;
    if(x >= 5 && x != 7) {
        y := "Foo";
        z := "Bar";
    }
    """
    assert_res(s, {'x' : 6, 'y' : "Foo", 'z' : "Bar"})
    
# If-Else

def test_if_else_minimal():
    assert_res('if(true) {} else {}', {})

def test_if_else_single():
    s = """
    i := 23; // Illuminati
    if(i % 2 == 0) {
        parity := "Even";
    } else {
        parity := "Odd";
    }
    """
    assert_res(s, {'parity' : "Odd"})

def test_if_four_else_if_else():
    s = Template("""
    grade := '$grade';
    if(grade == "A") {
        descr := "Excellent";
    } else if(grade == "B") {
        descr := "Good";
    } else if(grade == "C") {
        descr := "Satisfactory";
    } else if(grade == "D") {
        descr := "Pass";
    } else if(grade == "F") {
        descr := "Fail";
    } else {
        descr := "Invalid input";
    }
    """)
    
    permutations = {
        'A' : 'Excellent',
        'B' : 'Good',
        'C' : 'Satisfactory',
        'D' : 'Pass',
        'F' : 'Fail',
        'J' : 'Invalid input',
    }
    
    for grade, descr in permutations.items():
        source = s.substitute(grade=grade)
        assert_res(source, {'grade' : grade, 'descr' : descr})

def test_if_nested_else():
    s = Template("""
    if($num1 == $num2) {
        relation := "Equal";
    } else {
        if($num1 > $num2) { 
            relation := "Num1 greater";
        } else {
            relation := "Num2 greater";
        }
    }
    """)
    
    permutations = [
        (1,1, "Equal"),
        (2,1, "Num1 greater"),
        (1,2, "Num2 greater"),
    ]
    
    for x, y, relation in permutations:
        source = s.substitute(num1=x, num2=y)
        assert_res(source, {'relation' : relation}, True)
    