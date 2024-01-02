%token NUM
%token ID
%start program
%%
program: declaration_list
;
declaration_list: declaration_list declaration
| declaration
;
declaration: var_declaration 
| fun_declaration 
;
var_declaration: type_specifier ID ';' 
| type_specifier ID '[' NUM ']' ';'
;
type_specifier: "int" 
| "void"
;
fun_declaration: type_specifier ID '(' params ')' compound_stmt
;
params: param_list
| "void"
;
param_list: param_list ',' param
| param
;
param: type_specifier ID
| type_specifier ID '[' ']'
;
compound_stmt: '{' local_declarations statement_list '}'
;
local_declarations: local_declarations var_declaration
| /* epsilon */
;
statement_list: statement_list statement
| /* epsilon */
;
statement: expression_stmt
| compound_stmt
| selection_stmt
| iteration_stmt
| return_stmt
| switch_stmt
;
expression_stmt: expression ';'
| "break" ';'
| ';'
;
selection_stmt: "if" '(' expression ')' statement "endif"
| "if" '(' expression ')' statement "else" statement "endif"
;
iteration_stmt: "while" '(' expression ')' statement
;
return_stmt: "return" ';'
| "return" expression ';'
;
switch_stmt: "switch" '(' expression ')' '{' case_stmts default_stmt '}'
;
case_stmts: case_stmts case_stmt
| /* epsilon */
;
case_stmt: "case" NUM ':' statement_list
;
default_stmt: "default" ':' statement_list
| /* epsilon */
;
expression: var '=' expression
| simple_expression
;
var: ID
| ID '[' expression ']'
;
simple_expression: additive_expression relop additive_expression
| additive_expression
;
relop: '<'
| "=="
;
additive_expression: additive_expression addop term
| term
;
addop: '+'
| '-'
;
term: term mulop factor
| factor
;
mulop: '*'
| '/'
;
factor: '(' expression ')'
| var
| call
| NUM
;
call: ID '(' args ')'
;
args: arg_list
| /* epsilon */
;
arg_list: arg_list ',' expression
| expression
;
%%
