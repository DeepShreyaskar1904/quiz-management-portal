from django.contrib import admin
from .models import (
    UserProfile, Subject, Quiz, Question, Option,
    QuizAttempt, StudentAnswer, Certificate
)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'phone', 'created_at']
    list_filter = ['user_type', 'created_at']
    search_fields = ['user__username', 'user__email']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'difficulty', 'status', 'created_by', 'created_at']
    list_filter = ['difficulty', 'status', 'created_at']
    search_fields = ['title', 'description']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'quiz', 'question_type', 'marks', 'order']
    list_filter = ['quiz', 'question_type']
    search_fields = ['text']

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'text', 'is_correct']
    list_filter = ['is_correct']
    search_fields = ['text']

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['student', 'quiz', 'status', 'percentage', 'passed', 'started_at']
    list_filter = ['status', 'passed', 'started_at']
    search_fields = ['student__username', 'quiz__title']
    readonly_fields = ['obtained_score', 'percentage', 'passed']

@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ['quiz_attempt', 'question', 'is_correct', 'marks_obtained']
    list_filter = ['is_correct']

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['certificate_number', 'quiz_attempt', 'issue_date']
    list_filter = ['issue_date']
    search_fields = ['certificate_number']
