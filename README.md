# Django Quiz Management Portal

A comprehensive online quiz management system built with **Django**, **MySQL**, **HTML5**, and **Tailwind CSS**.

## 🎯 Features

### User Roles
- **👨‍💼 Admin**: Manage quizzes, users, and system settings
- **👨‍🏫 Teacher**: Create and manage quizzes, view student results
- **👨‍🎓 Student**: Take quizzes and earn certificates

### Core Features
✅ User authentication with role-based access control  
✅ Multiple question types (MCQ, True/False, Short Answer)  
✅ Flexible quiz settings (difficulty, time limit, passing score, etc.)  
✅ Real-time quiz taking with countdown timer  
✅ Automatic result calculation with score breakdown  
✅ **Automatic certificate generation** for passing students  
✅ Student performance tracking and analytics  
✅ Responsive design with Tailwind CSS  
✅ Beautiful UI with Font Awesome icons  
✅ Question shuffling and option shuffling  
✅ Negative marking support  

## 📋 Prerequisites

- Python 3.8+
- MySQL Server 5.7+
- pip (Python package manager)
- Virtual Environment (recommended)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/DeepShreyaskar1904/quiz-management-portal.git
cd quiz-management-portal
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create MySQL Database
```sql
CREATE DATABASE quiz_portal_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Configure Environment Variables
```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your settings
```

**Example .env configuration:**
```
SECRET_KEY=your-django-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_ENGINE=django.db.backends.mysql
DB_NAME=quiz_portal_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

### 6. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### 8. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 9. Run Development Server
```bash
python manage.py runserver
```

Access the application at:
- **Main Site**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

## 📁 Project Structure

```
quiz-management-portal/
├── config/
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI configuration
│   └── __init__.py
├── quiz/
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── forms.py             # Django forms
│   ├── urls.py              # Quiz app URLs
│   ├── admin.py             # Admin configuration
│   ├── apps.py              # App configuration
│   ├── utils.py             # Utility functions (Certificate generation)
│   └── __init__.py
├── templates/
│   ├── base.html            # Base template
│   ├── index.html           # Home page
│   └── quiz/
│       ├── navbar.html
│       ├── footer.html
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       ├── create_quiz.html
│       ├── edit_quiz.html
│       ├── quiz_detail.html
│       ├── take_quiz.html
│       ├── quiz_result.html
│       ├── profile.html
│       └── dashboards/
│           ├── admin_dashboard.html
│           ├── teacher_dashboard.html
│           └── student_dashboard.html
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── media/
│   ├── certificates/       # Generated certificates
│   ├── profile_pictures/
│   ├── question_images/
│   └── subject_icons/
├── manage.py
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

## 🗄️ Database Models

### UserProfile
Extends Django User with profile information
- User type (Admin/Teacher/Student)
- Profile picture, phone, bio

### Subject
Quiz subjects/categories

### Quiz
Main quiz entity with configuration
- Title, description, subject
- Duration, difficulty, passing score
- Settings (shuffle, negative marking, etc.)

### Question
Individual quiz questions
- Supports MCQ, True/False, Short Answer
- Marks allocation
- Question ordering

### Option
Answer options for MCQ questions

### QuizAttempt
Student's quiz attempt records
- Score, percentage, pass status
- Time taken tracking

### StudentAnswer
Individual student answers
- Tracks correctness and marks

### Certificate
Auto-generated certificates for passing students
- PDF file storage
- Unique certificate number

## 👥 User Workflows

### Admin
1. Login to admin panel
2. View all users, quizzes, and attempts
3. Manage system settings
4. View analytics and reports

### Teacher
1. Register/Login as Teacher
2. Create new quizzes
3. Add questions and options
4. Publish quizzes for students
5. View student results and analytics
6. Edit existing quizzes

### Student
1. Register/Login as Student
2. Browse available quizzes
3. Take published quizzes with timer
4. View results immediately
5. Download certificates if passed
6. Retake quizzes if needed

## 🎨 UI/UX Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Tailwind CSS**: Modern utility-first styling
- **Font Awesome Icons**: Professional icon set
- **Gradient Backgrounds**: Modern color schemes
- **Real-time Timer**: Countdown timer during quiz
- **Progress Indicators**: Visual feedback for user actions
- **Accessible Forms**: Clear labels and validation messages

## 📦 Technologies Used

| Technology | Version | Purpose |
|-----------|---------|----------|
| Django | 4.2.0 | Web framework |
| MySQL | 5.7+ | Database |
| Python | 3.8+ | Backend language |
| Tailwind CSS | Latest | Frontend styling |
| ReportLab | 4.0.7 | PDF certificate generation |
| Font Awesome | 6.4.0 | Icons |
| jQuery | 3.6.0 | DOM manipulation |

## 🔧 Configuration

### Email Configuration (for certificate sending)
Update `.env`:
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

### Database Configuration
Update database details in `.env`:
```
DB_ENGINE=django.db.backends.mysql
DB_NAME=quiz_portal_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

## 📝 Usage Examples

### Creating a Quiz as Teacher
1. Login as teacher
2. Go to Dashboard → Create New Quiz
3. Fill quiz details (title, description, settings)
4. Add questions and options
5. Publish the quiz
6. Students can now take the quiz

### Taking a Quiz as Student
1. Login as student
2. View available quizzes
3. Click "Start Quiz"
4. Answer all questions within time limit
5. Submit quiz
6. View results
7. Download certificate if passed

## 🔒 Security Features

- CSRF protection on all forms
- Password hashing with Django's authentication
- Role-based access control
- SQL injection prevention (Django ORM)
- XSS protection
- Secure session management

## 📊 Analytics & Reporting

- Student performance tracking
- Quiz attempt statistics
- Score distribution
- Pass/fail rates
- Time tracking
- Admin dashboard with key metrics

## 🐛 Troubleshooting

### MySQL Connection Error
```bash
# Install MySQL client
pip install mysqlclient

# On macOS
brew install mysql-client
```

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

### Migration Issues
```bash
python manage.py migrate --run-syncdb
```

## 📚 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|----------|
| `/quiz/login/` | POST | User login |
| `/quiz/register/` | POST | User registration |
| `/quiz/dashboard/` | GET | User dashboard |
| `/quiz/create/` | POST | Create quiz |
| `/quiz/take/<id>/` | GET | Take quiz |
| `/quiz/submit/<id>/` | POST | Submit quiz |
| `/quiz/result/<id>/` | GET | View result |
| `/quiz/certificate/<id>/download/` | GET | Download certificate |

## 🤝 Contributing

Contributions are welcome! Please feel free to:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 💬 Support & Contact

- **Email**: support@quizportal.com
- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check README for detailed information

## 🎓 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [ReportLab Guide](https://www.reportlab.com/docs/)

## 🚀 Future Enhancements

- [ ] Real-time notifications
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard
- [ ] Quiz templates library
- [ ] Video questions support
- [ ] Plagiarism detection
- [ ] Integration with LMS platforms
- [ ] Multi-language support
- [ ] Video proctoring
- [ ] API documentation (Swagger)

## 📞 Version History

### v1.0.0 (Current)
- Initial release
- Basic quiz management
- Certificate generation
- Three user roles
- Responsive design

---

**Made with ❤️ for educators and learners**
