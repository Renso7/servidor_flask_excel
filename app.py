from flask import Flask, send_file
import paramiko
from io import BytesIO

app = Flask(__name__)

@app.route('/descargar_excel')
def descargar_excel():
    # Configuración del servidor Alwaysdata con credenciales directas
    hostname = 'ssh-natureza.alwaysdata.net'
    port = 22
    username = 'natureza_anon'
    password = '(123456)'  # Cambiar esto para producción
    ruta_remota = 'Lozano.xlsx'

    # Conectar al servidor SSH y abrir una sesión SFTP
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port=port, username=username, password=password)

    # Descargar el archivo en memoria
    sftp = ssh.open_sftp()
    with sftp.open(ruta_remota, 'rb') as remote_file:
        excel_buffer = BytesIO(remote_file.read())
    sftp.close()
    ssh.close()

    # Preparar el archivo para ser descargado
    excel_buffer.seek(0)
    return send_file(
        excel_buffer,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='Lozano.xlsx'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
