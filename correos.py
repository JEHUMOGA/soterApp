from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pathlib import Path
import smtplib
import config

class EnvioCorreo:
  def enviar_correo(clave, fecha, hora, imagen, criminal: bool):
    message = MIMEMultipart()
    message["from"] = "SoterApp"
    message["to"] = f"{config.correo()}"
    if criminal:
      message["subject"] = "Ha sido detectado un criminal"
      message.attach(MIMEText(
        f"""Ha sido detectado un criminal
        Clave: {clave}
        Fecha de detección: {fecha}
        Hora de detección: {hora}
        """))
    else:
      message["subject"] = "Ha sido detectada una persona"
      message.attach(MIMEText(f"""Ha sido detectada una persona
      Clave: {clave}
      Fecha de detección: {fecha}
      Hora de detección: {hora}
      """))
    message.attach(MIMEImage(Path(imagen).read_bytes()))

    with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
      smtp.ehlo()
      smtp.starttls()
      smtp.login("soterapp.vigilancia@gmail.com", "vnuvynhqrzzaylmj")
      smtp.send_message(message)
      print("Enviado...")