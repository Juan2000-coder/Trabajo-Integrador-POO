import cv2
from flask import Flask, Response, render_template
import threading
import signal
import sys
class VideoStreamer:
    def __init__(self):
        self.app = Flask(__name__)
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def generate_frames(self):
        while True:
            success, frame = self.cap.read()
            if not success:
                break
            else:
                _, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def run(self):
        @self.app.route("/")
        def index():
            return render_template("index.html")

        @self.app.route("/video_feed")
        def video_feed():
            return Response(self.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

        # Indica la dirección IP y el puerto en el que deseas ejecutar la aplicación
        self.app.run(host='0.0.0.0', port=8000, debug=False)

        # Libera la cámara al finalizar la ejecución
        self.cap.release()
        
    def stop_streaming(self):
        self.streaming = False
        self.cap.release()

def start_video_stream():
    video_streamer = VideoStreamer()
    video_thread = threading.Thread(target=video_streamer.run)
    video_thread.start()
    def signal_handler(sig, frame):
        video_streamer.stop_streaming()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

