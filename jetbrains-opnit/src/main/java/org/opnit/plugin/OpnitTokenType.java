package org.opnit.plugin;

import com.intellij.psi.tree.IElementType;
import org.jetbrains.annotations.NonNls;
import org.jetbrains.annotations.NotNull;

public class OpnitTokenType extends IElementType {
    public OpnitTokenType(@NotNull @NonNls String debugName) {
        super(debugName, OpnitLanguage.INSTANCE);
    }

    @Override
    public String toString() {
        return "OpnitTokenType." + super.toString();
    }
} 