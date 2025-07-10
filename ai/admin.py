from django.contrib import admin
from .models import CareerQuizSubmissionModel

# Register your models here.


class CareerQuizSubmissionAdmin(admin.ModelAdmin):
    list_filter = ['submitted_at']
    list_display = ['questions', 'answers',
                    'recommendations', 'reasoning', 'submitted_at']


admin.site.register(CareerQuizSubmissionModel, CareerQuizSubmissionAdmin)
