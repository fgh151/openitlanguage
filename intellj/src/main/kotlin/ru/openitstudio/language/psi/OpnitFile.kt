package ru.openitstudio.language.psi

import com.intellij.extapi.psi.PsiFileBase
import com.intellij.psi.FileViewProvider
import ru.openitstudio.language.OpnitFileType
import ru.openitstudio.language.OpnitLanguage

class OpnitFile(viewProvider: FileViewProvider) : PsiFileBase(viewProvider, OpnitLanguage.INSTANCE) {
    override fun getFileType() = OpnitFileType.INSTANCE
} 