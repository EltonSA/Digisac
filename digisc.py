from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import requests

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Token e URL da API
token = "9f3eedafbbdd4fa90517d94862b678805d12640c"
url = "https://setuptecnologia.digisac.co/api/v1/messages"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# IDs dos remetentes
senders = {
    "*Victor Cals:*": "feabbeab-6c4c-479a-81cc-5d080ae2d5ee",
    "*Felipe:*": "e3b607c9-0b32-491b-8c9a-67683b55b7ca",
    "*Nathan:*": "cdf4a7e9-566a-4b32-8118-436287caafa3"
}

# Função para enviar mensagem
def enviar_mensagem(text, service_id, number, user_id):
    data = {
        "text": text,
        "number": number,
        #"type": "chat",
        "serviceId": service_id,
        #"userId": user_id,
        "origin": "bot",
        "dontOpenticket": True
    }
    response = requests.post(url, headers=headers, json=data)
    return response.status_code == 200

# Rota principal
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Pega os dados do formulário
        sender_name = request.form["sender"]
        message = request.form["message"]

        # Envia mensagem para cada contato do arquivo Excel
        file = request.files["file"]
        file_path = f"{app.config['UPLOAD_FOLDER']}/{file.filename}"
        file.save(file_path)
        
        # Carrega o arquivo Excel
        df = pd.read_excel(file_path)
        
        service_id = "c4fc0bac-7772-490c-adc8-9d0da2343c8b"
        user_id = senders[sender_name]

        clientes_enviados = []  # Lista para armazenar os clientes que receberam mensagens

        for _, row in df.iterrows():
            number = str(row["Numero"])
            nome = row["Nome"]
            personal_message = message.replace("{nome}", nome)
            if enviar_mensagem(personal_message, service_id, number, user_id):
                clientes_enviados.append(nome)

        return render_template("index.html", senders=senders.keys(), clientes_enviados=clientes_enviados)

    return render_template("index.html", senders=senders.keys())



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
