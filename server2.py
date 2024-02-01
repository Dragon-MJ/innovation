from flask import Flask, request, jsonify, render_template, send_file, request
from firebase import is_valid_user, make_user
import os
import io
import base64

from openai_api import tts, stt, chat, summary, generate_img, summary_dummy, tts_dummy, chat_dummy, stt_dummy, generate_img_dummy


from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/upload/*": {"origins": "*"}})

# 파일 저장 경로 설정
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    return render_template('test.html')


@app.route('/conversation', methods=['POST'])
def conversation():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']

    # 파일 이름 확인 (선택적)
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file:
        # 파일 저장 경로 설정
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        # 사용 예시
        file.save(filepath)

        audio_path = "output.mp3"
        text = stt(audio_path)
        text = chat(text)
        result_mp3_path = 'temp.mp3'
        tts(text, result_mp3_path)

        # 여기서 필요한 처리를 수행합니다.

        # return jsonify({'message': '파일이 성공적으로 업로드되었습니다.'})
        return send_file(result_mp3_path, as_attachment=True)


@app.route('/conversation/first', methods=['GET'])
def first_conversation():
    # 미리 정의한 text 에 대해 audio 와 text return
    PREDEFINED_TEXT = '오늘 어땠어?'
    result_mp3_path = 'temp.mp3'
    tts_dummy(PREDEFINED_TEXT, result_mp3_path) # tts_dummy

    return send_file(result_mp3_path, as_attachment=True)


@app.route('/conversation/first/selected', methods=['POST'])
def first_selected_converstation():
    text = request.form.get('text')
    result_mp3_path = 'temp.mp3'
    tts_dummy(text, result_mp3_path) # tts_dummy

    return send_file(result_mp3_path, as_attachment=True)


@app.route('/conversation/chat', methods=['POST'])
def chat_conversation():
    user_audio = request.files['user_audio']
    text = stt_dummy(user_audio) # stt_dummy
    response_text = chat_dummy(text) # chat_dummy
    result_mp3_path = 'temp.mp3'
    response_mp3_path = tts_dummy(response_text, result_mp3_path) #tts_dummy
    audio_content = open(response_mp3_path, 'rb').read()

    # Create an in-memory binary stream for the audio content
    audio_stream = io.BytesIO(audio_content)
    audio_base64 = base64.b64encode(audio_stream.getvalue()).decode('utf-8')

    # Send both the text data and audio content in the response
    response_data = {
        'text_data': response_text,
        'audio_file': audio_base64,
    }

    return jsonify(response_data), 200


@app.route('/conversation/summary', methods=['POST'])
def summary_text():
    text = request.form.get('text')
    summary_text = summary_dummy(text) #summary_dummy
    return summary_text


@app.route('/conversation/generate_image', methods=['POST'])
def generate_image():
    text = request.form.get('text')
    img_url = generate_img_dummy(text) # generate_img_dummy
    response_data = {
        'img_url': img_url
    }
    return jsonify(response_data), 200


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
