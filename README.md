# Telegram VIP Bot

این پروژه یک ربات تلگرام حرفه‌ای است با امکانات:
- ثبت‌نام کاربران و ثبت در Google Sheet
- ذخیره‌سازی داده‌ها در `user_data.json`
- پنل مدیریت با رمز عبور
- تعیین اشتراک (CIP / Hotline) برای کاربران
- محاسبه خودکار `days_left` بر اساس تاریخ شروع

## ⚙️ اجرای رایگان در Render
- Start command: `python3 main.py`
- Environment variables:
  - `BOT_TOKEN`
  - `GOOGLE_SHEET_URL`
  - `WEBHOOK_BASE_URL`
  - `ADMIN_PASSWORD` (مثلاً: `mysecurepass`)
  - `CHANNEL_ID`, `CIP_CHANNEL_ID`, `SUPPORT_ID`, ...

## 🔐 دستورات پنل ادمین
- ورود: `/admin <password>`
- افزودن اشتراک: `/set <phone> <days> <CIP> <Hotline>`
- خروج: `/logout`

## 📊 ساختار Google Sheet:
```
phone | name | days | start_date | days_left | CIP | Hotline
```
