from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import cv2
# ... otra lógica de tu servidor

class VideoServer:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def get_video_frame(self):
        ret, frame = self.cap.read()
        if ret:
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            return frame
        else:
            return None
