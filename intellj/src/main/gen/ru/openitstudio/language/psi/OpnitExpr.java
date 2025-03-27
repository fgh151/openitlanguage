// This is a generated file. Not intended for manual editing.
package ru.openitstudio.language.psi;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.psi.PsiElement;

public interface OpnitExpr extends PsiElement {

  @Nullable
  OpnitBinaryExpr getBinaryExpr();

  @Nullable
  OpnitCallExpr getCallExpr();

  @Nullable
  OpnitLiteral getLiteral();

  @Nullable
  OpnitRefExpr getRefExpr();

}
