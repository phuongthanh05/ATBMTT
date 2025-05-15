from flask import Flask, render_template, request, redirect, send_from_directory, flash
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Util import Counter
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
    key_length = int(request.form['aes_bits'])
    action = request.form['action']
    mode = request.form.get('mode', 'ECB')  # default to ECB

    if len(key_input) > key_length:
        flash(f"Độ dài khóa vượt quá {key_length} byte.")
        return redirect('/')

    key = key_input.ljust(key_length, '0').encode()
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    with open(filepath, 'rb') as f:
        data = f.read()

    try:
        if mode == 'CTR':
            nonce = get_random_bytes(8)
            ctr = Counter.new(64, prefix=nonce)
            cipher = AES.new(key, AES.MODE_CTR, counter=ctr)

            if action == 'encrypt':
                result = cipher.encrypt(data)
                result = nonce + result
                out_filename = 'encrypted_' + filename
            else:
                nonce = data[:8]
                ciphertext = data[8:]
                ctr = Counter.new(64, prefix=nonce)
                cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
                result = cipher.decrypt(ciphertext)
                out_filename = 'decrypted_' + filename
        else:  # ECB
            cipher = AES.new(key, AES.MODE_ECB)
            if action == 'encrypt':
                result = cipher.encrypt(pad(data, AES.block_size))
                out_filename = 'encrypted_' + filename
            else:
                result = unpad(cipher.decrypt(data), AES.block_size)
                out_filename = 'decrypted_' + filename
    except ValueError:
        flash("Giải mã thất bại. Có thể sai khóa hoặc sai file.")
        return redirect('/')

    result_path = os.path.join(RESULT_FOLDER, out_filename)
    with open(result_path, 'wb') as f:
        f.write(result)

    file_content = ""
    try:
        file_content = result.decode('utf-8')
    except UnicodeDecodeError:
        file_content = None

    return render_template('result.html', filename=out_filename, action=action, content=file_content)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(os.path.abspath(RESULT_FOLDER), filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
