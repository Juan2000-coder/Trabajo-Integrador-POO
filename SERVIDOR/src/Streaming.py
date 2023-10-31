import cv2
from flask import Flask, Response, render_template
import logging

class VideoStreamer:
    def __init__(self):
        self.app = Flask(__name__)
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        logging.getLogger('werkzeug').disabled = True

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
        
        self.app.run(host='0.0.0.0', port=8000, debug=False)

        
    def stop_streaming(self):
        self.streaming = False
        self.cap.release()
        
"""
if __name__ == "__main__":
    try:
        elrubius = VideoStreamer()
        thread = threading.Thread(target=elrubius.run, daemon=True)
        thread.start()

        while True:
            input("pone algo")
    except KeyboardInterrupt:
        elrubius.stop_streaming()
        print("hola")
        print("hola")"""