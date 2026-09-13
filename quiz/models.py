from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('admin', 'Administrator'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user_type})"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "User Profiles"

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='subject_icons/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Quiz(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quizzes')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_quizzes')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    duration_minutes = models.IntegerField(default=30, validators=[MinValueValidator(1)])
    passing_score = models.IntegerField(default=60, validators=[MinValueValidator(0), MaxValueValidator(100)])
    total_questions = models.IntegerField(default=0)
    show_correct_answers = models.BooleanField(default=True)
    shuffle_questions = models.BooleanField(default=True)
    shuffle_options = models.BooleanField(default=True)
    negative_marking = models.BooleanField(default=False)
    negative_marks = models.FloatField(default=0.25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Quizzes"

class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('mcq', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short', 'Short Answer'),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    image = models.ImageField(upload_to='question_images/', null=True, blank=True)
    marks = models.FloatField(default=1.0, validators=[MinValueValidator(0)])
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.quiz.title} - Q{self.order}"
    
    class Meta:
        ordering = ['quiz', 'order']
        verbose_name_plural = "Questions"

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.question.text[:30]} - {self.text}"
    
    class Meta:
        ordering = ['question', 'order']

class QuizAttempt(models.Model):
    STATUS_CHOICES = [
        ('started', 'Started'),
        ('submitted', 'Submitted'),
        ('completed', 'Completed'),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    total_score = models.FloatField(default=0)
    obtained_score = models.FloatField(default=0)
    percentage = models.FloatField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='started')
    passed = models.BooleanField(default=False)
    time_taken = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.student.username} - {self.quiz.title}"
    
    class Meta:
        ordering = ['-started_at']
        verbose_name_plural = "Quiz Attempts"
        unique_together = ('quiz', 'student')

class StudentAnswer(models.Model):
    quiz_attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.SET_NULL, null=True, blank=True)
    text_answer = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)
    marks_obtained = models.FloatField(default=0)
    
    def __str__(self):
        return f"{self.quiz_attempt.student.username} - {self.question.text[:30]}"
    
    class Meta:
        ordering = ['question__order']
        unique_together = ('quiz_attempt', 'question')

class Certificate(models.Model):
    quiz_attempt = models.OneToOneField(QuizAttempt, on_delete=models.CASCADE, related_name='certificate')
    issue_date = models.DateTimeField(auto_now_add=True)
    certificate_number = models.CharField(max_length=50, unique=True)
    pdf_file = models.FileField(upload_to='certificates/')
    
    def __str__(self):
        return f"Certificate - {self.quiz_attempt.student.username}"
    
    class Meta:
        ordering = ['-issue_date']
        verbose_name_plural = "Certificates"
