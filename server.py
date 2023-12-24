from flask import Flask, request, jsonify, render_template, send_file, request
from firebase import is_valid_user, make_user
import os

from openai_api import tts, stt, chat

import ffmpeg

def convert_webm_to_mp3(input_webm, output_mp3):
    (
        ffmpeg
        .input(input_webm)
        .output(output_mp3, audio_bitrate='192k')
        .run(overwrite_output=True)
    )


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
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_audio():
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
        path_to_mp3 = 'output.mp3'
        convert_webm_to_mp3(filepath, path_to_mp3)

        audio_path = "output.mp3"
        text = stt(audio_path)
        text = chat(text)
        result_mp3_path = 'temp.mp3'
        tts(text, result_mp3_path)

        # 여기서 필요한 처리를 수행합니다.

        # return jsonify({'message': '파일이 성공적으로 업로드되었습니다.'})
        return send_file(result_mp3_path, as_attachment=True)

@app.route('/signup', methods=['POST'])
def sign_up():
    data = request.json
    user_id = data.get('id')
    password = data.get('password')
    if make_user(user_id, password):
        return jsonify({"success": True, "message": "요청이 성공적으로 처리되었습니다."}), 200
    return jsonify({"success": False, "message": "필수 필드가 누락되었습니다."}), 400


@app.route('/signin', methods=['POST'])
def sign_in(): 
    data = request.json
    user_id = data.get('id')
    password = data.get('password')
    print(f'{user_id}, {password}')
    if is_valid_user(user_id, password):
        return jsonify({"success": True, "message": "요청이 성공적으로 처리되었습니다."}), 200
    return jsonify({"success": False, "message": "필수 필드가 누락되었습니다."}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
