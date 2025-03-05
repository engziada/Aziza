# Marriage Matchmaking System | نظام الزواج التوفيقي

## Features | المميزات

### User Management | إدارة المستخدمين
- User registration with phone number verification | تسجيل المستخدمين مع التحقق من رقم الهاتف
- Secure login system | نظام تسجيل دخول آمن
- Password reset via WhatsApp | إعادة تعيين كلمة المرور عبر واتساب
- Profile management | إدارة الملف الشخصي
- Password change functionality | إمكانية تغيير كلمة المرور

### Profile Features | مميزات الملف الشخصي
- Comprehensive personal information | معلومات شخصية شاملة:
  - Age | العمر
  - Nationality | الجنسية
  - Height and Weight | الطول والوزن
  - Skin Color | لون البشرة
  - Employment Status | الحالة الوظيفية
  - Tribe | القبيلة
  - Smoking Status | حالة التدخين
  - Marital Status | الحالة الاجتماعية
  - Educational Qualifications | المؤهلات التعليمية
  - Location (Area/City) | الموقع (المنطقة/المدينة)
  - Marriage Type (Public/Private) | نوع الزواج (معلن/غير معلن)
  - Personal Description | وصف شخصي
  - Partner Requirements | متطلبات الشريك

### Search Functionality | وظائف البحث
- Advanced search filters | فلاتر بحث متقدمة:
  - Gender | الجنس
  - Age Range | نطاق العمر
  - Nationality | الجنسية
  - Physical Characteristics | الخصائص الجسدية
  - Social Status | الحالة الاجتماعية
  - Location | الموقع
- Detailed search results | نتائج بحث مفصلة

### Communication System | نظام التواصل
- Request communication with potential matches | طلب التواصل مع الشركاء المحتملين
- WhatsApp notifications | إشعارات عبر واتساب
- Request management system | نظام إدارة الطلبات

### Administrative Features | مميزات الإدارة
- User management dashboard | لوحة تحكم إدارة المستخدمين
- Export data functionality | وظيفة تصدير البيانات
- Reset user passwords | إعادة تعيين كلمات مرور المستخدمين
- Delete user accounts | حذف حسابات المستخدمين

### Security Features | ميزات الأمان
- Encrypted passwords | تشفير كلمات المرور
- Session management | إدارة الجلسات
- Protected routes | مسارات محمية
- Input validation | التحقق من صحة المدخلات

### Technical Features | الميزات التقنية
- Responsive design | تصميم متجاوب
- RTL support | دعم الكتابة من اليمين إلى اليسار
- Bootstrap UI framework | إطار عمل Bootstrap للواجهة
- SQLite database | قاعدة بيانات SQLite
- Flask backend | خلفية Flask

## Project Structure | هيكل المشروع

```
dating_app/
├── app/                      # Application package
│   ├── __init__.py           # Application factory
│   ├── auth/                 # Authentication module
│   │   ├── __init__.py
│   │   └── routes.py         # Auth routes
│   ├── profile/              # Profile management module
│   │   ├── __init__.py
│   │   └── routes.py         # Profile routes
│   ├── admin/                # Admin module
│   │   ├── __init__.py
│   │   └── routes.py         # Admin routes
│   ├── models/               # Database models
│   │   ├── __init__.py
│   │   └── models.py         # SQLAlchemy models
│   ├── services/             # Business logic services
│   │   ├── __init__.py
│   │   ├── auth_service.py   # Auth services
│   │   ├── profile_service.py # Profile services
│   │   ├── request_service.py # Request services
│   │   └── admin_service.py  # Admin services
│   ├── utils/                # Utility functions
│   │   ├── __init__.py
│   │   ├── password.py       # Password utilities
│   │   ├── notifications.py  # Notification utilities
│   │   └── logging.py        # Logging utilities
│   ├── static/               # Static files
│   └── templates/            # Templates
├── migrations/               # Database migrations
├── logs/                     # Application logs
├── tests/                    # Test suite
├── config.py                 # Configuration
├── run.py                    # Application entry point
├── init_db.py                # Database initialization script
├── requirements.txt          # Dependencies
└── README.md                 # Documentation
```

## Installation | التثبيت

1. Clone the repository | انسخ المستودع
   ```
   git clone <repository-url>
   cd dating_app
   ```

2. Create a virtual environment | أنشئ بيئة افتراضية
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies | ثبت التبعيات
   ```
   pip install -r requirements.txt
   ```

4. Initialize the database | تهيئة قاعدة البيانات
   ```
   python init_db.py
   ```

5. Run the application | تشغيل التطبيق
   ```
   python run.py
   ```

## Checkpoints | نقاط التفتيش

### Checkpoint 1: Project Restructuring (2025-03-05)
- Reorganized project into a package structure
- Implemented Flask application factory pattern
- Created service layer for business logic
- Added improved logging system
- Standardized database models with better naming conventions
- Added database migration support

### Checkpoint 2: Git Configuration and .gitignore Update (2025-03-05)
- Updated .gitignore file with proper exclusions
- Configured Logs folder to be tracked in git for debugging purposes
- Fixed remote repository configuration

To revert to this checkpoint:
```
git checkout fd3f844d511d5b846f6546896f4bfe4516afeef5
```

## License | الترخيص

This project is licensed under the MIT License - see the LICENSE file for details.