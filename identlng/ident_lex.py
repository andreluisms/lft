import ply.lex as lex

def space_counter(token):
    spaces = 0
    for c in token.value:
        if c == ' ':
            spaces += 1
        elif c == '\t':
            spaces += 8 - (spaces % 8)
    return spaces

tokens = ['LINHA', 'IDENT', 'DEDENT']
stack = [0]
states = (('idstate', 'exclusive'),
          ('dedstate', 'exclusive'),)
t_LINHA = '[a-zA-Z][a-zA-Z \t]+'

def t_breakline(t):
    r'\n+'                 #reconhece uma ou mais quebras de linha
    t.lexer.lineno += len(t.value) 
    t.lexer.begin('idstate')

def t_idstate_blankline(t):
    r'([ \t]+)\n'         #reconhece uma linha em branco
    # print('t_idstate_blankline')
    pass

def t_idstate_linewithcode(t):
    '([ \t]+) | ([a-zA-Z])'               #reconhece brancos e tabulacoes ou uma letra
    # print('t_idstate_linewithcode')
    n_spaces = space_counter(t)
    t.lexer.begin('INITIAL')
    if n_spaces < stack[-1]:
        t.lexer.skip(-len(t.value))
        stack.pop()
        t.type='DEDENT'
        t.lexer.begin('dedstate')
        return t
    elif n_spaces > stack[-1]:
        stack.append(n_spaces)
        t.type='IDENT'
        return t
    elif n_spaces == 0:
        t.lexer.skip(-1)

def t_dedstate_linewithdedent(t):
    '([ \t]+) | ([a-zA-Z])'       #reconhece brancos e tabulacoes ou uma letra
    n_spaces = space_counter(t)
    if n_spaces < stack[-1]:
        t.lexer.skip(-len(t.value))
        stack.pop()
        t.type='DEDENT'
        return t
    elif n_spaces >= stack[-1]:  
        t.lexer.begin('INITIAL')
        if n_spaces > stack[-1]:
            print('Erro de dedentação --->', n_spaces)
        elif n_spaces == 0:    # Caso elemento reconhecido comece por letra
            t.lexer.skip(-1)

def t_error(t):
    print("Erro no estado INITIAL")
    print(t.value)
    t.lexer.skip(1)

def t_idstate_error(t):
    print("Erro no estado idstate")
    t.lexer.skip(1)

def t_dedstate_error(t):
    print("Erro no estado dedstate")
    t.lexer.skip(1)


lex.lex()
programa = """cleardef perm
    if len lsurf   
                
       return lalala land
r sapore torf
    for i in range len l  
             s  lili lost
             p perm
             for x in pix
                append tipo tor
    return r
"""
lex.input(programa)


for token in lex.lexer:
    print('[', token.type, ',', token.value, ']->', stack)