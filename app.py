from flask import Flask, request, jsonify, render_template
import g4f
from g4f.Provider import You
import sqlite3
import os

app = Flask(__name__)

# إنشاء قاعدة البيانات إذا لم تكن موجودة
def init_db():
    conn = sqlite3.connect("conversations.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    save_message("user", user_message)

    try:
        response = g4f.ChatCompletion.create(
            model="gpt-4o",
            provider=You,
            messages=[{"role": "user", "content": user_message}]
        )
        save_message("bot", response)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"response": f"❌ خطأ: {str(e)}"})

def save_message(sender, msg):
    conn = sqlite3.connect("conversations.db")
    c = conn.cursor()
    c.execute("INSERT INTO messages (sender, message) VALUES (?, ?)", (sender, msg))
    conn.commit()
    conn.close()

@app.route("/delete", methods=["POST"])
def delete():
    conn = sqlite3.connect("conversations.db")
    c = conn.cursor()
    c.execute("DELETE FROM messages")
    conn.commit()
    conn.close()
    return jsonify({"response": "✅ تم مسح كل المحادثات."})

if __name__ == "__main__":
    app.run(debug=True)

