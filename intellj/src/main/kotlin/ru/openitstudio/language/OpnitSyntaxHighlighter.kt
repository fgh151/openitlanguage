package ru.openitstudio.language

import com.intellij.lexer.Lexer
import com.intellij.openapi.editor.DefaultLanguageHighlighterColors
import com.intellij.openapi.editor.colors.TextAttributesKey
import com.intellij.openapi.fileTypes.SyntaxHighlighterBase
import com.intellij.psi.tree.IElementType
import ru.openitstudio.language.psi.OpnitTypes
import java.util.concurrent.ConcurrentHashMap

class OpnitSyntaxHighlighter : SyntaxHighlighterBase() {
    companion object {
        val KEYWORD = TextAttributesKey.createTextAttributesKey("OPNIT_KEYWORD", DefaultLanguageHighlighterColors.KEYWORD)
        val STRING = TextAttributesKey.createTextAttributesKey("OPNIT_STRING", DefaultLanguageHighlighterColors.STRING)
        val NUMBER = TextAttributesKey.createTextAttributesKey("OPNIT_NUMBER", DefaultLanguageHighlighterColors.NUMBER)
        val COMMENT = TextAttributesKey.createTextAttributesKey("OPNIT_COMMENT", DefaultLanguageHighlighterColors.LINE_COMMENT)
        val OPERATOR = TextAttributesKey.createTextAttributesKey("OPNIT_OPERATOR", DefaultLanguageHighlighterColors.OPERATION_SIGN)
        val PARENTHESES = TextAttributesKey.createTextAttributesKey("OPNIT_PARENTHESES", DefaultLanguageHighlighterColors.PARENTHESES)
        val IDENTIFIER = TextAttributesKey.createTextAttributesKey("OPNIT_IDENTIFIER", DefaultLanguageHighlighterColors.IDENTIFIER)

        private val KEYWORDS = setOf(
            OpnitTypes.FUNCTION,
            OpnitTypes.RETURN,
            OpnitTypes.TRUE,
            OpnitTypes.FALSE,
            OpnitTypes.NUMBER_TYPE,
            OpnitTypes.STRING_TYPE,
            OpnitTypes.BOOLEAN_TYPE,
            OpnitTypes.ANY_TYPE
        )

        private val OPERATORS = setOf(
            OpnitTypes.PLUS,
            OpnitTypes.MINUS,
            OpnitTypes.MULTIPLY,
            OpnitTypes.DIVIDE
        )

        private val PARENTHESES_TOKENS = setOf(
            OpnitTypes.LPAREN,
            OpnitTypes.RPAREN
        )

        private val TOKEN_HIGHLIGHTS = ConcurrentHashMap<IElementType, Array<TextAttributesKey>>().apply {
            // Pre-populate common tokens
            KEYWORDS.forEach { put(it, arrayOf(KEYWORD)) }
            put(OpnitTypes.STRING_LITERAL, arrayOf(STRING))
            put(OpnitTypes.NUMBER_LITERAL, arrayOf(NUMBER))
            put(OpnitTypes.COMMENT, arrayOf(COMMENT))
            OPERATORS.forEach { put(it, arrayOf(OPERATOR)) }
            PARENTHESES_TOKENS.forEach { put(it, arrayOf(PARENTHESES)) }
            put(OpnitTypes.IDENTIFIER, arrayOf(IDENTIFIER))
        }

        private val lexerCache = ThreadLocal.withInitial { OpnitLexerAdapter() }
    }

    override fun getHighlightingLexer(): Lexer = lexerCache.get()

    override fun getTokenHighlights(tokenType: IElementType): Array<TextAttributesKey> {
        return TOKEN_HIGHLIGHTS[tokenType] ?: TextAttributesKey.EMPTY_ARRAY
    }
} 