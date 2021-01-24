import pdftotext
import re
from datetime import datetime


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
    valor = validate_dados(valores_boleto)
    codigo_pagamento = (' ').join(codigo_de_barras).replace('.', ' ')

    return data_vencimento, valor, codigo_pagamento
