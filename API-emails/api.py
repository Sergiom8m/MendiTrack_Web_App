from flask import Flask, request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import GMAIL_USER, GMAIL_PASSWORD, SECRET_APP_KEY

# Crear y configurar la app
app = Flask(__name__)
app.secret_key = SECRET_APP_KEY


@app.route('/send', methods=['POST'])
def send_email():
     
    # Recoger los datos de la peticion
    data = request.json
    username = data.get('username')
    email = data.get('email')

    # Definir el cuerpo del correo
    subject = "MENDITRACK - CONFIRMACION DE REGISTRO"
    html_body = """
    <html>
        <body>
         <div>
          <h1>¡Hola {}!</h1>
          <p>Gracias por registrarte en nuestra página web.</p>
          <p>Estamos emocionados de tenerte como parte de nuestra comunidad. Explora nuestras funciones y no dudes en contactarnos si necesitas ayuda.</p>
          <p>Saludos,
          <br>
          <p>El equipo de MENDITRACK</p>
         </div>
        </body>
    </html>
    """.format(username)

    # Configuración del servidor SMTP de Gmail
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Crear el mensaje MIME
    message = MIMEMultipart()
    message["From"] = GMAIL_USER
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(html_body, "html"))

    # Iniciar conexión con el servidor SMTP de Gmail y enviar el correo
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, email, message.as_string())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)