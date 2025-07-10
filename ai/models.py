from django.db import models

# Create your models here.


class CareerQuizSubmissionModel(models.Model):
    submitted_at = models.DateTimeField(auto_now_add=True)
    questions = models.JSONField()
    answers = models.JSONField()
    recommendations = models.JSONField()
    reasoning = models.TextField()

    def __str__(self):
        return f"Submission on {self.submitted_at}"
