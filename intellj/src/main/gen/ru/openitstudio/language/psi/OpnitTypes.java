// This is a generated file. Not intended for manual editing.
package ru.openitstudio.language.psi;

import com.intellij.psi.tree.IElementType;
import com.intellij.psi.PsiElement;
import com.intellij.lang.ASTNode;
import ru.openitstudio.language.psi.impl.*;

public interface OpnitTypes {

  IElementType BINARY_EXPR = new OpnitElementType("BINARY_EXPR");
  IElementType CALL_EXPR = new OpnitElementType("CALL_EXPR");
  IElementType EXPR = new OpnitElementType("EXPR");
  IElementType FUNCTION_DEF = new OpnitElementType("FUNCTION_DEF");
  IElementType LITERAL = new OpnitElementType("LITERAL");
  IElementType PARAM = new OpnitElementType("PARAM");
  IElementType PARAM_LIST = new OpnitElementType("PARAM_LIST");
  IElementType REF_EXPR = new OpnitElementType("REF_EXPR");
  IElementType RETURN_STATEMENT = new OpnitElementType("RETURN_STATEMENT");
  IElementType STATEMENT_ = new OpnitElementType("STATEMENT_");
  IElementType TYPE = new OpnitElementType("TYPE");

  IElementType ANY_TYPE = new OpnitTokenType("any");
  IElementType BOOLEAN_TYPE = new OpnitTokenType("boolean");
  IElementType COLON = new OpnitTokenType(":");
  IElementType COMMA = new OpnitTokenType(",");
  IElementType COMMENT = new OpnitTokenType("COMMENT");
  IElementType DIVIDE = new OpnitTokenType("/");
  IElementType FALSE = new OpnitTokenType("false");
  IElementType FUNCTION = new OpnitTokenType("function");
  IElementType IDENTIFIER = new OpnitTokenType("IDENTIFIER");
  IElementType LBRACE = new OpnitTokenType("{");
  IElementType LPAREN = new OpnitTokenType("(");
  IElementType MINUS = new OpnitTokenType("-");
  IElementType MULTIPLY = new OpnitTokenType("*");
  IElementType NUMBER_LITERAL = new OpnitTokenType("NUMBER_LITERAL");
  IElementType NUMBER_TYPE = new OpnitTokenType("number");
  IElementType PLUS = new OpnitTokenType("+");
  IElementType RBRACE = new OpnitTokenType("}");
  IElementType RETURN = new OpnitTokenType("return");
  IElementType RPAREN = new OpnitTokenType(")");
  IElementType SEMICOLON = new OpnitTokenType(";");
  IElementType STRING_LITERAL = new OpnitTokenType("STRING_LITERAL");
  IElementType STRING_TYPE = new OpnitTokenType("string");
  IElementType TRUE = new OpnitTokenType("true");

  class Factory {
    public static PsiElement createElement(ASTNode node) {
      IElementType type = node.getElementType();
      if (type == BINARY_EXPR) {
        return new OpnitBinaryExprImpl(node);
      }
      else if (type == CALL_EXPR) {
        return new OpnitCallExprImpl(node);
      }
      else if (type == EXPR) {
        return new OpnitExprImpl(node);
      }
      else if (type == FUNCTION_DEF) {
        return new OpnitFunctionDefImpl(node);
      }
      else if (type == LITERAL) {
        return new OpnitLiteralImpl(node);
      }
      else if (type == PARAM) {
        return new OpnitParamImpl(node);
      }
      else if (type == PARAM_LIST) {
        return new OpnitParamListImpl(node);
      }
      else if (type == REF_EXPR) {
        return new OpnitRefExprImpl(node);
      }
      else if (type == RETURN_STATEMENT) {
        return new OpnitReturnStatementImpl(node);
      }
      else if (type == STATEMENT_) {
        return new OpnitStatement_Impl(node);
      }
      else if (type == TYPE) {
        return new OpnitTypeImpl(node);
      }
      throw new AssertionError("Unknown element type: " + type);
    }
  }
}
