package org.opnit.plugin;

import com.intellij.lexer.FlexLexer;
import com.intellij.psi.tree.IElementType;
import com.intellij.psi.TokenType;

%%

%class OpnitLexer
%implements FlexLexer
%unicode
%function advance
%type IElementType
%eof{  return;
%eof}

CRLF=\R
WHITE_SPACE=[\ \n\t\f]
COMMENT=#[^\r\n]*
IDENTIFIER=[a-zA-Z_][a-zA-Z0-9_]*
NUMBER_LITERAL=[0-9]+(\.[0-9]*)?
STRING_LITERAL=\"[^\"]*\"

%%

<YYINITIAL> {
  {WHITE_SPACE}        { return TokenType.WHITE_SPACE; }
  {COMMENT}           { return OpnitTypes.COMMENT; }

  "function"          { return OpnitTypes.FUNCTION; }
  "return"           { return OpnitTypes.RETURN; }
  "true"             { return OpnitTypes.TRUE; }
  "false"            { return OpnitTypes.FALSE; }
  "number"           { return OpnitTypes.NUMBER_TYPE; }
  "string"           { return OpnitTypes.STRING_TYPE; }
  "boolean"          { return OpnitTypes.BOOLEAN_TYPE; }

  "+"                { return OpnitTypes.PLUS; }
  "-"                { return OpnitTypes.MINUS; }
  "*"                { return OpnitTypes.MULTIPLY; }
  "/"                { return OpnitTypes.DIVIDE; }
  "->"               { return OpnitTypes.ARROW; }
  "("                { return OpnitTypes.LPAREN; }
  ")"                { return OpnitTypes.RPAREN; }
  "{"                { return OpnitTypes.LBRACE; }
  "}"                { return OpnitTypes.RBRACE; }
  ":"                { return OpnitTypes.COLON; }
  ";"                { return OpnitTypes.SEMICOLON; }
  ","                { return OpnitTypes.COMMA; }

  {NUMBER_LITERAL}    { return OpnitTypes.NUMBER_LITERAL; }
  {STRING_LITERAL}    { return OpnitTypes.STRING_LITERAL; }
  {IDENTIFIER}        { return OpnitTypes.IDENTIFIER; }

  [^]                { return TokenType.BAD_CHARACTER; }
} 