from flask import Flask, render_template, request, url_for
from classdef import end, after_end
import random
import os
import uuid
import base64
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ─── API-ключ: задайте переменную окружения ANTHROPIC_API_KEY ────────────────
# Render: Settings → Environment → Add ANTHROPIC_API_KEY = sk-ant-...
API = "AIzaSyBE9DJGO5RC8_gIjI9WIn_KjQOviBwjkQ8"
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', API)
# ─────────────────────────────────────────────────────────────────────────────

question, answer0, answer1, answer2, answer3 = [], [], [], [], []
answertf0, answertf1, answertf2, answertf3 = [], [], [], []
m = []
cs = 0
srt = 0

for i in range(1, after_end() + 2):
    m.append(str(i))
for i in range(11):
    a = random.choice(m)
    b = end(int(a))
    m.remove(a)
    question.append(b[0])
    answer0.append(b[1])
    answer1.append(b[2])
    answer2.append(b[3])
    answer3.append(b[4])
    answertf0.append(b[5])
    answertf1.append(b[6])
    answertf2.append(b[7])
    answertf3.append(b[8])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def analyze_image_with_claude(filepath, ext):
    if not GEMINI_API_KEY:
        return None, 'API-ключ не задан. Добавьте GEMINI_API_KEY.'

    with open(filepath, 'rb') as f:
        image_data = base64.standard_b64encode(f.read()).decode('utf-8')

    media_type_map = {
        'jpg': 'image/jpeg', 'jpeg': 'image/jpeg',
        'png': 'image/png', 'gif': 'image/gif', 'webp': 'image/webp'
    }
    media_type = media_type_map.get(ext, 'image/jpeg')

    payload = {
        "contents": [{
            "parts": [
                {"inline_data": {"mime_type": media_type, "data": image_data}},
                {"text": "Опиши это изображение кратко на русском языке — 2–4 предложения. Укажи что изображено, основные объекты, обстановку. Пиши простым языком."}
            ]
        }]
    }

    try:
        response = requests.post(
            'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent',
            headers={
            'x-goog-api-key': GEMINI_API_KEY,
            'content-type': 'application/json'
        },
        json=payload,
        timeout=30
)
        response.raise_for_status()
        data = response.json()
        text = data['candidates'][0]['content']['parts'][0]['text'].strip()
        return text, None
    except requests.exceptions.Timeout:
        return None, 'Превышено время ожидания.'
    except Exception as e:
        return None, f'Ошибка: {str(e)}'


# ─── МАРШРУТЫ ────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/two')
def two():
    return render_template("two.html")

@app.route('/', methods=['POST'])
def clicked():
    global srt, cs
    srt, cs = 0, 0
    return render_template('index.html')

@app.route('/photo', methods=['GET'])
def photo_search_page():
    return render_template('photo.html')

@app.route('/photo', methods=['POST'])
def photo_search():
    if 'photo' not in request.files:
        return render_template('photo.html', error='Файл не выбран')
    file = request.files['photo']
    if file.filename == '':
        return render_template('photo.html', error='Файл не выбран')
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        description, ai_error = analyze_image_with_claude(filepath, ext)
        image_url = url_for('static', filename=f'uploads/{filename}')
        return render_template(
            'photo_result.html',
            image_url=image_url,
            filename=filename,
            description=description,
            ai_error=ai_error
        )
    return render_template('photo.html', error='Недопустимый формат: PNG, JPG, JPEG, GIF, WEBP')

@app.route('/delete_photo/<filename>', methods=['POST'])
def delete_photo(filename):
    safe_name = secure_filename(filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)
    if os.path.exists(filepath):
        os.remove(filepath)
    return '', 204

@app.route('/arduino', methods=['POST'])
def clicked1():
    global srt, cs
    num_press_but = int(request.form.get('num_but', '99'))
    if num_press_but == 1 and answertf0[srt] == "True":
        cs += 1
    elif num_press_but == 2 and answertf1[srt] == "True":
        cs += 1
    elif num_press_but == 3 and answertf2[srt] == "True":
        cs += 1
    elif num_press_but == 4 and answertf3[srt] == "True":
        cs += 1
    try:
        if srt >= 10:
            return render_template('result.html', cs=cs)
        else:
            srt += 1
            return render_template(
                'opros.html',
                question=question[srt],
                answer0=answer0[srt],
                answer1=answer1[srt],
                answer2=answer2[srt],
                answer3=answer3[srt])
    except Exception as e:
        return f"Ошибка: {str(e)}", 500

@app.route('/two', methods=['POST'])
def clicked2():
    return render_template('two.html')

@app.route('/help', methods=['POST'])
def clicked_help():
    user_input = request.form['user_input']
    if user_input != "":
        with open('b.txt', 'a', encoding='UTF-8') as file:
            file.write(str(user_input) + "\n\n")
    return render_template('help.html')

if __name__ == "__main__":
    app.run(debug=True)
