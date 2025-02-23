from flask import Flask, request, render_template, flash, redirect
from werkzeug.utils import secure_filename  # Sửa từ werkzeug import secure_filename thành dạng này
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Cần cho flash messages
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Kiểm tra loại file hợp lệ
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'docx', 'txt'}

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('Không có file được chọn')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('Chưa chọn file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        flash('Tải file lên thành công. Vui lòng đẩy thư mục uploads lên GitHub và chạy fine-tuning trên Kaggle.')
        return redirect('/')
    else:
        flash('Định dạng file không hợp lệ (chỉ chấp nhận PDF, DOCX, TXT)')
        return redirect(request.url)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)