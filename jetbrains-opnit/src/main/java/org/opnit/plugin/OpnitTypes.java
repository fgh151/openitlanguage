package org.opnit.plugin;

import com.intellij.psi.tree.IElementType;

public interface OpnitTypes {
    IElementType FUNCTION = new OpnitTokenType("FUNCTION");
    IElementType RETURN = new OpnitTokenType("RETURN");
    IElementType TRUE = new OpnitTokenType("TRUE");
    IElementType FALSE = new OpnitTokenType("FALSE");
    IElementType NUMBER_TYPE = new OpnitTokenType("NUMBER_TYPE");
    IElementType STRING_TYPE = new OpnitTokenType("STRING_TYPE");
    IElementType BOOLEAN_TYPE = new OpnitTokenType("BOOLEAN_TYPE");

    IElementType PLUS = new OpnitTokenType("PLUS");
    IElementType MINUS = new OpnitTokenType("MINUS");
    IElementType MULTIPLY = new OpnitTokenType("MULTIPLY");
    IElementType DIVIDE = new OpnitTokenType("DIVIDE");
    IElementType ARROW = new OpnitTokenType("ARROW");
    IElementType LPAREN = new OpnitTokenType("LPAREN");
    IElementType RPAREN = new OpnitTokenType("RPAREN");
    IElementType LBRACE = new OpnitTokenType("LBRACE");
    IElementType RBRACE = new OpnitTokenType("RBRACE");
    IElementType COLON = new OpnitTokenType("COLON");
    IElementType SEMICOLON = new OpnitTokenType("SEMICOLON");
    IElementType COMMA = new OpnitTokenType("COMMA");

    IElementType COMMENT = new OpnitTokenType("COMMENT");
    IElementType IDENTIFIER = new OpnitTokenType("IDENTIFIER");
    IElementType NUMBER_LITERAL = new OpnitTokenType("NUMBER_LITERAL");
    IElementType STRING_LITERAL = new OpnitTokenType("STRING_LITERAL");
} 