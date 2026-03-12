from flask import Flask, request, jsonify, render_template, redirect, url_for
from datetime import datetime, timedelta, timezone
from flask_cors import CORS

app = Flask(__name__)
# CORS لم يعد ضرورياً لأن كل شيء على نفس الرابط، لكن نتركه احتياطاً
CORS(app) 

# *******************************************************************
# 🔑 قاعدة بيانات الأكواد والمدة الزمنية
# *******************************************************************
# المفتاح (Key): هو الكود السري
# القيمة (Value): هي مدة الصلاحية (بالأيام)
ACCESS_CODES = {
    # الكود: عدد الأيام
   # "CODE28H": 1,        # كود صالح ليوم واحد
  #  "CODE9J": 7,         # كود صالح لأسبوع
    "HERR.JAWAD": 7,         # كود صالح لأسبوع
    # "MEDMALIK": 60,   # 12/12/25 verment CIH
  #  "BADR2026S": 60,  # 27/12/25 verment CIH
    "CHAIMAEDEUTSCH": 60,
    "LMGHABAR": 60,
    "IKRAMDEUTSCH": 60,
    "MEDSAYAH": 60,
    "OUZAID&AY": 30,
    "MEDDEUTCH": 60,
    "AMINE2026£": 30,
    "AMAL2026MZ": 60,  # 27/01/26 verment CIH
    "BOUCHRA2026D": 60, # 09/02/26 verment CIH
    "ilyasse9000@#": 60,    # 06/02/26 verment CIH
             # كود صالح لـ 12 ساعة
   "NSD67WECA1": 0.5,          # كود صالح لـ 12 ساعة
}

# 🌐 نقطة نهاية التحقق من الكود (API Endpoint)
@app.route('/api/verify_code', methods=['POST'])
def verify_code():
    data = request.get_json()
    entered_code = data.get('code')
    
    # 1. التحقق من أن الكود موجود
    if entered_code in ACCESS_CODES:
        duration_days = ACCESS_CODES[entered_code]
        
        # 2. حساب تاريخ انتهاء الصلاحية
        expiration_date = datetime.now(timezone.utc) + timedelta(days=duration_days)
        expiration_timestamp_ms = int(expiration_date.timestamp() * 1000)

        # 3. إرجاع النجاح وتاريخ انتهاء الصلاحية
        return jsonify({
            "status": "success",
            "message": "Access granted",
            "valid_until": expiration_timestamp_ms
        }), 200
    else:
        # 4. إرجاع رسالة خطأ
        return jsonify({
            "status": "invalid",
            "message": "Falscher Code. Bitte erneut versuchen."
        }), 401

# 🏠 المسار الافتراضي (الصفحة الرئيسية) - تعرض صفحة الدخول
@app.route('/')
def index_page():
    # سيتم عرض ملف login.html الموجود في مجلد templates
    return render_template('login.html')

# 🔑 مسار قائمة الأزرار المحمية
@app.route('/dashboard')
def dashboard_page():
    # سيتم عرض ملف index.html الموجود في مجلد templates
    return render_template('index.html')


# 🚀 تشغيل التطبيق (للاختبار المحلي فقط)
if __name__ == '__main__':
    app.run(debug=False)
