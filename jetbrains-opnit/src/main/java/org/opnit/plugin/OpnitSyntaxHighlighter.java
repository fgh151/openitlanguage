package org.opnit.plugin;

import com.intellij.lexer.Lexer;
import com.intellij.openapi.editor.DefaultLanguageHighlighterColors;
import com.intellij.openapi.editor.HighlighterColors;
import com.intellij.openapi.editor.colors.TextAttributesKey;
import com.intellij.openapi.fileTypes.SyntaxHighlighterBase;
import com.intellij.psi.TokenType;
import com.intellij.psi.tree.IElementType;
import org.jetbrains.annotations.NotNull;

import static com.intellij.openapi.editor.colors.TextAttributesKey.createTextAttributesKey;

public class OpnitSyntaxHighlighter extends SyntaxHighlighterBase {
    public static final TextAttributesKey KEYWORD = 
        createTextAttributesKey("OPNIT_KEYWORD", DefaultLanguageHighlighterColors.KEYWORD);
    public static final TextAttributesKey FUNCTION = 
        createTextAttributesKey("OPNIT_FUNCTION", DefaultLanguageHighlighterColors.FUNCTION_DECLARATION);
    public static final TextAttributesKey STRING = 
        createTextAttributesKey("OPNIT_STRING", DefaultLanguageHighlighterColors.STRING);
    public static final TextAttributesKey NUMBER = 
        createTextAttributesKey("OPNIT_NUMBER", DefaultLanguageHighlighterColors.NUMBER);
    public static final TextAttributesKey COMMENT = 
        createTextAttributesKey("OPNIT_COMMENT", DefaultLanguageHighlighterColors.LINE_COMMENT);
    public static final TextAttributesKey OPERATOR = 
        createTextAttributesKey("OPNIT_OPERATOR", DefaultLanguageHighlighterColors.OPERATION_SIGN);
    public static final TextAttributesKey TYPE = 
        createTextAttributesKey("OPNIT_TYPE", DefaultLanguageHighlighterColors.CLASS_NAME);
    public static final TextAttributesKey BAD_CHARACTER =
        createTextAttributesKey("OPNIT_BAD_CHARACTER", HighlighterColors.BAD_CHARACTER);

    private static final TextAttributesKey[] KEYWORD_KEYS = new TextAttributesKey[]{KEYWORD};
    private static final TextAttributesKey[] FUNCTION_KEYS = new TextAttributesKey[]{FUNCTION};
    private static final TextAttributesKey[] STRING_KEYS = new TextAttributesKey[]{STRING};
    private static final TextAttributesKey[] NUMBER_KEYS = new TextAttributesKey[]{NUMBER};
    private static final TextAttributesKey[] COMMENT_KEYS = new TextAttributesKey[]{COMMENT};
    private static final TextAttributesKey[] OPERATOR_KEYS = new TextAttributesKey[]{OPERATOR};
    private static final TextAttributesKey[] TYPE_KEYS = new TextAttributesKey[]{TYPE};
    private static final TextAttributesKey[] BAD_CHAR_KEYS = new TextAttributesKey[]{BAD_CHARACTER};
    private static final TextAttributesKey[] EMPTY_KEYS = new TextAttributesKey[0];

    @NotNull
    @Override
    public Lexer getHighlightingLexer() {
        return new OpnitLexerAdapter();
    }

    @NotNull
    @Override
    public TextAttributesKey[] getTokenHighlights(IElementType tokenType) {
        if (tokenType.equals(OpnitTypes.FUNCTION) || 
            tokenType.equals(OpnitTypes.RETURN)) {
            return KEYWORD_KEYS;
        }
        if (tokenType.equals(OpnitTypes.IDENTIFIER)) {
            return FUNCTION_KEYS;
        }
        if (tokenType.equals(OpnitTypes.STRING_LITERAL)) {
            return STRING_KEYS;
        }
        if (tokenType.equals(OpnitTypes.NUMBER_LITERAL)) {
            return NUMBER_KEYS;
        }
        if (tokenType.equals(OpnitTypes.COMMENT)) {
            return COMMENT_KEYS;
        }
        if (tokenType.equals(OpnitTypes.PLUS) || 
            tokenType.equals(OpnitTypes.MINUS) ||
            tokenType.equals(OpnitTypes.MULTIPLY) ||
            tokenType.equals(OpnitTypes.DIVIDE) ||
            tokenType.equals(OpnitTypes.ARROW)) {
            return OPERATOR_KEYS;
        }
        if (tokenType.equals(OpnitTypes.NUMBER_TYPE) ||
            tokenType.equals(OpnitTypes.STRING_TYPE) ||
            tokenType.equals(OpnitTypes.BOOLEAN_TYPE)) {
            return TYPE_KEYS;
        }
        if (tokenType.equals(TokenType.BAD_CHARACTER)) {
            return BAD_CHAR_KEYS;
        }
        return EMPTY_KEYS;
    }
} 