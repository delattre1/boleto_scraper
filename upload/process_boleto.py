import pdftotext
import re
from datetime import datetime
import os


def get_credentials():
    import json

    with open('.credentials.txt') as json_file:
        data = json.load(json_file)
        database_credential = data['database']
    return database_credential


def load_pdf(path):
    with open(path, "rb") as f:
        pdf = pdftotext.PDF(f)
        pdf = pdf[0]

    split = pdf.split()
    clean = ' '.join(split).replace('_', '').replace(
        '-', '').replace('(', '').replace(')', '')  # .replace('/','')
    palavras = clean.split()

    return palavras


def is_float(val):
    val = val.replace(',', '.')
    return all([[any([i.isnumeric(), i in ['.', 'e']]) for i in val],  len(val.split('.')) == 2])


def is_float_or_int(string):
    try:
        int(string)
        return True
    except:
        try:
            return is_float(string)
        except:
            return False


def get_data_from_boleto(path):
    palavras = load_pdf(path)
    data_vencimento, valor, codigo_pagamento = dados_boleto(palavras)
    return data_vencimento, valor, codigo_pagamento


def dados_boleto(palavras):
    datas_vencimento = []
    valores_boleto = []
    codigo_de_barras = []
    possiveis_codigos = []

    for i in range(len(palavras) - 10):
        if palavras[i] == "Vencimento":
            for j in range(i, i+10):
                if data_valida(palavras[j]):
                    datas_vencimento.append(palavras[j])

        if palavras[i] == "Valor":
            for j in range(i, i+8):
                if is_float(palavras[j]):
                    valores_boleto.append(palavras[j])

        maybe_is_the_code = True
        for j in range(i, i+5):
            if not is_float_or_int(palavras[j]):
                maybe_is_the_code = False
                continue

        if maybe_is_the_code:
            possiveis_codigos.append(palavras[i:i+5])

    data_vencimento = validate_dados(datas_vencimento)
    valor = 'R$ ' + str(validate_dados(valores_boleto))

    codigo_pagamento = select_rigth_code_from_list(possiveis_codigos)

    return data_vencimento, valor, codigo_pagamento


def data_valida(data):
    try:
        datetime.strptime(data, '%d/%m/%Y')
        return True
    except ValueError:
        return False


def validate_dados(lista):
    try:
        return max(set(lista), key=lista.count)
    except:
        return f"some error with {lista}"


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
        return False


def select_rigth_code_from_list(lista_possibilities):
    for i in lista_possibilities:
        code = ((' ').join(i).replace('.', ' '))
        codigo = correct_bar_code(code)
        if codigo is not False:
            return codigo


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
