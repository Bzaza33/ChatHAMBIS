from flask import Flask, request, jsonify, render_template
import g4f
from g4f.Provider import You  # مزود GPT مجاني وسريع

app = Flask(__name__)  # إنشاء تطبيق Flask

# المسار الرئيسي للموقع: يعرض الواجهة
@app.route("/")
def home():
    return render_template("index.html")

# مسار المحادثة: يستقبل الرسالة ويرسلها إلى GPT
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    try:
        # إرسال الرسالة إلى GPT-4o واستقبال الرد
        response = g4f.ChatCompletion.create(
            model="gpt-4o",
            provider=You,
            messages=[{"role": "user", "content": user_message}]
        )
        return jsonify({"response": response})
    except Exception as e:
        # في حال حدوث خطأ
        return jsonify({"response": f"❌ خطأ: {str(e)}"})

# تشغيل الخادم
if __name__ == "__main__":
    app.run(debug=True)
