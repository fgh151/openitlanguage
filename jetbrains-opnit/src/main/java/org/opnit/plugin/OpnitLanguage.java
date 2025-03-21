package org.opnit.plugin;

import com.intellij.lang.Language;

public class OpnitLanguage extends Language {
    public static final OpnitLanguage INSTANCE = new OpnitLanguage();

    private OpnitLanguage() {
        super("Opnit");
    }
} 