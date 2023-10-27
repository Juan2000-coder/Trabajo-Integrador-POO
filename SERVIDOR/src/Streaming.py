import cv2
from flask import Flask, Response, render_template

app = Flask(__name__)
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)  # Abre la cámara

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame) #Lo encodea en jpg, es como que el programa esta constantemente leyendo imagenes y pegandolas juntas para armar un video
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/")
def index():
    return render_template("index.html") #Template html esta en la carpeta templates. No tocar

@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run('0.0.0.0',port=8000,debug=False)

cap.release()

