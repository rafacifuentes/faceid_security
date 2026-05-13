from flask import Flask, render_template, request
import cv2
import os
import numpy as np
from PIL import Image
import sqlite3

app = Flask(__name__)

# =========================
# BANCO DE DADOS
# =========================

conn = sqlite3.connect('faceid.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS pessoas (

    id INTEGER PRIMARY KEY,

    nome TEXT,

    cpf TEXT,

    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS imagens (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    pessoa_id INTEGER,

    caminho_imagem TEXT
)
''')

conn.commit()

conn.close()

# =========================
# DATASET
# =========================

DATASET = "dataset"

if not os.path.exists(DATASET):
    os.makedirs(DATASET)

recognizer = cv2.face.LBPHFaceRecognizer_create()

cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

# =========================
# HOME
# =========================

@app.route('/')
def index():
    return render_template('index.html')


# =========================
# CADASTRO
# =========================

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():

    if request.method == 'POST':

        nome = request.form['nome']

        cpf = request.form['cpf']

        pessoa_id = request.form['id']

        foto = request.files['foto']

        total = len(os.listdir(DATASET))

        caminho = f"{DATASET}/{pessoa_id}_{total}.jpg"

        foto.save(caminho)

        conn = sqlite3.connect('faceid.db')

        cursor = conn.cursor()

        cursor.execute(
            '''
            INSERT OR REPLACE INTO pessoas
            (id, nome, cpf)

            VALUES (?, ?, ?)
            ''',
            (pessoa_id, nome, cpf)
        )

        cursor.execute(
            '''
            INSERT INTO imagens
            (pessoa_id, caminho_imagem)

            VALUES (?, ?)
            ''',
            (pessoa_id, caminho)
        )

        conn.commit()

        conn.close()

        return f"""
        Pessoa cadastrada!<br>
        Nome: {nome}<br>
        CPF: {cpf}<br>
        ID: {pessoa_id}
        """

    return render_template('cadastro.html')


# =========================
# TREINAR
# =========================

@app.route('/treinar')
def treinar():

    faces = []
    ids = []

    arquivos = os.listdir(DATASET)

    if len(arquivos) == 0:
        return "Nenhuma imagem cadastrada!"

    for arquivo in arquivos:

        caminho = os.path.join(DATASET, arquivo)

        imagem = Image.open(caminho).convert('L')

        imagem_np = np.array(imagem, 'uint8')

        nome_arquivo = os.path.split(caminho)[-1]

        pessoa_id = int(
            nome_arquivo.split("_")[0]
        )

        faces_detectadas = cascade.detectMultiScale(imagem_np)

        for (x, y, w, h) in faces_detectadas:

            faces.append(imagem_np[y:y+h, x:x+w])

            ids.append(pessoa_id)

    if len(faces) == 0:
        return "Nenhum rosto detectado nas imagens!"

    recognizer.train(faces, np.array(ids))

    recognizer.write('trainer.yml')

    return "Treinamento concluído!"


# =========================
# RECONHECIMENTO
# =========================

@app.route('/reconhecimento')
def reconhecimento():

    if not os.path.exists('trainer.yml'):
        return "Treine o sistema primeiro!"

    recognizer.read('trainer.yml')

    camera = cv2.VideoCapture(0)

    while True:

        conectado, frame = camera.read()

        cinza = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = cascade.detectMultiScale(
            cinza,
            1.3,
            5
        )

        for (x, y, w, h) in faces:

            id_pessoa, confianca = recognizer.predict(
                cinza[y:y+h, x:x+w]
            )

            conn = sqlite3.connect('faceid.db')

            cursor = conn.cursor()

            cursor.execute(
                "SELECT nome FROM pessoas WHERE id=?",
                (id_pessoa,)
            )

            resultado = cursor.fetchone()

            conn.close()

            if resultado:
                nome = resultado[0]
            else:
                nome = "Desconhecido"

            porcentagem = max(
                0,
                min(100, round(130 - confianca))
            )

            confianca_texto = (
                f"Confianca: {porcentagem}%"
            )

            cv2.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                (0,255,0),
                2
            )

            cv2.putText(
                frame,
                nome,
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2
            )

            cv2.putText(
                frame,
                confianca_texto,
                (x, y+h+25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,0),
                2
            )

        cv2.imshow(
            "Reconhecimento Facial",
            frame
        )

        tecla = cv2.waitKey(1)

        if tecla == 27:
            break

    camera.release()

    cv2.destroyAllWindows()

    return "Reconhecimento encerrado."


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)