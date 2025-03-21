package org.opnit.plugin;

import com.intellij.openapi.fileTypes.LanguageFileType;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;

public class OpnitFileType extends LanguageFileType {
    public static final OpnitFileType INSTANCE = new OpnitFileType();

    private OpnitFileType() {
        super(OpnitLanguage.INSTANCE);
    }

    @NotNull
    @Override
    public String getName() {
        return "Opnit File";
    }

    @NotNull
    @Override
    public String getDescription() {
        return "Opnit language file";
    }

    @NotNull
    @Override
    public String getDefaultExtension() {
        return "opnit";
    }

    @Nullable
    @Override
    public Icon getIcon() {
        return null;
    }
} 