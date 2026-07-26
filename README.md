
# 📝 Todo API – A Professional Django REST API

یک API قدرتمند و کامل برای مدیریت تسک‌ها، ساخته‌شده با **Django REST Framework** و **Docker**.
این پروژه تمام ویژگی‌های یک سیستم مدیریت وظایف مدرن را در خود دارد و با استفاده از **Celery** و **Redis** قابلیت پردازش‌های پس‌زمینه را نیز فراهم می‌کند.

---

## ✨ ویژگی‌ها

### 🔐 احراز هویت و مجوزها
- ثبت‌نام و ورود با **JWT** (Simple JWT)
- دریافت و تازه‌سازی توکن
- کنترل دسترسی با **Permissions** سفارشی (مثلاً `IsOwner`)
- محدودیت نرخ درخواست (**Throttling**) برای کاربران ناشناس و لاگین‌شده

### 📝 مدیریت تسک‌ها (CRUD)
- ایجاد، خواندن، ویرایش و حذف تسک‌ها
- هر کاربر فقط تسک‌های خود را می‌بیند
- فیلدهای هر تسک: عنوان، توضیحات، اولویت، وضعیت، تاریخ سررسید، عمومی/خصوصی، واگذار به
- **اکشن‌های سفارشی**: `mark-done` (انجام شد)، `overdue` (عقب‌افتاده)، `stats` (آمار)
- **عمومی کردن تسک** با یک کلیک
- فیلتر و جستجوی پیشرفته با `django-filter`
- صفحه‌بندی (`Pagination`) برای لیست‌ها

### 🔔 اعلان‌ها و پردازش‌های پس‌زمینه
- **Celery** + **Redis** برای انجام کارهای زمان‌بر در پس‌زمینه
- ارسال ایمیل یادآوری برای تسک‌های نزدیک به موعد (در حال توسعه)

### 🧪 تست‌های خودکار
- پوشش تست کامل برای مدل‌ها، ویوها و API
- بیش از ۱۵ تست واحد (`Unit Test`) برای تضمین صحت عملکرد

### 🐳 استقرار آسان با Docker
- کانتینرایز کامل با **Docker** و **Docker Compose**
- سرویس‌های مجزا برای `web`، `PostgreSQL`، `Redis` و `Celery Worker`
- آماده برای دیپلوی روی هر پلتفرمی (Render، Railway، AWS و ...)

### 📚 مستندات خودکار
- مستندات تعاملی **Swagger UI** با `drf-spectacular`
- نسخه‌بندی API (`v1`، `v2`)
- **Browsable API** برای تست آسان

---

## 🛠️ تکنولوژی‌های استفاده‌شده

| دسته | تکنولوژی |
|------|-----------|
| **Backend** | Python 3.10, Django 5.x, Django REST Framework |
| **Authentication** | Simple JWT |
| **Database** | PostgreSQL (Dockerized) |
| **Task Queue** | Celery + Redis |
| **Web Server** | Gunicorn |
| **Containerization** | Docker, Docker Compose |
| **Testing** | Django TestCase, APITestCase |
| **Documentation** | drf-spectacular (Swagger) |
| **Static Files** | Whitenoise (for production) |

---

## 📂 ساختار پروژه

```
todo_prj/
├── config/                 # تنظیمات اصلی Django
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py           # پیکربندی Celery
│   └── wsgi.py
├── todo/                   # اپلیکیشن اصلی
│   ├── models.py           # مدل‌های Todo, Notification, Contact
│   ├── serializers.py      # سریالایزرهای DRF
│   ├── views.py            # ویوها و ViewSetها
│   ├── filters.py          # فیلترهای django-filter
│   ├── permissions.py      # مجوزهای سفارشی
│   ├── tasks.py            # Celery Tasks
│   ├── tests.py            # تست‌های خودکار
│   └── urls.py
├── templates/              # قالب‌های ادمین و ایمیل (در صورت نیاز)
├── Dockerfile
├── docker-compose.yml
├── .env                    # متغیرهای محیطی (در Production مخفی)
├── requirements.txt
└── manage.py
```

---

## 🚀 راه‌اندازی سریع (با Docker)

### پیش‌نیازها
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### ۱. کلون کردن مخزن
```bash
git clone https://github.com/your-username/todo-api.git
cd todo-api
```

### ۲. ساخت فایل `.env`
یک فایل `.env` در ریشهٔ پروژه بسازید و مقادیر زیر را (به دلخواه خود) پر کنید:

```env
SECRET_KEY=your-very-secret-key
DEBUG=False
ALLOWED_HOSTS=*
DATABASE_URL=postgres://todo_user:todo_password@db:5432/todo_db
```

### ۳. اجرای پروژه با Docker
```bash
docker compose up --build
```

داکر ایمیج‌ها را می‌سازد، سرویس‌های `web` (Django)، `db` (PostgreSQL)، `redis` و `celery_worker` را راه‌اندازی می‌کند.  
منتظر بمانید تا لاگ `Ready to accept connections` را برای `redis` و `Starting gunicorn` را ببینید.

### ۴. مهاجرت و ایجاد ابرکاربر
در یک ترمینال جدید، دستورات زیر را اجرا کنید:

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

### ۵. دسترسی به API
- **Browsable API**: [http://127.0.0.1:8000/api/v1/todos/](http://127.0.0.1:8000/api/v1/todos/)
- **Swagger UI**: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- **پنل ادمین**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

### ۶. دریافت توکن JWT (برای تست با ابزارهایی مثل Postman)

```bash
http POST http://127.0.0.1:8000/api/token/ username=admin password=yourpassword
```

پاسخ شامل `access` و `refresh` خواهد بود.  
توکن `access` را در هدر `Authorization: Bearer <token>` استفاده کنید.

---

## 🧪 اجرای تست‌ها

```bash
docker compose exec web python manage.py test todo
```

---

## 🌐 API Endpoints

| Method | Endpoint | توضیح |
|--------|----------|-------|
| `GET` | `/api/v1/todos/` | لیست تسک‌های کاربر |
| `POST` | `/api/v1/todos/` | ایجاد تسک جدید |
| `GET` | `/api/v1/todos/{slug}/` | جزئیات یک تسک |
| `PUT` | `/api/v1/todos/{slug}/` | ویرایش کامل تسک |
| `PATCH` | `/api/v1/todos/{slug}/` | ویرایش جزئی |
| `DELETE` | `/api/v1/todos/{slug}/` | حذف تسک |
| `POST` | `/api/v1/todos/{slug}/mark-done/` | تغییر وضعیت به "انجام شده" |
| `GET` | `/api/v1/todos/overdue/` | تسک‌های عقب‌افتاده |
| `GET` | `/api/v1/todos/stats/` | آمار تسک‌های کاربر |

همهٔ Endpointها (به جز دریافت توکن) نیاز به احراز هویت با `Bearer Token` دارند.

---

## 🐳 مدیریت کانتینرها

- **مشاهده لاگ‌ها**:
  ```bash
  docker compose logs -f web
  docker compose logs -f celery_worker
  ```
- **ورود به Shell یک سرویس**:
  ```bash
  docker compose exec web bash
  ```
- **توقف پروژه**:
  ```bash
  docker compose down
  ```
- **توقف و پاک کردن داده‌ها**:
  ```bash
  docker compose down -v
  ```

---

## 🤝 مشارکت

پیشنهادات و مشارکت‌های شما خوش‌آمد است.  
لطفاً یک **Pull Request** باز کنید یا Issue ثبت کنید.

---


---

⭐ اگر این پروژه برایتان مفید بود، لطفاً یک ستاره بدهید!
```

---