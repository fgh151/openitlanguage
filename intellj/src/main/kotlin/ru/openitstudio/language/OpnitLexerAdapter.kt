package ru.openitstudio.language

import com.intellij.lexer.FlexAdapter
import ru.openitstudio.language.lexer._OpnitLexer

class OpnitLexerAdapter : FlexAdapter(_OpnitLexer(null)) 