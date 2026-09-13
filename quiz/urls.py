from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_quiz, name='create_quiz'),
    path('edit/<int:quiz_id>/', views.edit_quiz, name='edit_quiz'),
    path('detail/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('take/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('submit/<int:quiz_id>/', views.submit_quiz, name='submit_quiz'),
    path('result/<int:attempt_id>/', views.quiz_result, name='quiz_result'),
    path('certificate/<int:certificate_id>/download/', views.download_certificate, name='download_certificate'),
    path('profile/', views.profile, name='profile'),
]
