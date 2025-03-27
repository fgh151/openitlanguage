package ru.openitstudio.language

import com.intellij.openapi.fileTypes.LanguageFileType
import com.intellij.openapi.util.IconLoader
import javax.swing.Icon

class OpnitFileType private constructor() : LanguageFileType(OpnitLanguage.INSTANCE) {
    companion object {
        @JvmStatic
        val INSTANCE = OpnitFileType()
    }

    override fun getName(): String = "Opnit File"
    override fun getDescription(): String = "Opnit language file"
    override fun getDefaultExtension(): String = "opnit"
    override fun getIcon(): Icon = IconLoader.getIcon("/icons/icon.svg", OpnitFileType::class.java)
} 