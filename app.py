from flask import Flask, request, send_file
from playwright.sync_api import sync_playwright
import tempfile

app = Flask(__name__)

@app.route('/gerar-pdf', methods=['POST'])
def gerar_pdf():
    data = request.get_json()
    url = data['url']

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        pdf_path = tmpfile.name

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(3000)  # Espera 3 segundos para garantir o carregamento completo

        page.pdf(path=pdf_path, format="A4", print_background=True)
        browser.close()

    return send_file(pdf_path, as_attachment=True, download_name="painel.pdf")
