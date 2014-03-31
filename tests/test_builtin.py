from nose.tools import eq_, nottest

import sys
import random

from StringIO import StringIO

from setlx2py.setlx_builtin import *

def test_implies():
    assert stlx_implies(True,True)   == True
    assert stlx_implies(True,False)  == False
    assert stlx_implies(False,True)  == True
    assert stlx_implies(False,False) == True

def test_equivalent():
    assert stlx_equivalent(True,True)   == True
    assert stlx_equivalent(True,False)  == False
    assert stlx_equivalent(False,True)  == False
    assert stlx_equivalent(False,False) == True

def test_antivalent():
    assert stlx_antivalent(True,True)   == False
    assert stlx_antivalent(True,False)  == True
    assert stlx_antivalent(False,True)  == True
    assert stlx_antivalent(False,False) == False

def test_product():
    assert stlx_product(range(1,5)) == 24
    assert stlx_product([1,5,34,5,6,8]) == (1 * 5 * 34 * 5 * 6 * 8)

def test_arb():
    random.seed(42)
    s = Set([42])

    result = stlx_arb(s)
    eq_(result, 42)
    eq_(s, Set([42]))
    
def test_from():
    s = Set([42])
    s, result = stlx_from(s)

    eq_(result, 42)
    eq_(s, Set([]))    

# Custom/Overloaded set Operations
# ----------

def test_set_operations():
    s1 = Set([1,2])
    s2 = Set([2,3])
    
    eq_(s1 + s2, Set([1,2,3]))
    eq_(s1 - s2, Set([1]))
    eq_(s1 * s2, Set([2]))
    eq_(s1 % s2, Set([1, 3]) )
    eq_(stlx_pow(s1, 2), Set([(1, 1), (1, 2), (2, 1), (2, 2)]))
    eq_(stlx_pow(2, s2), Set([(), (2,), (2,3), (3,)]))
    eq_(stlx_cartesian(s1, s2), Set([(1, 2), (1, 3), (2, 2), (2, 3)]))

# Matching
# ========

def test_matches():
    # case []
    p = Pattern(0, False)
    assert stlx_matches(p , [])
    assert not stlx_matches(p, [1])                

    # case [a,b]
    assert stlx_matches(Pattern(2, False), [1, 2])           

    # case [a,b|c]
    assert stlx_matches(Pattern(2, True), [1, 2])      

    # case [a,b,c]
    p = Pattern(3, False)
    assert not stlx_matches(p, [1, 2])
    assert stlx_matches(p, [1,2,3])
    assert not stlx_matches(p, [1, 2, 3, 4])  

    # case [a,b,c|d]
    p = Pattern(3, True)
    assert stlx_matches(p, [1, 2, 3]) 
    assert not stlx_matches(p, [1, 2])

def test_bind_list_simple():
    # match ([1,2,3]) { case [a,b,c] : .. }
    matchee = SetlxList([1,2,3])
    a, b, c = stlx_bind(Pattern(3, False), matchee)
    eq_(a,1)
    eq_(b,2)
    eq_(c,3)

def test_bind_list_tail():
    # match ([1..5]) { case [a,b|c] : .. }
    matchee = SetlxList([1,2,3,4,5])
    a, b, c = stlx_bind(Pattern(2, True), matchee)
    eq_(a,1)
    eq_(b,2)
    eq_(c,SetlxList([3,4,5]))

def test_bind_string_single():
    # match ("a") { case [a] : .. }
    matchee = SetlxString("a")
    a, = stlx_bind(Pattern(1, False), matchee)
    eq_(a, SetlxString("a"))

def test_bind_string_single_tail():
    # match ("a") { case [a] : .. }
    matchee = SetlxString("a")
    a, b = stlx_bind(Pattern(1, True), matchee)
    eq_(a, SetlxString("a"))
    eq_(b, Bumper())

def test_bind_string_three():
    # match ("abc") { case [a,b,c] : .. }
    matchee = SetlxString("abc")
    a, b, c = stlx_bind(Pattern(3, False), matchee)
    eq_(a, SetlxString("a"))
    eq_(b, SetlxString("b"))
    eq_(c, SetlxString("c"))

def test_bind_string_tail_minimal():
    # match ("ab") { case [a|b] : .. }
    matchee = SetlxString("ab")
    a, b = stlx_bind(Pattern(1, True), matchee)
    eq_(a, SetlxString("a"))
    eq_(b, SetlxString("b"))    

def test_bind_string_tail_longer_string():
    # match ("abcdef") { case [a|b] : .. }
    matchee = SetlxString("abcdef")
    a, b = stlx_bind(Pattern(1, True), matchee)
    eq_(a, SetlxString("a"))
    eq_(b, SetlxString("bcdef"))

def test_print():
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    stlx_print('Foo ', 'Bar ', 'baz')
    result =  mystdout.getvalue()
    sys.stdout = old_stdout
    eq_(result, 'Foo Bar baz\n')