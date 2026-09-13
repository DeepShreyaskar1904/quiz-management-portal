# Django Quiz Management Portal - Deployment Guide

## 🚀 Production Deployment

### Recommended Hosting Platforms
- AWS (EC2, RDS)
- DigitalOcean
- Heroku
- PythonAnywhere
- Google Cloud Platform

### Pre-Deployment Checklist

- [ ] Set `DEBUG = False` in settings.py
- [ ] Set secure `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use environment variables for sensitive data
- [ ] Set up HTTPS/SSL certificates
- [ ] Configure proper database backups
- [ ] Set up email configuration
- [ ] Test all features in staging environment

### Environment Setup for Production

```bash
# Create production .env file
DEBUG=False
SECRET_KEY=your-very-secure-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DB_ENGINE=django.db.backends.mysql
DB_NAME=prod_quiz_db
DB_USER=prod_user
DB_PASSWORD=very-secure-password
DB_HOST=your-rds-endpoint
DB_PORT=3306

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Running with Gunicorn & Nginx

```bash
# Install production server
pip install gunicorn

# Run Gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Database Backup

```bash
# Backup
mysqldump -u root -p quiz_portal_db > backup.sql

# Restore
mysql -u root -p quiz_portal_db < backup.sql
```

## 📞 Support

For deployment issues, refer to Django's deployment documentation.
