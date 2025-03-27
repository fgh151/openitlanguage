package ru.openitstudio.language

import com.intellij.codeInsight.completion.*
import com.intellij.codeInsight.lookup.LookupElementBuilder
import com.intellij.patterns.PlatformPatterns
import com.intellij.util.ProcessingContext

class OpnitCompletionContributor : CompletionContributor() {
    init {
        // Add keyword completion
        extend(CompletionType.BASIC,
            PlatformPatterns.psiElement(),
            object : CompletionProvider<CompletionParameters>() {
                override fun addCompletions(
                    parameters: CompletionParameters,
                    context: ProcessingContext,
                    result: CompletionResultSet
                ) {
                    // Keywords
                    result.addElement(LookupElementBuilder.create("function"))
                    result.addElement(LookupElementBuilder.create("return"))
                    result.addElement(LookupElementBuilder.create("true"))
                    result.addElement(LookupElementBuilder.create("false"))

                    // Types
                    result.addElement(LookupElementBuilder.create("number"))
                    result.addElement(LookupElementBuilder.create("string"))
                    result.addElement(LookupElementBuilder.create("boolean"))
                    result.addElement(LookupElementBuilder.create("any"))

                    // Built-in functions
                    result.addElement(LookupElementBuilder
                        .create("gettype")
                        .withTailText("(variable: any): string")
                        .withTypeText("Built-in function"))
                    
                    result.addElement(LookupElementBuilder
                        .create("print")
                        .withTailText("(str: any)")
                        .withTypeText("Built-in function"))
                }
            }
        )
    }
} 