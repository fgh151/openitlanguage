package ru.openitstudio.language.psi

import com.intellij.psi.tree.IElementType
import ru.openitstudio.language.OpnitLanguage

class OpnitTokenType(debugName: String) : IElementType(debugName, OpnitLanguage.INSTANCE) 