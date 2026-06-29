# فارسی:

# 📚 لیبریس — سیستم مدیریت کتابخانه شخصی

## این پروژه در وبسایت زیر قابل مشاهده است:
## https://libris-your-personal-library.onrender.com

**لیبریس** یک برنامهٔ تحت وب برای مدیریت کتابخانهٔ شخصی است که با **فلسک (Flask)** ساخته شده است.  
این سیستم به کاربران اجازه می‌دهد ثبت‌نام کنند، مجموعهٔ کتاب‌های خود را مدیریت کنند، وضعیت مطالعه را ردیابی کنند و کتابخانهٔ شخصی‌شان را در یک رابط کاربری تمیز و مینیمال سازماندهی کنند.

این پروژه به عنوان یک تمرین عملی در حوزهٔ **توسعه بک‌اند** طراحی شده و تمرکز ویژه‌ای بر **احراز هویت، طراحی پایگاه داده و ساختار قابل گسترش** دارد.

---

## 🚀 ویژگی‌ها

### 🔐 سیستم احراز هویت
- ثبت‌نام و ورود کاربران  
- هش امن رمز عبور  
- احراز هویت مبتنی بر session  
- بازیابی رمز عبور از طریق ایمیل با توکن محدود به زمان  
- کنترل دسترسی مبتنی بر نقش (ادمین / کاربر عادی)

### 📚 مدیریت کتاب
- اضافه، ویرایش و حذف کتاب  
- ردیابی وضعیت مطالعه (خوانده نشده / در حال مطالعه / خوانده شده)  
- دسته‌بندی کتاب‌ها بر اساس ژانر  
- استفاده از سیستم `enum` برای ثبات داده‌ها

### 👤 داشبورد کاربر
- داشبورد شخصی برای مدیریت کتاب‌ها  
- صفحهٔ پروفایل  
- کنترل دسترسی ادمین

### 📩 سیستم تماس
- فرم تماس با ذخیره‌سازی در دیتابیس  
- پنل ادمین برای مشاهده و مدیریت پیام‌ها

### 💬 رابط کاربری و تجربه کاربری
- رابط تمیز و مینیمال  
- سیستم پیام‌رسانی (Flash Messages)  
- طراحی واکنش‌گرا (Responsive)  
- پشتیبانی از زبان‌های راست‌به‌چپ (فارسی)

---

## 🛠 فناوری‌های استفاده‌شده

**بک‌اند**  
- Python  
- Flask  
- Flask-SQLAlchemy  
- Jinja2  
- Werkzeug Security  

**پایگاه داده**  
- SQLite (برای محیط توسعه)

**فرانت‌اند**  
- HTML5  
- CSS3  
- قالب‌های Jinja

---

## ⚙️ راه‌اندازی و نصب

```bash
git clone https://github.com/MaedehSoleymani/Libris-your-personal-library.git
cd libris
python -m venv venv
source venv/bin/activate        # در لینوکس/مک
# یا
venv\Scripts\activate          # در ویندوز
pip install -r requirements.txt
python app.py
```

برنامه به صورت محلی روی آدرس زیر اجرا می‌شود:
```
http://127.0.0.1:5000/
```

## 🔒 ملاحظات امنیتی
- رمزهای عبور با استفاده از کتابخانهٔ Werkzeug هش می‌شوند.
- توکن‌های بازیابی رمز عبور محدود به زمان هستند.
- دسترسی به روت‌های ادمین محدود شده است.
- اعتبارسنجی فرم‌ها در سمت سرور انجام می‌شود.
- 📈 بهبودهای آینده
- سیستم جستجو و فیلتر
- صفحه‌بندی (Pagination)
- نسخهٔ REST API
- پشتیبانی از PostgreSQL
- کانتینری‌سازی با Docker
- ردیابی پیشرفت مطالعه
- سیستم برچسب‌گذاری (Tagging)
- تست‌های واحد (Unit Tests)

## 🎯 هدف پروژه
- این پروژه به عنوان یک تمرین عملی در توسعه بک‌اند ساخته شده تا مهارت‌های زیر را تقویت کند:
- سیستم‌های احراز هویت
- مدل‌سازی پایگاه داده
- کنترل دسترسی مبتنی بر نقش
- گردش‌های کاری مبتنی بر توکن
- معماری برنامه‌های Flask

این پروژه نشان‌دهندهٔ توانایی در ساخت یک برنامهٔ تحت وب ساختاریافته، امن و قابل گسترش است.


# ENGLISH:

# 📚 Libris — Personal Library Management System

## this website can be visited through this link:
## https://libris-your-personal-library.onrender.com

Libris is a web-based personal library management application built with **Flask**.  
It allows users to register, manage their book collection, track reading status, and organize their personal library through a clean and minimal interface.

This project was developed as a backend-focused practice application with attention to authentication, database design, and scalable structure.

---

## 🚀 Features

### 🔐 Authentication System
- User registration & login
- Secure password hashing
- Session-based authentication
- Password reset via email with time-limited token
- Role-based access (Admin / User)

### 📚 Book Management
- Add, edit, and delete books
- Track reading status (Unread / Reading / Completed)
- Categorize books by genre
- Enum-based status system for data consistency

### 👤 User Dashboard
- Personal dashboard for managing books
- Profile page
- Admin access control

### 📩 Contact System
- Contact form with database storage
- Admin panel for viewing and managing messages

### 💬 UI & UX
- Clean, minimal interface
- Flash messaging system
- Responsive layout
- RTL support (Persian)

---

## 🛠 Tech Stack

**Backend**
- Python
- Flask
- Flask-SQLAlchemy
- Jinja2
- Werkzeug Security

**Database**
- SQLite (development)

**Frontend**
- HTML5
- CSS3
- Jinja Templates

---

## ⚙️ Setup & Installation

```bash
git clone https://github.com/MaedehSoleymani/Libris-your-personal-library.git
cd libris
python -m venv venv
Linux: source venv/bin/activate 
#or 
Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The application runs locally on:

```
http://127.0.0.1:5000/
```

---

## 🔒 Security Considerations

- Passwords are hashed using Werkzeug.
- Reset tokens are time-limited.
- Admin routes are access-restricted.
- Form validation is handled server-side.

---

## 📈 Future Improvements

- Search & filtering system
- Pagination
- REST API version
- PostgreSQL support
- Docker containerization
- Reading progress tracking
- Tagging system
- Unit tests

---

## 🎯 Project Purpose

This project was built as a backend development practice to strengthen:

- Authentication systems
- Database modeling
- Role-based access control
- Token-based workflows
- Flask application architecture

It demonstrates practical experience in building a structured and extendable web application.