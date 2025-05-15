from flask import Flask, render_template, request, redirect, send_from_directory, flash
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

app = Flask(__name__)
app.secret_key = 'aessecretkey'
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    key_input = request.form['key']
    key_length = int(request.form['key_length'])
    action = request.form['action']

    # Bổ sung "0" để đủ độ dài khóa
    key = key_input.ljust(key_length, '0').encode()

    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    with open(filepath, 'rb') as f:
        data = f.read()

    cipher = AES.new(key, AES.MODE_ECB)

    try:
        if action == 'encrypt':
            result = cipher.encrypt(pad(data, AES.block_size))
            out_filename = 'encrypted_' + filename
        else:
            result = unpad(cipher.decrypt(data), AES.block_size)
            out_filename = 'decrypted_' + filename
    except ValueError:
        flash("Giải mã thất bại. Có thể sai khóa hoặc sai file.")
        return redirect('/')

    # Ghi file kết quả
    result_path = os.path.join(RESULT_FOLDER, out_filename)
    with open(result_path, 'wb') as f:
        f.write(result)

    # Thử chuyển kết quả sang text để hiển thị
    try:
        preview = result.decode('utf-8')
    except UnicodeDecodeError:
        preview = "(Không thể hiển thị nội dung dạng văn bản)"

    return render_template('download.html', filename=out_filename, preview=preview)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(os.path.abspath(RESULT_FOLDER), filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
