from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Avg
from .models import (
    UserProfile, Quiz, Question, Option, Subject,
    QuizAttempt, StudentAnswer, Certificate
)
from .forms import (
    CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm,
    QuizForm, SubjectForm
)
from .utils import generate_certificate
import json
from datetime import datetime

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type')
            phone = form.cleaned_data.get('phone')
            
            profile = UserProfile.objects.create(
                user=user,
                user_type=user_type,
                phone=phone
            )
            
            login(request, user)
            messages.success(request, f'Welcome {user.first_name}! Your account has been created.')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'quiz/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'quiz/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required(login_url='login')
def dashboard(request):
    user_profile = request.user.profile
    
    if user_profile.user_type == 'admin':
        return admin_dashboard(request)
    elif user_profile.user_type == 'teacher':
        return teacher_dashboard(request)
    else:
        return student_dashboard(request)

def admin_dashboard(request):
    total_quizzes = Quiz.objects.count()
    total_users = UserProfile.objects.count()
    total_attempts = QuizAttempt.objects.count()
    total_students = UserProfile.objects.filter(user_type='student').count()
    
    recent_attempts = QuizAttempt.objects.select_related('student', 'quiz').order_by('-started_at')[:5]
    
    context = {
        'total_quizzes': total_quizzes,
        'total_users': total_users,
        'total_attempts': total_attempts,
        'total_students': total_students,
        'recent_attempts': recent_attempts,
    }
    return render(request, 'quiz/admin_dashboard.html', context)

def teacher_dashboard(request):
    teacher = request.user
    quizzes = Quiz.objects.filter(created_by=teacher)
    total_quizzes = quizzes.count()
    total_attempts = QuizAttempt.objects.filter(quiz__created_by=teacher).count()
    
    context = {
        'quizzes': quizzes,
        'total_quizzes': total_quizzes,
        'total_attempts': total_attempts,
    }
    return render(request, 'quiz/teacher_dashboard.html', context)

def student_dashboard(request):
    student = request.user
    available_quizzes = Quiz.objects.filter(status='published')
    attempted_quizzes = QuizAttempt.objects.filter(student=student).select_related('quiz')
    certificates = Certificate.objects.filter(quiz_attempt__student=student)
    
    context = {
        'available_quizzes': available_quizzes,
        'attempted_quizzes': attempted_quizzes,
        'certificates': certificates,
    }
    return render(request, 'quiz/student_dashboard.html', context)

@login_required(login_url='login')
def create_quiz(request):
    if request.user.profile.user_type not in ['teacher', 'admin']:
        messages.error(request, 'You do not have permission to create quizzes.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.created_by = request.user
            quiz.save()
            messages.success(request, 'Quiz created successfully!')
            return redirect('edit_quiz', quiz_id=quiz.id)
    else:
        form = QuizForm()
    
    return render(request, 'quiz/create_quiz.html', {'form': form})

@login_required(login_url='login')
def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    if quiz.created_by != request.user and request.user.profile.user_type != 'admin':
        messages.error(request, 'You do not have permission to edit this quiz.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quiz updated successfully!')
            return redirect('quiz_detail', quiz_id=quiz.id)
    else:
        form = QuizForm(instance=quiz)
    
    context = {
        'form': form,
        'quiz': quiz,
        'questions': quiz.questions.all(),
    }
    return render(request, 'quiz/edit_quiz.html', context)

@login_required(login_url='login')
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all().prefetch_related('options')
    
    context = {
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, 'quiz/quiz_detail.html', context)

@login_required(login_url='login')
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, status='published')
    
    if request.user.profile.user_type != 'student':
        messages.error(request, 'Only students can take quizzes.')
        return redirect('dashboard')
    
    attempt, created = QuizAttempt.objects.get_or_create(
        quiz=quiz,
        student=request.user
    )
    
    if attempt.status == 'submitted':
        messages.warning(request, 'You have already submitted this quiz.')
        return redirect('quiz_result', attempt_id=attempt.id)
    
    questions = quiz.questions.all().prefetch_related('options')
    if quiz.shuffle_questions:
        questions = list(questions)
        import random
        random.shuffle(questions)
    
    context = {
        'quiz': quiz,
        'attempt': attempt,
        'questions': questions,
    }
    return render(request, 'quiz/take_quiz.html', context)

@login_required(login_url='login')
@require_POST
def submit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    attempt = get_object_or_404(QuizAttempt, quiz=quiz, student=request.user)
    
    data = json.loads(request.body)
    answers = data.get('answers', {})
    time_taken = data.get('time_taken', 0)
    
    total_score = 0
    obtained_score = 0
    
    for question_id, answer_data in answers.items():
        question = get_object_or_404(Question, id=question_id)
        total_score += question.marks
        
        student_answer = StudentAnswer.objects.create(
            quiz_attempt=attempt,
            question=question,
        )
        
        if question.question_type == 'mcq':
            option_id = answer_data.get('option_id')
            if option_id:
                option = Option.objects.get(id=option_id)
                student_answer.selected_option = option
                if option.is_correct:
                    student_answer.is_correct = True
                    student_answer.marks_obtained = question.marks
                else:
                    if quiz.negative_marking:
                        student_answer.marks_obtained = -quiz.negative_marks
                else:
                    if quiz.negative_marking and not student_answer.is_correct:
                        student_answer.marks_obtained = -quiz.negative_marks
            student_answer.save()
        
        elif question.question_type == 'true_false':
            answer = answer_data.get('answer')
            if answer == 'True' or answer == 'False':
                student_answer.text_answer = answer
                student_answer.save()
        
        elif question.question_type == 'short':
            text = answer_data.get('text', '')
            student_answer.text_answer = text
            student_answer.save()
        
        obtained_score += student_answer.marks_obtained
    
    attempt.total_score = total_score
    attempt.obtained_score = max(0, obtained_score)
    attempt.percentage = (attempt.obtained_score / total_score * 100) if total_score > 0 else 0
    attempt.passed = attempt.percentage >= quiz.passing_score
    attempt.status = 'submitted'
    attempt.time_taken = time_taken
    attempt.submitted_at = datetime.now()
    attempt.save()
    
    if attempt.passed:
        generate_certificate(attempt)
    
    return JsonResponse({
        'success': True,
        'attempt_id': attempt.id,
        'passed': attempt.passed,
        'score': attempt.obtained_score,
        'percentage': attempt.percentage,
    })

@login_required(login_url='login')
def quiz_result(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    
    if attempt.student != request.user and request.user.profile.user_type not in ['teacher', 'admin']:
        messages.error(request, 'You do not have permission to view this result.')
        return redirect('dashboard')
    
    answers = attempt.answers.all().select_related('question', 'selected_option')
    
    context = {
        'attempt': attempt,
        'answers': answers,
        'show_answers': request.user.profile.user_type in ['teacher', 'admin'] or attempt.quiz.show_correct_answers,
    }
    return render(request, 'quiz/quiz_result.html', context)

@login_required(login_url='login')
def download_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id)
    
    if certificate.quiz_attempt.student != request.user and request.user.profile.user_type not in ['teacher', 'admin']:
        messages.error(request, 'You do not have permission to download this certificate.')
        return redirect('dashboard')
    
    return redirect(certificate.pdf_file.url)

@login_required(login_url='login')
def profile(request):
    user_profile = request.user.profile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    
    context = {'form': form, 'profile': user_profile}
    return render(request, 'quiz/profile.html', context)
