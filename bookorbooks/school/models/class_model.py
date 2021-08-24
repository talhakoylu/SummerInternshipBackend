from django.core.exceptions import ValidationError
from constants.school_strings import SchoolStrings
from django.db import models
from school.models.abstract_base_model import AbstractSchoolBaseModel


class Class(AbstractSchoolBaseModel):
    school = models.ForeignKey(
        "school.School",
        on_delete=models.CASCADE,
        related_name="classes_school",
        verbose_name=SchoolStrings.ClassStrings.school_verbose_name)
    instructor = models.ForeignKey(
        "account.InstructorProfile",
        on_delete=models.CASCADE,
        related_name="instructors_school",
        verbose_name=SchoolStrings.ClassStrings.instructor_verbose_name)
    name = models.CharField(
        max_length=50,
        verbose_name=SchoolStrings.ClassStrings.name_verbose_name)
    grade = models.IntegerField(
        verbose_name=SchoolStrings.ClassStrings.grade_verbose_name)

    class Meta:
        verbose_name = SchoolStrings.ClassStrings.meta_verbose_name
        verbose_name_plural = SchoolStrings.ClassStrings.meta_verbose_name_plural
        ordering = ["name", "grade"]

    def __str__(self):
        return f"{self.school.name} - {self.name} - Grade: {self.grade}"

    def clean(self) -> None:
        """
        This method checks whether the teacher trying to be assigned to the class is working in that school.
        """
        if self.instructor.school != self.school:
            raise ValidationError(SchoolStrings.ClassStrings.instructor_not_working_at_this_school_error)