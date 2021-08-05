from constants.account_strings import AccountStrings
from django.db import models



class ChildList(models.Model):
    parent = models.ForeignKey(
        "account.ParentProfile",
        on_delete=models.CASCADE,
        related_name="parent_children",
        verbose_name=AccountStrings.ChildListString.parent_verbose_name)
    child = models.OneToOneField(
        "account.ChildProfile",
        on_delete=models.CASCADE,
        related_name="child_list",
        verbose_name=AccountStrings.ChildListString.child_verbose_name)

    def __str__(self):
        return f"{self.parent.user.first_name} {self.parent.user.last_name} - {self.child.user.first_name} {self.child.user.last_name}"

    class Meta:
        verbose_name = AccountStrings.ChildListString.meta_verbose_name
        verbose_name_plural = AccountStrings.ChildListString.meta_verbose_name_plural