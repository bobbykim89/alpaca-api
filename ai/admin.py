from django.contrib import admin
from .models import CareerQuizSubmissionModel, DegreeRecommendationSubmissionModel

# Register your models here.


class CareerQuizSubmissionAdmin(admin.ModelAdmin):
    list_filter = ['submitted_at']
    list_display = ['questions', 'answers',
                    'recommendations', 'reasoning', 'submitted_at']


class DegreeRecommendationSubmissionAdmin(admin.ModelAdmin):
    list_filter = ['submitted_at']
    list_display = ['selected_career', 'answers',
                    'recommendations', 'submitted_at']


admin.site.register(CareerQuizSubmissionModel, CareerQuizSubmissionAdmin)
admin.site.register(DegreeRecommendationSubmissionModel,
                    DegreeRecommendationSubmissionAdmin)
