// This is a generated file. Not intended for manual editing.
package ru.openitstudio.language.psi;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.psi.PsiElement;

public interface OpnitFunctionDef extends PsiElement {

  @Nullable
  OpnitParamList getParamList();

  @NotNull
  List<OpnitStatement_> getStatement_List();

  @NotNull
  OpnitType getType();

  @NotNull
  PsiElement getIdentifier();

  //WARNING: getName(...) is skipped
  //matching getName(OpnitFunctionDef, ...)
  //methods are not found in null

  //WARNING: getParameters(...) is skipped
  //matching getParameters(OpnitFunctionDef, ...)
  //methods are not found in null

  //WARNING: getReturnType(...) is skipped
  //matching getReturnType(OpnitFunctionDef, ...)
  //methods are not found in null

}
