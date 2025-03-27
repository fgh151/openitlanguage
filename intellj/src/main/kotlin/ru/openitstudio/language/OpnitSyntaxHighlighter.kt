package ru.openitstudio.language

import com.intellij.lexer.Lexer
import com.intellij.openapi.editor.DefaultLanguageHighlighterColors
import com.intellij.openapi.editor.colors.TextAttributesKey
import com.intellij.openapi.fileTypes.SyntaxHighlighterBase
import com.intellij.psi.tree.IElementType
import ru.openitstudio.language.psi.OpnitTypes

class OpnitSyntaxHighlighter : SyntaxHighlighterBase() {
    companion object {
        val KEYWORD = TextAttributesKey.createTextAttributesKey("OPNIT_KEYWORD", DefaultLanguageHighlighterColors.KEYWORD)
        val STRING = TextAttributesKey.createTextAttributesKey("OPNIT_STRING", DefaultLanguageHighlighterColors.STRING)
        val NUMBER = TextAttributesKey.createTextAttributesKey("OPNIT_NUMBER", DefaultLanguageHighlighterColors.NUMBER)
        val COMMENT = TextAttributesKey.createTextAttributesKey("OPNIT_COMMENT", DefaultLanguageHighlighterColors.LINE_COMMENT)
        val OPERATOR = TextAttributesKey.createTextAttributesKey("OPNIT_OPERATOR", DefaultLanguageHighlighterColors.OPERATION_SIGN)
        val PARENTHESES = TextAttributesKey.createTextAttributesKey("OPNIT_PARENTHESES", DefaultLanguageHighlighterColors.PARENTHESES)
        val IDENTIFIER = TextAttributesKey.createTextAttributesKey("OPNIT_IDENTIFIER", DefaultLanguageHighlighterColors.IDENTIFIER)
    }

    override fun getHighlightingLexer(): Lexer = OpnitLexerAdapter()

    override fun getTokenHighlights(tokenType: IElementType): Array<TextAttributesKey> {
        return when (tokenType) {
            OpnitTypes.FUNCTION,
            OpnitTypes.RETURN,
            OpnitTypes.TRUE,
            OpnitTypes.FALSE,
            OpnitTypes.NUMBER_TYPE,
            OpnitTypes.STRING_TYPE,
            OpnitTypes.BOOLEAN_TYPE,
            OpnitTypes.ANY_TYPE -> arrayOf(KEYWORD)
            
            OpnitTypes.STRING_LITERAL -> arrayOf(STRING)
            OpnitTypes.NUMBER_LITERAL -> arrayOf(NUMBER)
            OpnitTypes.COMMENT -> arrayOf(COMMENT)
            
            OpnitTypes.PLUS,
            OpnitTypes.MINUS,
            OpnitTypes.MULTIPLY,
            OpnitTypes.DIVIDE -> arrayOf(OPERATOR)
            
            OpnitTypes.LPAREN,
            OpnitTypes.RPAREN -> arrayOf(PARENTHESES)
            
            OpnitTypes.IDENTIFIER -> arrayOf(IDENTIFIER)
            
            else -> TextAttributesKey.EMPTY_ARRAY
        }
    }
} 