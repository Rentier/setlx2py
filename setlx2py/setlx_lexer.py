#------------------------------------------------------------------------------
# setlx2py: setlx_lexer.py
#
# Lexer class: lexer for the setlx language
#
# Copyright (C) 2013, Jan-Christoph Klie
# License: Apache v2
#------------------------------------------------------------------------------

from ply import lex
from ply.lex import TOKEN

import re

class SetlxSyntaxError (Exception):
    def __init__(self, msg, LEXER, src, lineno=None, lexpos=None):
        if lineno is None:
            lineno = LEXER.lexer.lineno
        if lexpos is None:
            lexpos = LEXER.lexer.lexpos
        msg += " at %d column %d: %r" % (
            lineno, lexpos - LEXER.line_head_pos, src)
        Exception.__init__(self, msg)

class Lexer():

    def __init__(self):
        pass

    def build(self, **kwargs):
        """ Builds the lexer from the specification. Must be
            called after the lexer object is created.

            This method exists separately, because the PLY
            manual warns against calling lex.lex inside
            __init__
        """
        self.lexer = lex.lex(object=self, **kwargs)
        self.reset()

    def input(self, text):
        """ Sets the input for the lexer
        """
        self.lexer.input(text)  
    
    def token(self):
        self.last_token = self.lexer.token()
        return self.last_token

    def reset(self):
        self.lexer.lineno = 1

    ##
    ## Lexer configuration
    ##

    # Whitespace skipped
    t_ignore = ' \t\r\f\v'

    # Ignore comments
    t_ignore_comment = r'(/\*(.|\n)*?\*/)|(//.*)'      

    def t_newline(self, t):
        r'\n'
        t.lexer.lineno += 1
        self.line_head_pos = t.lexpos + 1

    def t_error(self, t):
        raise SetlxSyntaxError("Bad character: ", self, t.value[0])

    ##
    ## Regexes for use in tokens
    ##

    # An identifier must start with a lower case letter
    # and may contain numbers, letters and underscores   
    identifier = r'[a-z][a-zA-Z_0-9]*'
    term = r'[\^A-Z]' + '[a-zA-Z_0-9]*'

    # character sequences

    string = r'"([^\\"]|(\\.))*"'
    literal = r"'([^\\']|(\\.))*'"    
    interpolation = re.compile('"[^"]*(\$[^\$\"]+?\$)[^"]*?"')
    
    # integer constants    
    integer_constant = '0|([1-9][0-9]*)'

    # floating constants
    exponent_part = r"""([eE][-+]?[0-9]+)"""
    fractional_constant = r"""([0-9]*\.(?!\.)[0-9]+)|([0-9]+\.(?!\.))"""
    double_constant = '(((('+ fractional_constant + ')'+ \
                        exponent_part + '?)|([0-9]+'+ \
                        exponent_part + '))[FfLl]?)'

    ##
    ## List of tokens recognized by the lexer
    ##
 
    keywords = {
        'true'            : 'TRUE',
        'false'           : 'FALSE',
        'in'              : 'IN',
        'notin'           : 'NOTIN',
        'forall'          : 'FORALL',
        'exists'          : 'EXISTS',
        'backtrack'       : 'BACKTRACK',
        'check'           : 'CHECK',
        'match'           : 'MATCH',
        'regex'           : 'REGEX',
        'as'              : 'AS',
        'break'           : 'BREAK',
        'continue'        : 'CONTINUE',
        'exit'            : 'EXIT',
        'return'          : 'RETURN',
        'assert'          : 'ASSERT',
        'if'              : 'IF',
        'else'            : 'ELSE',
        'switch'          : 'SWITCH',
        'case'            : 'CASE',
        'default'         : 'DEFAULT',
        'for'             : 'FOR',
        'do'              : 'DO',
        'while'           : 'WHILE',
        'procedure'       : 'PROCEDURE',
        'cachedProcedure' : 'CPROCEDURE',
        'class'           : 'CLASS',
        'static'          : 'STATIC',
        'scan'            : 'SCAN',
        'using'           : 'USING',
        'try'             : 'TRY',
        'catch'           : 'CATCH',
        'catchUsr'        : 'CATCH_USR',
        'catchLng'        : 'CATCH_LNG',
    }
    
    tokens = [
        # Identifiers
        'IDENTIFIER',
        'TERM',

        # Unused placeholder
        'UNUSED',
        
        # Number constants
        'INTEGER', 'DOUBLE',

        # Character Sequences
        'STRING', 'LITERAL', 'INTERPOLATION',
            
        # Operators
        'PLUS', 'MINUS',
        'TIMES', 'DIVIDE', 'IDIVIDE', 'MOD', 'CARTESIAN', 'POW',
        'EQUIVALENT', 'ANTIVALENT', 'IMPLICATES',
        'OR', 'AND',
        'EQ', 'NEQ',
        'LT', 'LE', 'GT', 'GE',
        'SUM', 'PRODUCT', 'BANG', 
        'HASH', 'AT',

        # Delimiter
        'SEMICOLON', 'COMMA', 'COLON', 'DOT', 'RANGE',
        'LPAREN', 'RPAREN',             # ()
        'LBRACKET', 'RBRACKET',         # []
        'LBRACE', 'RBRACE',             # {}
        'PIPE',

        # Assign
        'ASSIGN',
        'PLUS_EQUAL', 'MINUS_EQUAL',
        'TIMES_EQUAL', 'MOD_EQUAL',
        'DIVIDE_EQUAL', 'IDIVIDE_EQUAL',
        'LAMBDADEF',

    ] + list(keywords.values())

    ##
    ## Rules for the normal state
    ##

    # Operators

    t_PLUS          = r'\+'
    t_MINUS         = r'\-'
    
    t_DIVIDE        = r'/'
    t_TIMES         = r'\*'
    t_IDIVIDE       = r'\\'
    t_MOD           = r'%'
    t_CARTESIAN     = r'><'
    t_POW           = r'\*\*'
    t_HASH          = r'\#'
    t_AT            = r'@'

    t_EQUIVALENT    = r'<==>'
    t_ANTIVALENT    = r'<!=>'
    t_IMPLICATES    = r'=>'

    t_OR            = r'\|\|'
    t_AND           = r'&&'

    t_EQ            = r'=='
    t_NEQ           = r'!='
    t_LT            = r'<'
    t_LE            = r'<='
    t_GT            = r'>'
    t_GE            = r'>='
    t_BANG          = r'!'
    t_SUM           = r'\+/'
    t_PRODUCT       = r'\*/'
    
    # Delimiter

    t_SEMICOLON     = r';'
    t_COMMA         = r','
    t_COLON         = r':'
    t_RANGE         = r'\.\.'
    t_DOT           = r'\.'
    t_PIPE          = r'\|'
    t_LPAREN        = r'\('
    t_RPAREN        = r'\)'
    t_LBRACKET      = r'\['
    t_RBRACKET      = r'\]'
    t_LBRACE        = r'{'
    t_RBRACE        = r'}'

    # Assign

    t_ASSIGN        = r':='
    t_PLUS_EQUAL    = r'\+='
    t_MINUS_EQUAL   = r'\-='
    t_TIMES_EQUAL   = r'\*='
    t_DIVIDE_EQUAL  = r'/='
    t_IDIVIDE_EQUAL = r'\\='
    t_MOD_EQUAL     = r'%='
    t_LAMBDADEF     = r'\|->'

    # Unused
    t_UNUSED        = r'_'
    
    @TOKEN(identifier)
    def t_IDENTIFIER(self, t):
        t.type = self.keywords.get(t.value, 'IDENTIFIER')
        return t

    @TOKEN(term)
    def t_TERM(self, t):
        return t
    
    @TOKEN(double_constant)
    def t_DOUBLE(self, t):
        return t

    @TOKEN(integer_constant)
    def t_INTEGER(self, t):
        return t        

    @TOKEN(string)
    def t_STRING(self, t):
        if re.match(self.interpolation, t.value):
            t.type = 'INTERPOLATION'
        
        t.value = self.escape(t.value)
        return t

    @TOKEN(literal)
    def t_LITERAL(self, t):
        t.value = self.escape(t.value)
        return t

    def escape(self, string):
        escaped = False
        s = string[1:-1]
        new_str = ""
        for i, c  in enumerate(s):
            if escaped:
                if c == "n":
                    c = "\n"
                elif c == "t":
                    c = "\t"
                new_str += c
                escaped = True
            else:
                if c == r"\\":
                    escaped = True
                else:
                    new_str += c
        return new_str