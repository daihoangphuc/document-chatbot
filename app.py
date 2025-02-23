from flask import Flask, request, render_template, flash, redirect
from werkzeug.utils import secure_filename
import os
from github import Github

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads/'
GITHUB_TOKEN = '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'  # Thay bằng GitHub PAT
REPO_NAME = 'daihoangphuc/document-chatbot'   # Thay bằng repo của bạn

# Khởi tạo GitHub API
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'docx', 'txt'}

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('Không có file')
        return redirect('/')
    file = request.files['file']
    if file.filename == '':
        flash('Chưa chọn file')
        return redirect('/')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        with open(file_path, 'rb') as f:
            content = f.read()
        
        # Kiểm tra xem file đã tồn tại hay chưa
        try:
            existing_file = repo.get_contents(f'uploads/{filename}')
            repo.update_file(existing_file.path, f'Cập nhật {filename}', content, existing_file.sha)
            flash('File đã được cập nhật trên GitHub. Quá trình fine-tuning sẽ tự động bắt đầu.')
        except:
            repo.create_file(f'uploads/{filename}', f'Thêm {filename}', content)
            flash('File đã được tải lên GitHub. Quá trình fine-tuning sẽ tự động bắt đầu.')
        
        return redirect('/')
    else:
        flash('Định dạng file không hợp lệ')
        return redirect('/')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)