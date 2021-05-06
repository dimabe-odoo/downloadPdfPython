import json

from flask import Flask, jsonify, request
import pdfkit
import base64
import requests

app = Flask(__name__)


@app.route('/api/download_pdfs/', methods=['POST'])
def download_pdfs_api():
    content = request.json
    documents = content['documents']
    files = download_pdfs(documents)
    result = {"result": files}
    return jsonify(result)


def download_pdfs(documents):
    s = requests.session()
    login_data = {
        'login': '7808800014004',
        'password': 'Alimpsaexcell2021'
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
    app.run()
