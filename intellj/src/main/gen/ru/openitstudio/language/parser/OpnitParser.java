// This is a generated file. Not intended for manual editing.
package ru.openitstudio.language.parser;

import com.intellij.lang.PsiBuilder;
import com.intellij.lang.PsiBuilder.Marker;
import static ru.openitstudio.language.psi.OpnitTypes.*;
import static com.intellij.lang.parser.GeneratedParserUtilBase.*;
import com.intellij.psi.tree.IElementType;
import com.intellij.lang.ASTNode;
import com.intellij.psi.tree.TokenSet;
import com.intellij.lang.PsiParser;
import com.intellij.lang.LightPsiParser;

@SuppressWarnings({"SimplifiableIfStatement", "UnusedAssignment"})
public class OpnitParser implements PsiParser, LightPsiParser {

  public ASTNode parse(IElementType root_, PsiBuilder builder_) {
    parseLight(root_, builder_);
    return builder_.getTreeBuilt();
  }

  public void parseLight(IElementType root_, PsiBuilder builder_) {
    boolean result_;
    builder_ = adapt_builder_(root_, builder_, this, null);
    Marker marker_ = enter_section_(builder_, 0, _COLLAPSE_, null);
    result_ = parse_root_(root_, builder_);
    exit_section_(builder_, 0, marker_, root_, result_, true, TRUE_CONDITION);
  }

  protected boolean parse_root_(IElementType root_, PsiBuilder builder_) {
    return parse_root_(root_, builder_, 0);
  }

  static boolean parse_root_(IElementType root_, PsiBuilder builder_, int level_) {
    return root(builder_, level_ + 1);
  }

  /* ********************************************************** */
  // ref_expr LBRACKET expr RBRACKET
  public static boolean array_access(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "array_access")) return false;
    if (!nextTokenIs(builder_, IDENTIFIER)) return false;
    boolean result_;
    Marker marker_ = enter_section_(builder_);
    result_ = ref_expr(builder_, level_ + 1);
    result_ = result_ && consumeToken(builder_, LBRACKET);
    result_ = result_ && expr(builder_, level_ + 1);
    result_ = result_ && consumeToken(builder_, RBRACKET);
    exit_section_(builder_, marker_, ARRAY_ACCESS, result_);
    return result_;
  }

  /* ********************************************************** */
  // LBRACKET (expr (COMMA expr)*)? RBRACKET
  public static boolean array_literal(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "array_literal")) return false;
    if (!nextTokenIs(builder_, LBRACKET)) return false;
    boolean result_;
    Marker marker_ = enter_section_(builder_);
    result_ = consumeToken(builder_, LBRACKET);
    result_ = result_ && array_literal_1(builder_, level_ + 1);
    result_ = result_ && consumeToken(builder_, RBRACKET);
    exit_section_(builder_, marker_, ARRAY_LITERAL, result_);
    return result_;
  }

  // (expr (COMMA expr)*)?
  private static boolean array_literal_1(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "array_literal_1")) return false;
    array_literal_1_0(builder_, level_ + 1);
    return true;
  }

  // expr (COMMA expr)*
  private static boolean array_literal_1_0(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "array_literal_1_0")) return false;
    boolean result_;
    Marker marker_ = enter_section_(builder_);
    result_ = expr(builder_, level_ + 1);
    result_ = result_ && array_literal_1_0_1(builder_, level_ + 1);
    exit_section_(builder_, marker_, null, result_);
    return result_;
  }

  // (COMMA expr)*
  private static boolean array_literal_1_0_1(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "array_literal_1_0_1")) return false;
    while (true) {
      int pos_ = current_position_(builder_);
      if (!array_literal_1_0_1_0(builder_, level_ + 1)) break;
      if (!empty_element_parsed_guard_(builder_, "array_literal_1_0_1", pos_)) break;
    }
    return true;
  }

  // COMMA expr
  private static boolean array_literal_1_0_1_0(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "array_literal_1_0_1_0")) return false;
    boolean result_;
    Marker marker_ = enter_section_(builder_);
    result_ = consumeToken(builder_, COMMA);
    result_ = result_ && expr(builder_, level_ + 1);
    exit_section_(builder_, marker_, null, result_);
    return result_;
  }

  /* ********************************************************** */
  // expr (PLUS | MINUS | MULTIPLY | DIVIDE) expr
  public static boolean binary_expr(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "binary_expr")) return false;
    boolean result_;
    Marker marker_ = enter_section_(builder_, level_, _NONE_, BINARY_EXPR, "<binary expr>");
    result_ = expr(builder_, level_ + 1);
    result_ = result_ && binary_expr_1(builder_, level_ + 1);
    result_ = result_ && expr(builder_, level_ + 1);
    exit_section_(builder_, level_, marker_, result_, false, null);
    return result_;
  }

  // PLUS | MINUS | MULTIPLY | DIVIDE
  private static boolean binary_expr_1(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "binary_expr_1")) return false;
    boolean result_;
    result_ = consumeToken(builder_, PLUS);
    if (!result_) result_ = consumeToken(builder_, MINUS);
    if (!result_) result_ = consumeToken(builder_, MULTIPLY);
    if (!result_) result_ = consumeToken(builder_, DIVIDE);
    return result_;
  }

  /* ********************************************************** */
  // IDENTIFIER LPAREN (expr (COMMA expr)*)? RPAREN
  public static boolean call_expr(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "call_expr")) return false;
    if (!nextTokenIs(builder_, IDENTIFIER)) return false;
    boolean result_;
    Marker marker_ = enter_section_(builder_);
    result_ = consumeTokens(builder_, 0, IDENTIFIER, LPAREN);
    result_ = result_ && call_expr_2(builder_, level_ + 1);
    result_ = result_ && consumeToken(builder_, RPAREN);
    exit_section_(builder_, marker_, CALL_EXPR, result_);
    return result_;
  }

  // (expr (COMMA expr)*)?
  private static boolean call_expr_2(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "call_expr_2")) return false;
    call_expr_2_0(builder_, level_ + 1);
    return true;
  }

  // expr (COMMA expr)*
  private static boolean call_expr_2_0(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "call_expr_2_0")) return false;
    boolean result_;
    Marker marker_ = enter_section_(builder_);
    result_ = expr(builder_, level_ + 1);
    result_ = result_ && call_expr_2_0_1(builder_, level_ + 1);
    exit_section_(builder_, marker_, null, result_);
    return result_;
  }

  // (COMMA expr)*
  private static boolean call_expr_2_0_1(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "call_expr_2_0_1")) return false;
    while (true) {
      int pos_ = current_position_(builder_);
      if (!call_expr_2_0_1_0(builder_, level_ + 1)) break;
      if (!empty_element_parsed_guard_(builder_, "call_expr_2_0_1", pos_)) break;
    }
    return true;
  }

  // COMMA expr
  private static boolean call_expr_2_0_1_0(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "call_expr_2_0_1_0")) return false;
    boolean result_;
    Marker marker_ = enter_section_(builder_);
    result_ = consumeToken(builder_, COMMA);
    result_ = result_ && expr(builder_, level_ + 1);
    exit_section_(builder_, marker_, null, result_);
    return result_;
  }

  /* ********************************************************** */
  // binary_expr | array_access | call_expr | ref_expr | array_literal | literal
  public static boolean expr(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "expr")) return false;
    boolean result_;
    Marker marker_ = enter_section_(builder_, level_, _NONE_, EXPR, "<expr>");
    result_ = binary_expr(builder_, level_ + 1);
    if (!result_) result_ = array_access(builder_, level_ + 1);
    if (!result_) result_ = call_expr(builder_, level_ + 1);
    if (!result_) result_ = ref_expr(builder_, level_ + 1);
    if (!result_) result_ = array_literal(builder_, level_ + 1);
    if (!result_) result_ = literal(builder_, level_ + 1);
    exit_section_(builder_, level_, marker_, result_, false, null);
    return result_;
  }

  /* ********************************************************** */
  // FUNCTION IDENTIFIER LPAREN param_list? RPAREN COLON type LBRACE statement_* RBRACE
  public static boolean function_def(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "function_def")) return false;
    if (!nextTokenIs(builder_, FUNCTION)) return false;
    boolean result_;
    Marker marker_ = enter_section_(builder_);
    result_ = consumeTokens(builder_, 0, FUNCTION, IDENTIFIER, LPAREN);
    result_ = result_ && function_def_3(builder_, level_ + 1);
    result_ = result_ && consumeTokens(builder_, 0, RPAREN, COLON);
    result_ = result_ && type(builder_, level_ + 1);
    result_ = result_ && consumeToken(builder_, LBRACE);
    result_ = result_ && function_def_8(builder_, level_ + 1);
    result_ = result_ && consumeToken(builder_, RBRACE);
    exit_section_(builder_, marker_, FUNCTION_DEF, result_);
    return result_;
  }

  // param_list?
  private static boolean function_def_3(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "function_def_3")) return false;
    param_list(builder_, level_ + 1);
    return true;
  }

  // statement_*
  private static boolean function_def_8(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "function_def_8")) return false;
    while (true) {
      int pos_ = current_position_(builder_);
      if (!statement_(builder_, level_ + 1)) break;
      if (!empty_element_parsed_guard_(builder_, "function_def_8", pos_)) break;
    }
    return true;
  }

  /* ********************************************************** */
  // function_def|statement_
  static boolean item_(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "item_")) return false;
    boolean result_;
    result_ = function_def(builder_, level_ + 1);
    if (!result_) result_ = statement_(builder_, level_ + 1);
    return result_;
  }

  /* ********************************************************** */
  // NUMBER_LITERAL | STRING_LITERAL | TRUE | FALSE
  public static boolean literal(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "literal")) return false;
    boolean result_;
    Marker marker_ = enter_section_(builder_, level_, _NONE_, LITERAL, "<literal>");
    result_ = consumeToken(builder_, NUMBER_LITERAL);
    if (!result_) result_ = consumeToken(builder_, STRING_LITERAL);
    if (!result_) result_ = consumeToken(builder_, TRUE);
    if (!result_) result_ = consumeToken(builder_, FALSE);
    exit_section_(builder_, level_, marker_, result_, false, null);
    return result_;
  }

  /* ********************************************************** */
  // IDENTIFIER COLON type
  public static boolean param(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "param")) return false;
    if (!nextTokenIs(builder_, IDENTIFIER)) return false;
    boolean result_;
    Marker marker_ = enter_section_(builder_);
    result_ = consumeTokens(builder_, 0, IDENTIFIER, COLON);
    result_ = result_ && type(builder_, level_ + 1);
    exit_section_(builder_, marker_, PARAM, result_);
    return result_;
  }

  /* ********************************************************** */
  // param (COMMA param)*
  public static boolean param_list(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "param_list")) return false;
    if (!nextTokenIs(builder_, IDENTIFIER)) return false;
    boolean result_;
    Marker marker_ = enter_section_(builder_);
    result_ = param(builder_, level_ + 1);
    result_ = result_ && param_list_1(builder_, level_ + 1);
    exit_section_(builder_, marker_, PARAM_LIST, result_);
    return result_;
  }

  // (COMMA param)*
  private static boolean param_list_1(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "param_list_1")) return false;
    while (true) {
      int pos_ = current_position_(builder_);
      if (!param_list_1_0(builder_, level_ + 1)) break;
      if (!empty_element_parsed_guard_(builder_, "param_list_1", pos_)) break;
    }
    return true;
  }

  // COMMA param
  private static boolean param_list_1_0(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "param_list_1_0")) return false;
    boolean result_;
    Marker marker_ = enter_section_(builder_);
    result_ = consumeToken(builder_, COMMA);
    result_ = result_ && param(builder_, level_ + 1);
    exit_section_(builder_, marker_, null, result_);
    return result_;
  }

  /* ********************************************************** */
  // IDENTIFIER
  public static boolean ref_expr(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "ref_expr")) return false;
    if (!nextTokenIs(builder_, IDENTIFIER)) return false;
    boolean result_;
    Marker marker_ = enter_section_(builder_);
    result_ = consumeToken(builder_, IDENTIFIER);
    exit_section_(builder_, marker_, REF_EXPR, result_);
    return result_;
  }

  /* ********************************************************** */
  // RETURN expr
  public static boolean return_statement(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "return_statement")) return false;
    if (!nextTokenIs(builder_, RETURN)) return false;
    boolean result_;
    Marker marker_ = enter_section_(builder_);
    result_ = consumeToken(builder_, RETURN);
    result_ = result_ && expr(builder_, level_ + 1);
    exit_section_(builder_, marker_, RETURN_STATEMENT, result_);
    return result_;
  }

  /* ********************************************************** */
  // item_*
  static boolean root(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "root")) return false;
    while (true) {
      int pos_ = current_position_(builder_);
      if (!item_(builder_, level_ + 1)) break;
      if (!empty_element_parsed_guard_(builder_, "root", pos_)) break;
    }
    return true;
  }

  /* ********************************************************** */
  // (var_declaration | return_statement | expr) SEMICOLON
  public static boolean statement_(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "statement_")) return false;
    boolean result_;
    Marker marker_ = enter_section_(builder_, level_, _NONE_, STATEMENT_, "<statement>");
    result_ = statement__0(builder_, level_ + 1);
    result_ = result_ && consumeToken(builder_, SEMICOLON);
    exit_section_(builder_, level_, marker_, result_, false, null);
    return result_;
  }

  // var_declaration | return_statement | expr
  private static boolean statement__0(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "statement__0")) return false;
    boolean result_;
    result_ = var_declaration(builder_, level_ + 1);
    if (!result_) result_ = return_statement(builder_, level_ + 1);
    if (!result_) result_ = expr(builder_, level_ + 1);
    return result_;
  }

  /* ********************************************************** */
  // NUMBER_TYPE | STRING_TYPE | BOOLEAN_TYPE | ANY_TYPE
  public static boolean type(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "type")) return false;
    boolean result_;
    Marker marker_ = enter_section_(builder_, level_, _NONE_, TYPE, "<type>");
    result_ = consumeToken(builder_, NUMBER_TYPE);
    if (!result_) result_ = consumeToken(builder_, STRING_TYPE);
    if (!result_) result_ = consumeToken(builder_, BOOLEAN_TYPE);
    if (!result_) result_ = consumeToken(builder_, ANY_TYPE);
    exit_section_(builder_, level_, marker_, result_, false, null);
    return result_;
  }

  /* ********************************************************** */
  // VAR IDENTIFIER ASSIGN expr
  public static boolean var_declaration(PsiBuilder builder_, int level_) {
    if (!recursion_guard_(builder_, level_, "var_declaration")) return false;
    if (!nextTokenIs(builder_, VAR)) return false;
    boolean result_;
    Marker marker_ = enter_section_(builder_);
    result_ = consumeTokens(builder_, 0, VAR, IDENTIFIER, ASSIGN);
    result_ = result_ && expr(builder_, level_ + 1);
    exit_section_(builder_, marker_, VAR_DECLARATION, result_);
    return result_;
  }

}
