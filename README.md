# FaceID Security

## Sobre o Projeto

O FaceID Security é um sistema web de reconhecimento facial desenvolvido utilizando Python, Flask e OpenCV.

O sistema permite cadastrar pessoas, salvar imagens faciais e realizar reconhecimento facial em tempo real utilizando webcam.

O projeto foi desenvolvido para a disciplina de Programação Web Design.

---

# Tecnologias Utilizadas

- Python
- Flask
- OpenCV
- SQLite
- HTML5
- CSS3
- Bootstrap

---

# Funcionalidades

- Cadastro de pessoas
- Upload de imagens faciais
- Banco de dados SQLite
- Treinamento facial
- Reconhecimento facial em tempo real
- Integração com webcam
- Interface responsiva

---

# Estrutura do Projeto

bash
faceid/
│
├── app.py
├── faceid.db
├── trainer.yml
│
├── dataset/
│
├── templates/
│   ├── index.html
│   └── cadastro.html
│
└── README.md


---

# Como Executar

## Instalar dependências

bash
pip install flask
pip install opencv-contrib-python
pip install pillow
pip install numpy


## Executar projeto

bash
python app.py


---

# Acesso

Abra no navegador:

bash
http://127.0.0.1:5000


---

# Banco de Dados

O sistema utiliza SQLite para armazenar:

- Pessoas cadastradas
- CPF
- Imagens faciais

---

# Autor

Projeto acadêmico desenvolvido para a disciplina de Programação Web Design.