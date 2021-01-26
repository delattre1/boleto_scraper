import pdftotext
import re
from datetime import datetime


def get_credentials():
    import json

    with open('.credentials.txt') as json_file:
        data = json.load(json_file)
        database_credential = data['database']
    return database_credential


def upload_to_db(path):
    import pymongo
    db_credential = get_credentials()
    client = pymongo.MongoClient(db_credential)
    db = client['teste']
    collection = db['collection_teste']
    valor, vencimento, codigo = get_data_from_boleto(path)
    dados_boleto = {'Valor': valor, 'Vencimento': vencimento, 'Código': codigo}
    try:
        collection.insert_one(dados_boleto)
        return 'successfully added to database '
    except:
        return 'some error ocurred '


def get_data_from_boleto(path):
    palavras = load_pdf(path)
    data_vencimento, valor, codigo_pagamento = dados_boleto(palavras)
    return data_vencimento, valor, codigo_pagamento


def load_pdf(path):
    with open(path, "rb") as f:
        pdf = pdftotext.PDF(f)
        pdf = pdf[0]

    split = pdf.split()
    clean = ' '.join(split).replace('_', '').replace(
        '-', '').replace('(', '').replace(')', '')
    palavras = clean.split()

    return palavras


def data_valida(data):
    try:
        datetime.strptime(data, '%d/%m/%Y')
        return True
    except ValueError:
        return False


def is_float(val):
    val = val.replace(',', '.')
    return all([[any([i.isnumeric(), i in ['.', 'e']]) for i in val],  len(val.split('.')) == 2])


def validate_dados(lista):
    if len(lista) > 1:
        is_equal = True
        for i in range(len(lista) - 1):
            data1 = lista[i]
            data2 = lista[i+1]

            if data1 == data2:
                continue
            else:
                is_equal = False

        if is_equal:
            return data1
        else:
            return "not equal"
    elif len(lista) == 1:
        return lista[0]

    else:
        return "Failed to get data"


def dados_boleto(palavras):
    datas_vencimento = []
    valores_boleto = []
    codigo_de_barras = []

    for i in range(len(palavras)):
        if palavras[i] == "Vencimento":
            for j in range(i, i+10):
                if data_valida(palavras[j]):
                    datas_vencimento.append(palavras[j])

        if palavras[i] == "Valor":
            for j in range(i, i+10):
                if is_float(palavras[j]):
                    valores_boleto.append(palavras[j])

        if palavras[i-1] == "Autenticação" and palavras[i] == "Mecânica":
            for j in range(i+2, i+10):
                try:
                    float(palavras[j])
                    codigo_de_barras.append(palavras[j])
                except:
                    continue

    data_vencimento = validate_dados(datas_vencimento)
    valor = 'R$ ' + str(validate_dados(valores_boleto))
    code_bar = (' ').join(codigo_de_barras).replace('.', ' ')
    codigo_pagamento = correct_bar_code(code_bar)

    return data_vencimento, valor, codigo_pagamento


def correct_bar_code(codigo):
    split = codigo.split()
    without_spaces = ('').join(split)
    tamanho_codigo = (len(without_spaces))

    if tamanho_codigo == 47 or tamanho_codigo == 48:
        return codigo

    elif tamanho_codigo > 48 and tamanho_codigo < 53:
        codigo_corrigido = (' '.join(split[1:]))
        return codigo_corrigido

    else:
        return "falha na identificacao"
