import json

from flask import Flask, jsonify, request
import os
import pdfkit
import base64
import requests

htmltopdf = Flask(__name__)

ROOT_PREFIX = '/' + os.path.dirname(os.path.realpath(__file__)).rsplit('\\', 1)[-1]

@htmltopdf.route('/')
def index():
    return "Hola"

@htmltopdf.route('/api/download_pdfs/', methods=['POST'])
def download_pdfs_api():
    content = request.json
    documents = content['documents']
    user = content['user']
    password = content['password']
    if not password or not user:
        return jsonify(error='Usuario y contraseña no enviado'), 400
    files = download_pdfs(documents, user, password)
    result = {"result": files}
    return jsonify(result)


def download_pdfs(documents, user, password):
    s = requests.session()
    login_data = {
        'login': user,
        'password': password
    }
    s.post('https://www.comercionet.cl/usuarios/login.php', data=login_data)
    result = []
    for doc in documents:
        url = "https://www.comercionet.cl/visualizacion/visualizar_documentoORDERS.php?tipo=recibidos&docu_id=" + doc
        cookies = []
        for key, value in s.cookies.get_dict().items():
            cookies.append((key, value))

        options = {'cookie': cookies}
        # verificar configuración de wkhtmltopdf en odoo sh
        config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
        pdfkit.from_url(url, "order.pdf", options=options, configuration=config)
        with open("order.pdf", "rb") as pdf_file:
            pdf_b64 = base64.b64encode(pdf_file.read()).decode('utf-8')
        result.append({'doc_id': doc, 'pdf_file': pdf_b64})
    return result


if __name__ == '__main__':
    htmltopdf.run(debug=True)
