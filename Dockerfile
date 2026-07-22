# ۱. از یک ایمیج رسمی پایتون استفاده کن
FROM python:3.10-slim

# ۲. جلوگیری از نوشتن فایل‌های .pyc و بافرینگ خروجی
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# ۳. پوشهٔ کاری داخل کانتینر
WORKDIR /app

# ۴. فایل requirements.txt را کپی و کتابخانه‌ها را نصب کن
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# ۵. کل پروژه را کپی کن
COPY . /app/

# ۶. پورت ۸۰۰۰ را باز کن
EXPOSE 8000

# ۷. فرمان پیش‌فرض برای اجرا (با gunicorn)
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]