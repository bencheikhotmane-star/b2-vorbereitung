from flask import Flask, request, jsonify
from datetime import datetime, timedelta, timezone
from flask_cors import CORS # ضروري للتواصل بين Frontend و Backend

app = Flask(__name__)
# تفعيل CORS للسماح لصفحة login.html (من رابط آخر) بالتواصل مع هذا السيرفر
CORS(app) 

# *******************************************************************
# 🔑 قاعدة بيانات الأكواد والمدة الزمنية
# *******************************************************************
# المفتاح (Key): هو الكود السري
# القيمة (Value): هي مدة الصلاحية (بالأيام)
ACCESS_CODES = {
    # الكود: عدد الأيام
    "CODE24H": 1,        # كود صالح ليوم واحد
    "CODE7J": 7,         # كود صالح لأسبوع
    "B2TRIAL": 30,       # كود صالح لشهر واحد
    "VIP2026": 365,      # كود صالح لسنة
    "DEMO": 0.5          # كود صالح لـ 12 ساعة (نصف يوم)
}

# 🌐 نقطة نهاية التحقق من الكود (API Endpoint)
@app.route('/api/verify_code', methods=['POST'])
def verify_code():
    data = request.get_json()
    entered_code = data.get('code')
    
    # 1. التحقق من أن الكود موجود في القائمة
    if entered_code in ACCESS_CODES:
        duration_days = ACCESS_CODES[entered_code]
        
        # 2. حساب تاريخ انتهاء الصلاحية
        # نحسب تاريخ الانتهاء بناءً على المدة المحددة
        expiration_date = datetime.now(timezone.utc) + timedelta(days=duration_days)
        
        # 3. تحويل تاريخ الانتهاء إلى timestamp (بالمللي ثانية) ليستخدمه JavaScript
        expiration_timestamp_ms = int(expiration_date.timestamp() * 1000)

        # 4. إرجاع النجاح وتاريخ انتهاء الصلاحية
        return jsonify({
            "status": "success",
            "message": "Access granted",
            "valid_until": expiration_timestamp_ms
        }), 200
    else:
        # 5. إرجاع رسالة خطأ إذا كان الكود غير موجود
        return jsonify({
            "status": "invalid",
            "message": "Falscher Code. Bitte erneut versuchen."
        }), 401

# 🚀 تشغيل التطبيق (Render يستخدم gunicorn لبدء التشغيل، لكن هذا ضروري إذا أردت الاختبار محلياً)
if __name__ == '__main__':
    app.run(debug=False)
