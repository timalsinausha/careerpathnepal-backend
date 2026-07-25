from django.db import models


class AssessmentAttribute(models.Model):

    class Category(models.TextChoices):

        INTEREST = "INTEREST", "Interest"
        TRAIT = "TRAIT", "Trait"
        WORK_STYLE = "WORK_STYLE", "Work Style"
        VALUE = "VALUE", "Value"
        APTITUDE = "APTITUDE", "Aptitude"

    name = models.CharField(
        max_length=100,
        unique=True
    )

    code = models.CharField(
        max_length=50,
        unique=True
    )

    category = models.CharField(
        max_length=20,
        choices=Category.choices
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name
    
class AssessmentQuestion(models.Model):

    class Section(models.TextChoices):

        INTEREST = "INTEREST", "Interests"
        TRAIT = "TRAIT", "Natural Strengths"
        WORK_STYLE = "WORK_STYLE", "Work Style"
        VALUE = "VALUE", "Values"
        APTITUDE = "APTITUDE", "Aptitude"

    section = models.CharField(
        max_length=20,
        choices=Section.choices,
    )


    question_text = models.TextField()

    order = models.PositiveIntegerField(
        unique=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )


class AssessmentOption(models.Model):

    question = models.ForeignKey(
        AssessmentQuestion,
        on_delete=models.CASCADE,
        related_name="options",
    )
    

    option_text = models.TextField()

    option_code = models.CharField(
        max_length=10
    )

    is_correct = models.BooleanField(
        default=False
    )

    order = models.PositiveIntegerField()

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "question",
                    "option_code",
                ],
                name="unique_option_code_per_question",
            ),
        ]

        ordering = [
            "order",
        ]

    def __str__(self):
        return f"{self.option_code}. {self.option_text}"
    

class OptionScore(models.Model):

    option = models.ForeignKey(
        AssessmentOption,
        on_delete=models.CASCADE,
        related_name="scores",
    )

    attribute = models.ForeignKey(
        AssessmentAttribute,
        on_delete=models.CASCADE,
        related_name="option_scores",
    )

    score = models.PositiveIntegerField()

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "option",
                    "attribute",
                ],
                name="unique_option_attribute_score",
            ),
        ]

    def __str__(self):
        return (
            f"{self.option.option_code} "
            f"→ {self.attribute.name}: "
            f"{self.score}"
        )
    


class AssessmentAttempt(models.Model):

    student = models.ForeignKey(
        "student_profile.StudentProfile",
        on_delete=models.CASCADE,
        related_name="assessment_attempts",
    )

    started_at = models.DateTimeField(
        auto_now_add=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    is_completed = models.BooleanField(
        default=False
    )

    def __str__(self):
        return (
            f"{self.student.user.email} "
            f"- Assessment Attempt"
        )
    

class StudentAnswer(models.Model):

    attempt = models.ForeignKey(
        AssessmentAttempt,
        on_delete=models.CASCADE,
        related_name="answers",
    )

    question = models.ForeignKey(
        AssessmentQuestion,
        on_delete=models.CASCADE,
    )

    selected_option = models.ForeignKey(
        AssessmentOption,
        on_delete=models.CASCADE,
    )

    answered_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "attempt",
                    "question",
                ],
                name="one_answer_per_question_per_attempt",
            ),
        ]

    def __str__(self):
        return (
            f"{self.attempt.student.user.email} - "
            f"Question {self.question.order} - "
            f"Option {self.selected_option.option_code}"
        )
    

class StudentAttributeScore(models.Model):

    attempt = models.ForeignKey(
        AssessmentAttempt,
        on_delete=models.CASCADE,
        related_name="attribute_scores",
    )

    attribute = models.ForeignKey(
        AssessmentAttribute,
        on_delete=models.CASCADE,
        related_name="student_scores",
    )

    score = models.PositiveIntegerField()

    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "attempt",
                    "attribute",
                ],
                name="one_attribute_score_per_attempt",
            ),
        ]

    def __str__(self):
        return (
            f"{self.attempt.student.user.email} - "
            f"{self.attribute.name}: "
            f"{self.percentage}%"
        )