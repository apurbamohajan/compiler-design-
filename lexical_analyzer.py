import re

keywords = {
    "if", "else", "switch", "case", "for", "while", "do",
    "break", "continue", "return",
    "int", "float", "double", "char", "class", "struct",
    "enum", "typedef", "using",
    "public", "private", "protected", "static", "const",
    "volatile", "mutable",
    "async", "await", "throw", "try", "catch", "finally",
    "import", "export", "module", "include", "require",
    "true", "false"
}

with open("input.txt", "r") as f:
    text = f.read()

library_pattern = r'#include\s*[<"]([\w./]+)[>"]'
comment_single = r'//[^\n]*'
comment_multi = r'/\*[\s\S]*?\*/'
string_pattern = r'"[^"]*"'
float_pattern = r'\d+\.\d+([eE][+-]?\d+)?'
integer_pattern = r'\d+'
logical_op = r'&&|\|\||!'
assign_op = r'\+=|-=|\*=|/=|%=|='
rel_op = r'==|!=|<=|>=|<|>'
arith_op = r'\+\+|--|\+|-|\*|/|%'
identifier_pattern = r'[a-zA-Z_][a-zA-Z0-9_]*'
symbol_pattern = r'[(){}\[\];,:]'

tokens = []
line_num = 1
i = 0

while i < len(text):
    if text[i] in ' \t':
        i += 1
        continue
    
    if text[i] == '\n':
        line_num += 1
        i += 1
        continue
    
    match = re.match(library_pattern, text[i:])
    if match:
        lib_name = match.group(1)
        tokens.append(("Library File", lib_name, line_num))
        i += match.end()
        continue
    
    match = re.match(comment_single, text[i:])
    if match:
        tokens.append(("Comment", match.group(), line_num))
        i += match.end()
        continue
    
    match = re.match(comment_multi, text[i:])
    if match:
        comment_text = match.group()
        tokens.append(("Comment", comment_text, line_num))
        line_num += comment_text.count('\n')
        i += match.end()
        continue
    
    match = re.match(float_pattern, text[i:])
    if match:
        tokens.append(("Number", match.group(), line_num))
        i += match.end()
        continue
    
    match = re.match(integer_pattern, text[i:])
    if match:
        tokens.append(("Number", match.group(), line_num))
        i += match.end()
        continue
    
    match = re.match(logical_op, text[i:])
    if match:
        tokens.append(("Logical Operator", match.group(), line_num))
        i += match.end()
        continue
    
    match = re.match(assign_op, text[i:])
    if match:
        tokens.append(("Assignment Operator", match.group(), line_num))
        i += match.end()
        continue
    
    match = re.match(rel_op, text[i:])
    if match:
        tokens.append(("Relational Operator", match.group(), line_num))
        i += match.end()
        continue
    
    match = re.match(arith_op, text[i:])
    if match:
        tokens.append(("Arithmetic Operator", match.group(), line_num))
        i += match.end()
        continue
    
    match = re.match(identifier_pattern, text[i:])
    if match:
        name = match.group()
        i += match.end()
        
        if name in keywords:
            tokens.append(("Keyword", name, line_num))
            continue
        
        rest = text[i:]
        space_match = re.match(r'[ \t]*', rest)
        if space_match:
            after_space = i + space_match.end()
            if after_space < len(text) and text[after_space] == '(':
                paren_start = after_space
                paren_count = 1
                j = paren_start + 1
                while j < len(text) and paren_count > 0:
                    if text[j] == '(':
                        paren_count += 1
                    elif text[j] == ')':
                        paren_count -= 1
                    j += 1
                
                func_call = name + " " + text[paren_start:j]
                tokens.append(("Function", func_call, line_num))
                i = j
                continue
        
        tokens.append(("Identifier", name, line_num))
        continue
    
    match = re.match(string_pattern, text[i:])
    if match:
        tokens.append(("String Literal", match.group(), line_num))
        i += match.end()
        continue
    
    match = re.match(symbol_pattern, text[i:])
    if match:
        tokens.append(("Symbol", match.group(), line_num))
        i += match.end()
        continue
    
    i += 1

with open("output.txt", "w") as f:
    for token_type, value, line in tokens:
        f.write(f"{token_type}: {value} (line:{line})\n")

print("Lexical analysis complete. Check output.txt")
