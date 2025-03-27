package ru.openitstudio.language

import com.intellij.lang.Language

class OpnitLanguage private constructor() : Language("Opnit") {
    companion object {
        @JvmStatic
        val INSTANCE = OpnitLanguage()
    }
} 