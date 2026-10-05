# راه‌اندازی روی cPanel

1. فایل‌ها رو آپلود کن توی مثلاً `~/telegram-bot` (پوشه‌ی ساب‌دامین، نه public_html).
2. cPanel → **Setup Python App** → Create:
   - Python version: 3.10 یا بالاتر
   - Application root: `telegram-bot`
   - Application URL: ساب‌دامین (مثلاً bot.example.com)
   - Startup file: `passenger_wsgi.py`
   - Entry point: `application`
3. توی همون صفحه، فایل `requirements.txt` رو Install کن (دکمه Run Pip Install).
4. `.env.example` رو کپی کن به `.env` و مقدارها رو پر کن.
5. Restart اپ.
6. توی ترمینال cPanel (با همون virtualenv که بالای صفحه‌ی Python App نشون می‌ده):
   `python set_webhook.py`
7. به ربات پیام بده.

دیباگ: آدرس `https://bot.example.com/` باید `{"ok":true}` برگردونه.
خطاها توی `stderr.log` پوشه‌ی اپ هستن، و `getWebhookInfo` آخرین خطای تلگرام رو نشون می‌ده.

نکته: چون Passenger ممکنه چند پروسه بسازه، State توی حافظه (مثل FSM پیش‌فرض) بین درخواست‌ها
مشترک نیست. وقتی نیاز شد، از Redis یا دیتابیس برای storage استفاده کن.
