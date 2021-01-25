from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
import os
from process_boleto import get_data_from_boleto, get_credentials

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    from process_boleto import upload_to_db
    save_path = './boletos_processados'
    app.config['UPLOAD_FOLDER'] = save_path
    try:
        if request.method == 'POST':
            f = request.files['file']
            filename = (secure_filename(f.filename))
            caminho_boleto = os.path.join(
                app.config['UPLOAD_FOLDER'], filename)
            f.save(caminho_boleto)
            is_success = upload_to_db(caminho_boleto)
            return is_success + caminho_boleto
    except:
        return 'couldn\'t upload the file'


@app.route('/contas')
def show_contas():
    import pymongo
    db_credential = get_credentials()
    client = pymongo.MongoClient(db_credential)
    db = client['teste']
    collection = db['collection_teste']
    boletos = collection.find({})
    return render_template('contas.html', boletos=boletos)


if __name__ == '__main__':
    app.run(debug=True)
