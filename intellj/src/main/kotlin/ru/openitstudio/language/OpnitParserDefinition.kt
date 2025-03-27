package ru.openitstudio.language

import com.intellij.lang.ASTNode
import com.intellij.lang.ParserDefinition
import com.intellij.lang.PsiParser
import com.intellij.lexer.Lexer
import com.intellij.openapi.project.Project
import com.intellij.psi.FileViewProvider
import com.intellij.psi.PsiElement
import com.intellij.psi.PsiFile
import com.intellij.psi.TokenType
import com.intellij.psi.tree.IFileElementType
import com.intellij.psi.tree.TokenSet
import ru.openitstudio.language.parser.OpnitParser
import ru.openitstudio.language.psi.OpnitFile
import ru.openitstudio.language.psi.OpnitTypes

class OpnitParserDefinition : ParserDefinition {
    companion object {
        val WHITE_SPACES = TokenSet.create(TokenType.WHITE_SPACE)
        val COMMENTS = TokenSet.create(OpnitTypes.COMMENT)
        val FILE = IFileElementType(OpnitLanguage.INSTANCE)

        private val lexerCache = ThreadLocal.withInitial { OpnitLexerAdapter() }
        private val parserCache = ThreadLocal.withInitial { OpnitParser() }
    }

    override fun createLexer(project: Project?): Lexer = lexerCache.get()

    override fun createParser(project: Project?): PsiParser = parserCache.get()

    override fun getFileNodeType(): IFileElementType = FILE

    override fun getWhitespaceTokens(): TokenSet = WHITE_SPACES

    override fun getCommentTokens(): TokenSet = COMMENTS

    override fun getStringLiteralElements(): TokenSet = TokenSet.EMPTY

    override fun createElement(node: ASTNode?): PsiElement = OpnitTypes.Factory.createElement(node)

    override fun createFile(viewProvider: FileViewProvider): PsiFile = OpnitFile(viewProvider)
} 