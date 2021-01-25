from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
import os
from process_boleto import get_data_from_boleto

ALLOWED_EXTENSIONS = {'pdf'}
save_path = './boletos'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = save_path


def get_credentials():
    import json

    with open('.credentials.txt') as json_file:
        data = json.load(json_file)
        database_credential = data['database']
    return database_credential


@app.route('/')
def main():
    da = get_credentials()
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


@app.route('/see_mongo')
def see_mongo():

    import pymongo
    db_credential = get_credentials()
    client = pymongo.MongoClient(db_credential)
    db = client['teste']
    collection = db['collection_teste']
    tudo = collection.find({})
    v1 = tudo[0]['valor']
    return str(v1)


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
    app.run(debug=False)
