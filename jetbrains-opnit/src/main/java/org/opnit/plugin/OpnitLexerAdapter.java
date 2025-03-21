package org.opnit.plugin;

import com.intellij.lexer.FlexAdapter;

public class OpnitLexerAdapter extends FlexAdapter {
    public OpnitLexerAdapter() {
        super(new OpnitLexer(null));
    }
} 