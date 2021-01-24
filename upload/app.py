from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
import os
from process_boleto import get_data_from_boleto

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


@app.route('/boleto')
def show_boleto_name():
    path = '../example_boletos/ex1.pdf'
    data, vencimento, codigo = get_data_from_boleto(path)
    dados = data + ' ' + vencimento
    return dados


if __name__ == '__main__':
    app.run(debug=False)
