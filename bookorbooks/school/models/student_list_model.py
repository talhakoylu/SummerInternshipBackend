from constants.school_strings import SchoolStrings
from django.db import models
from school.models.abstract_base_model import AbstractSchoolBaseModel


class StudentList(AbstractSchoolBaseModel):
    school_class = models.ForeignKey(
        "school.Class",
        on_delete=models.CASCADE,
        related_name="student_list_class",
        verbose_name=SchoolStrings.StudentListStrings.school_class_verbose_name
    )
    child = models.ForeignKey(
        "account.ChildProfile",
        on_delete=models.CASCADE,
        related_name="student_list_children",
        verbose_name=SchoolStrings.StudentListStrings.child_verbose_name)

    class Meta:
        verbose_name = SchoolStrings.StudentListStrings.meta_verbose_name
        verbose_name_plural = SchoolStrings.StudentListStrings.meta_verbose_name_plural

    def __str__(self):
        return f"{self.school_class.name} : {self.child.user.first_name} {self.child.user.last_name}"