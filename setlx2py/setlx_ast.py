#-----------------------------------------------------------------
# ** ATTENTION **
# This code was automatically generated from the file:
# setlx2py/setlx_ast.cfg
#
# Do not modify it directly. Modify the configuration file and
# run the generator again.
# ** ** *** ** **
#
# AST Node classes.
#
# Copyright (C) 2008-2013, Eli Bendersky
#               2013,      Jan-Christoph Klie 
# License: BSD
#-----------------------------------------------------------------


import sys


class Node(object):
    """ Abstract base class for AST nodes.
    """
    def children(self):
        """ A sequence of all children that are Nodes
        """
        pass

    def __str__(self):
        return self.show()

    def __repr__(self):
        return str(self.to_tuples())

    def to_tuples(self):
        result = [self.__class__.__name__]

        attr_list = [getattr(self, n) for n in self.attr_names]
        result.extend(attr_list)

        for (child_name, child) in self.children():
            result.append( child.to_tuples() )
        return tuple(result)

    def show(self,
             buf=None,
             offset=0,
             attrnames=False,
             nodenames=False,
             showcoord=False,
             _my_node_name=None):
        """ Pretty print the Node and all its attributes and
            children (recursively) to a buffer.

            buf:
                Open IO buffer into which the Node is printed.
                If it is None or let empty, instead a string
                is returned

            offset:
                Initial offset (amount of leading spaces)

            attrnames:
                True if you want to see the attribute names in
                name=value pairs. False to only see the values.

            nodenames:
                True if you want to see the actual node names
                within their parents.

            showcoord:
                Do you want the coordinates of each Node to be
                displayed.
        """
        s = ''
        lead = ' ' * offset
        if nodenames and _my_node_name is not None:
            s += lead + self.__class__.__name__+ ' <' + _my_node_name + '>: '
        else:
            s += lead + self.__class__.__name__+ ': '

        if self.attr_names:
            if attrnames:
                nvlist = [(n, getattr(self,n)) for n in self.attr_names]
                attrstr = ', '.join('%s=%s' % nv for nv in nvlist)
            else:
                vlist = [getattr(self, n) for n in self.attr_names]
                attrstr = ', '.join('%s' % v for v in vlist)
            s += attrstr

        if showcoord: s += ' (at %s)' % self.coord
        s += '\n'

        for (child_name, child) in self.children():
            s += child.show(
                buf,
                offset=offset + 2,
                attrnames=attrnames,
                nodenames=nodenames,
                showcoord=showcoord,
                _my_node_name=child_name)

        if buf is None: return s
        else: buf.write(s)

class NodeVisitor(object):
    """ A base NodeVisitor class for visiting c_ast nodes.
        Subclass it and define your own visit_XXX methods, where
        XXX is the class name you want to visit with these
        methods.

        For example:

        class ConstantVisitor(NodeVisitor):
            def __init__(self):
                self.values = []

            def visit_Constant(self, node):
                self.values.append(node.value)

        Creates a list of values of all the constant nodes
        encountered below the given node. To use it:

        cv = ConstantVisitor()
        cv.visit(node)

        Notes:

        *   generic_visit() will be called for AST nodes for which
            no visit_XXX method was defined.
        *   The children of nodes for which a visit_XXX was
            defined will not be visited - if you need this, call
            generic_visit() on the node.
            You can use:
                NodeVisitor.generic_visit(self, node)
        *   Modeled after Python's own AST visiting facilities
            (the ast module of Python 3.0)
    """
    def visit(self, node):
        """ Visit a node.
        """
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """ Called if no explicit visitor function exists for a
            node. Implements preorder visiting of the node.
        """
        for c_name, c in node.children():
            self.visit(c)


class ArrayRef(Node):
    def __init__(self, obj, subscript, coord=None):
        self.obj = obj
        self.subscript = subscript
        self.coord = coord

    def children(self):
        nodelist = []
        if self.obj is not None: nodelist.append(("obj", self.obj))
        if self.subscript is not None: nodelist.append(("subscript", self.subscript))
        return tuple(nodelist)

    attr_names = ()

class Assert(Node):
    def __init__(self, cond, expr, coord=None):
        self.cond = cond
        self.expr = expr
        self.coord = coord

    def children(self):
        nodelist = []
        if self.cond is not None: nodelist.append(("cond", self.cond))
        if self.expr is not None: nodelist.append(("expr", self.expr))
        return tuple(nodelist)

    attr_names = ()

class Assignment(Node):
    def __init__(self, op, left, right, coord=None):
        self.op = op
        self.left = left
        self.right = right
        self.coord = coord

    def children(self):
        nodelist = []
        if self.left is not None: nodelist.append(("left", self.left))
        if self.right is not None: nodelist.append(("right", self.right))
        return tuple(nodelist)

    attr_names = ('op',)

class AssignmentList(Node):
    def __init__(self, assignments, coord=None):
        self.assignments = assignments
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.assignments or []):
            nodelist.append(("assignments[%d]" % i, child))
        return tuple(nodelist)

    attr_names = ()

class BinaryOp(Node):
    def __init__(self, op, left, right, coord=None):
        self.op = op
        self.left = left
        self.right = right
        self.coord = coord

    def children(self):
        nodelist = []
        if self.left is not None: nodelist.append(("left", self.left))
        if self.right is not None: nodelist.append(("right", self.right))
        return tuple(nodelist)

    attr_names = ('op',)

class Backtrack(Node):
    def __init__(self, coord=None):
        self.coord = coord

    def children(self):
        return ()

    attr_names = ()

class Block(Node):
    def __init__(self, stmts, coord=None):
        self.stmts = stmts
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.stmts or []):
            nodelist.append(("stmts[%d]" % i, child))
        return tuple(nodelist)

    attr_names = ()

class Break(Node):
    def __init__(self, coord=None):
        self.coord = coord

    def children(self):
        return ()

    attr_names = ()

class Continue(Node):
    def __init__(self, coord=None):
        self.coord = coord

    def children(self):
        return ()

    attr_names = ()

class Constant(Node):
    def __init__(self, type, value, coord=None):
        self.type = type
        self.value = value
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = ('type','value',)

class Exit(Node):
    def __init__(self, coord=None):
        self.coord = coord

    def children(self):
        return ()

    attr_names = ()

class ExprList(Node):
    def __init__(self, exprs, coord=None):
        self.exprs = exprs
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.exprs or []):
            nodelist.append(("exprs[%d]" % i, child))
        return tuple(nodelist)

    attr_names = ()

class FileAST(Node):
    def __init__(self, stmts, coord=None):
        self.stmts = stmts
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.stmts or []):
            nodelist.append(("stmts[%d]" % i, child))
        return tuple(nodelist)

    attr_names = ()

class If(Node):
    def __init__(self, cond, iftrue, iffalse, coord=None):
        self.cond = cond
        self.iftrue = iftrue
        self.iffalse = iffalse
        self.coord = coord

    def children(self):
        nodelist = []
        if self.cond is not None: nodelist.append(("cond", self.cond))
        if self.iftrue is not None: nodelist.append(("iftrue", self.iftrue))
        if self.iffalse is not None: nodelist.append(("iffalse", self.iffalse))
        return tuple(nodelist)

    attr_names = ()

class Iterator(Node):
    def __init__(self, assignable, expression, coord=None):
        self.assignable = assignable
        self.expression = expression
        self.coord = coord

    def children(self):
        nodelist = []
        if self.assignable is not None: nodelist.append(("assignable", self.assignable))
        if self.expression is not None: nodelist.append(("expression", self.expression))
        return tuple(nodelist)

    attr_names = ()

class IteratorChain(Node):
    def __init__(self, iterators, coord=None):
        self.iterators = iterators
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.iterators or []):
            nodelist.append(("iterators[%d]" % i, child))
        return tuple(nodelist)

    attr_names = ()

class MemberAccess(Node):
    def __init__(self, obj, field, coord=None):
        self.obj = obj
        self.field = field
        self.coord = coord

    def children(self):
        nodelist = []
        if self.obj is not None: nodelist.append(("obj", self.obj))
        if self.field is not None: nodelist.append(("field", self.field))
        return tuple(nodelist)

    attr_names = ()

class Quantor(Node):
    def __init__(self, name, lhs, cond, coord=None):
        self.name = name
        self.lhs = lhs
        self.cond = cond
        self.coord = coord

    def children(self):
        nodelist = []
        if self.lhs is not None: nodelist.append(("lhs", self.lhs))
        if self.cond is not None: nodelist.append(("cond", self.cond))
        return tuple(nodelist)

    attr_names = ('name',)

class Return (Node):
    def __init__(self, expr, coord=None):
        self.expr = expr
        self.coord = coord

    def children(self):
        nodelist = []
        if self.expr is not None: nodelist.append(("expr", self.expr))
        return tuple(nodelist)

    attr_names = ()

class Term(Node):
    def __init__(self, name, args, coord=None):
        self.name = name
        self.args = args
        self.coord = coord

    def children(self):
        nodelist = []
        if self.args is not None: nodelist.append(("args", self.args))
        return tuple(nodelist)

    attr_names = ('name',)

class UnaryOp(Node):
    def __init__(self, op, expr, coord=None):
        self.op = op
        self.expr = expr
        self.coord = coord

    def children(self):
        nodelist = []
        if self.expr is not None: nodelist.append(("expr", self.expr))
        return tuple(nodelist)

    attr_names = ('op',)

class Variable(Node):
    def __init__(self, name, coord=None):
        self.name = name
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = ('name',)

class While(Node):
    def __init__(self, cond, body, coord=None):
        self.cond = cond
        self.body = body
        self.coord = coord

    def children(self):
        nodelist = []
        if self.cond is not None: nodelist.append(("cond", self.cond))
        if self.body is not None: nodelist.append(("body", self.body))
        return tuple(nodelist)

    attr_names = ()

