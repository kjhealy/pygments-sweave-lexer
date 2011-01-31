# -*- coding: utf-8 -*-
"""
    An Sweave lexer for Pygments
    ~~~~~~~~~~~~~~~~~~~~
    
    The math.py file in Pygments 1.4 can be patched with
    add_sweave_lexer.patch to add an sweave lexer. Once
    you've patched the file (in, e.g.,
    Pygments-1.4-py2.6.egg/pygments/lexers/math.py),
    you must run 
    > sudo python _mapping.py
    from inside the lexers directory to register the new
    lexer.

    This file is just for reference. (Or, if you don't want
    patch the file, just add the code below in the proper
    places in math.py and run _mapping.py.)

    
"""

### Add at header
from pygments.lexer import DelegatingLexer
from pygments.lexers.text import TexLexer

### Add to __all__ statement
__all__ = ['RnwLexer',' SweaveLexer']

### Add to the end of the file

## RnwLexer (can't use SLexer because of its handling of quotes)
class RnwLexer(RegexLexer):
    """
    For S, S-plus, and R source code in Sweave documents.

    *Kieran Healy*
    """

    name = 'Rnw'
    aliases = ['rnw']
    filenames = ['*.r']
    mimetypes = ['text/S-plus', 'text/S', 'text/R']

    tokens = {
        's-header': [
            (r'(<<.*?>>=)', Keyword.Reserved), 
        ],
        's-closer': [
            (r'(^@)', Keyword.Reserved),
        ],
        'comments': [
            (r'#.*$', Comment.Single),
        ],
        'valid_name': [
            (r'[a-zA-Z][0-9a-zA-Z\._]+', Text),
            (r'`.+`', String.Backtick),
        ],
        'punctuation': [
            (r'\[|\]|\[\[|\]\]|\$|\(|\)|@|:::?|;|,', Punctuation),
        ],
        'keywords': [
            (r'for(?=\s*\()|while(?=\s*\()|if(?=\s*\()|(?<=\s)else|'
             r'(?<=\s)break(?=;|$)|return(?=\s*\()|function(?=\s*\()',
             Keyword.Reserved)
        ],
        'operators': [
            (r'<-|-|==|<=|>=|<|>|&&|&|!=|\|\|?', Operator),
            (r'\*|\+|\^|/|%%|%/%|=', Operator),
            (r'%in%|%*%', Operator)
        ],
        'builtin_symbols': [
            (r'(NULL|NA|TRUE|FALSE|NaN)\b', Keyword.Constant),
            (r'(T|F)\b', Keyword.Variable),
        ],
        'numbers': [
            (r'(?<![0-9a-zA-Z\)\}\]`\"])(?=\s*)[-\+]?[0-9]+'
             r'(\.[0-9]*)?(E[0-9][-\+]?(\.[0-9]*)?)?', Number),
            (r'\.[0-9]*(E[0-9][-\+]?(\.[0-9]*)?)?', Number),
        ],
        'statements': [
            include('s-header'),
            include('s-closer'),
            include('comments'),
            # whitespaces
            (r'\s+', Text),
            # (r'\'', String, 'string_squote'),
            # (r'\"', String, 'string_dquote'),
            include('builtin_symbols'),
            include('numbers'),
            include('keywords'),
            include('punctuation'),
            include('operators'),
            include('valid_name'),
        ],

        'root': [
            include('statements'),
            # blocks:
            (r'\{|\}', Punctuation),
            (r'.', Text),
        ],
    }

    def analyse_text(text):
        return '<-' in text       

## Sweave
class SweaveLexer(DelegatingLexer):
    """
    Lexer for Sweave documents (S/R code and LaTeX).
    """

    name = 'Sweave'
    aliases = ['sweave']
    filenames = ['*.Snw', '*.Rnw', '*.snw', '*.rnw']
    mimetypes = ['text/x-sweave']
    
    def __init__(self, **options):
        super(SweaveLexer, self).__init__(RnwLexer, TexLexer, Text, **options)
