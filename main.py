from flask import Flask, send_file
from io import BytesIO
import paramiko

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bienvenido a la aplicación'

@app.route('/descargar', methods=['GET'])
def descargar():
    # Definir la conexión SSH y descargar el archivo (Lozano.xlsx)
    hostname = 'ssh-natureza.alwaysdata.net'  # Reemplaza con el hostname real
    port = 22  # Puerto SSH
    username = 'natureza_anon'  # Tu nombre de usuario
    password = '(123456)'  # Contraseña para acceder al servidor (considera usar autenticación con clave)

    # Conectarse al servidor SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port=port, username=username, password=password)

    # Usar SFTP para descargar el archivo
    sftp = ssh.open_sftp()
    remote_path = 'Lozano.xlsx'  # Ruta del archivo en el servidor remoto
    file_data = sftp.open(remote_path).read()  # Leer el archivo

    # Cerrar la conexión SSH y SFTP
    sftp.close()
    ssh.close()

    # Devolver el archivo como descarga
    return send_file(
        BytesIO(file_data),
        as_attachment=True,
        download_name='Lozano.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)



