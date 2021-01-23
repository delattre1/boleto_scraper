import pdftotext
import re
# Load your PDF
with open("example1.pdf", "rb") as f:
    pdf = pdftotext.PDF(f)
    pdf = pdf[0]

split = pdf.split()
clean = ' '.join(split).replace('_', '').replace('-', '')
palavras = clean.split()

for i in palavras:
    print(i)

print(palavras)

for i in range(len(palavras)):
    if palavras[i] == "R$":
        valor_total = palavras[i+1]
        print(f'valor:  R${valor_total}')

    elif palavras[i] == "Vencimento":
        vencimento = palavras[i+2]
        print(f'vencimento: {vencimento}')
