from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
import os

ALLOWED_EXTENSIONS = {'pdf'}
save_path = './boletos'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = save_path


@app.route('/')
def main():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = (secure_filename(f.filename))
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'file uploaded successfully'


if __name__ == '__main__':
    app.run(debug=False)
