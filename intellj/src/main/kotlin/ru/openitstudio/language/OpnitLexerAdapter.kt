package ru.openitstudio.language

import com.intellij.lexer.FlexAdapter
import ru.openitstudio.language.lexer._OpnitLexer

class OpnitLexerAdapter : FlexAdapter(_OpnitLexer(null)) {
    companion object {
        private val lexerCache = ThreadLocal.withInitial { _OpnitLexer(null) }
    }

    override fun start(buffer: CharSequence, startOffset: Int, endOffset: Int, initialState: Int) {
        val lexer = lexerCache.get()
        lexer.reset(buffer, startOffset, endOffset, initialState)
        super.start(buffer, startOffset, endOffset, initialState)
    }
} 