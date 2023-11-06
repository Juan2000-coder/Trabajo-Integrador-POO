"""
 * Aplicativo para control de un robot 3DF conectado
 * de forma local por puerto serie.
 * Componente: Streaming.
 * 
 * @version  1.0
 * @date     2023.11.06
 * @author   Borquez Juan Manuel, Dalessandro Francisco, Miranda Francisco
 * @contact  borquez.juan00@gmail.com, panchodal867@gmail.com, francisconehuenmiranda@gmail.com

"""
import threading
from flask import Flask, Response, render_template
from werkzeug.serving import make_server
import cv2
import logging
import socket

class VideoStreaming(threading.Thread):
    """Una clase para video Streaming. Se define como un hilo en sí."""

    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        self.app = Flask(__name__)          # Crea una instancia de la aplicación Flask.
        self.hostname = socket.getfqdn()    # Obtiene el nombre de host.
        self.server = make_server(socket.gethostbyname_ex(self.hostname)[2][0], 5000, self.app)
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Inicia la captura de video desde la cámara.
        self.apagado = False                           # Bandera para terminar la captura de video.
        logging.getLogger('werkzeug').disabled = True  # Deshabilita el registro de eventos de Werkzeug.

    def generate_frames(self):
        """Función principal para la captura de video."""
        while not self.apagado:
            success, frame = self.cap.read()  # Captura un fotograma de video desde la cámara.
            if not success:
                break
            else:
                _, buffer = cv2.imencode('.jpg', frame)  # Codifica el fotograma en formato JPEG.
                frame = buffer.tobytes()
                # Genera y envía el fotograma en el formato necesario para una transmisión.
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        return

    def run(self):
        @self.app.route("/")
        def index():
            return render_template("index.html")  # Devuelve una plantilla HTML en la ruta raíz.

        @self.app.route("/video_feed")
        def video_feed():
            return Response(self.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
            # Devuelve la secuencia de fotogramas de video en tiempo real en la ruta "/video_feed".

        self.server.serve_forever()  # Inicia el servidor Flask y lo ejecuta de forma indefinida en un hilo.

    def detenerStreaming(self):
        self.apagado = True     # Termina la transmisión.
        self.cap.release()      # Libera la captura de video.
        self.server.shutdown()  # Apaga el servidor Flask.
