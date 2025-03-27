// This is a generated file. Not intended for manual editing.
package ru.openitstudio.language.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static ru.openitstudio.language.psi.OpnitTypes.*;
import com.intellij.extapi.psi.ASTWrapperPsiElement;
import ru.openitstudio.language.psi.*;

public class OpnitParamListImpl extends ASTWrapperPsiElement implements OpnitParamList {

  public OpnitParamListImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull OpnitVisitor visitor) {
    visitor.visitParamList(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof OpnitVisitor) accept((OpnitVisitor)visitor);
    else super.accept(visitor);
  }

  @Override
  @NotNull
  public List<OpnitParam> getParamList() {
    return PsiTreeUtil.getChildrenOfTypeAsList(this, OpnitParam.class);
  }

}
