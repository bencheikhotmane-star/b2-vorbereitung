from flask import Flask, request, jsonify
from datetime import datetime, timedelta, timezone
from flask_cors import CORS # ⚠️ مهم جداً للتواصل بين Frontend و Backend

app = Flask(__name__)
# ⚠️ تمكين CORS للسماح لصفحة index.html بالتواصل مع هذا السيرفر
CORS(app) 

# *******************************************************************
# 🔑 قاعدة بيانات الأكواد والمدة الزمنية
# *******************************************************************
# المفتاح (Key): هو الكود السري الذي تعطيه للمستخدم
# القيمة (Value): هي مدة الصلاحية (بالأيام)
# يمكنك تغيير هذه القيم يدوياً لإضافة أكواد جديدة بمدد مختلفة
ACCESS_CODES = {
    "CODE24H": 1,        # كود صالح ليوم واحد (24 ساعة)
    "CODE7J": 7,         # كود صالح لأسبوع واحد
    "B2TRIAL": 30,       # كود صالح لشهر واحد
    "VIP2026": 365,      # كود صالح لسنة كاملة
    "TEST": 0.5          # كود صالح لـ 12 ساعة (نصف يوم)
}

# 🌐 نقطة نهاية التحقق من الكود (API Endpoint)
@app.route('/api/verify_code', methods=['POST'])
def verify_code():
    data = request.get_json()
    entered_code = data.get('code')
    
    # التحقق من أن الكود موجود في القائمة
    if entered_code in ACCESS_CODES:
        duration_days = ACCESS_CODES[entered_code]
        
        # حساب تاريخ انتهاء الصلاحية
        # استخدام التوقيت العالمي الموحد (UTC)
        expiration_date = datetime.now(timezone.utc) + timedelta(days=duration_days)
        
        # تحويل تاريخ الانتهاء إلى timestamp (بالمللي ثانية) ليستخدمه JavaScript
        expiration_timestamp_ms = int(expiration_date.timestamp() * 1000)

        # إرجاع النجاح وتاريخ انتهاء الصلاحية
        return jsonify({
            "status": "success",
            "message": "Access granted",
            "valid_until": expiration_timestamp_ms
        }), 200
    else:
        # إرجاع رسالة خطأ إذا كان الكود غير موجود
        return jsonify({
            "status": "invalid",
            "message": "Falscher Code. Bitte erneut versuchen."
        }), 401

# 🚀 تشغيل التطبيق (هذا لا يُستخدم في Render، لكنه مفيد للاختبار المحلي)
if __name__ == '__main__':
    app.run(debug=True, port=5000)
