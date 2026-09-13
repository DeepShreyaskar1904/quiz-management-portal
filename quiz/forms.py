from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile, Quiz, Question, Option, Subject

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    user_type = forms.ChoiceField(
        choices=[('student', 'Student'), ('teacher', 'Teacher')],
        widget=forms.RadioSelect
    )
    phone = forms.CharField(max_length=15, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'user_type', 'phone')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Phone (Optional)'})

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'bio', 'profile_picture']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'subject', 'difficulty', 'duration_minutes', 
                  'passing_score', 'show_correct_answers', 'shuffle_questions', 
                  'shuffle_options', 'negative_marking', 'negative_marks']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'passing_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'negative_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'show_correct_answers': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'shuffle_questions': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'shuffle_options': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'negative_marking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'description', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'icon': forms.FileInput(attrs={'class': 'form-control'}),
        }
