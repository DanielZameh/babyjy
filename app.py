
from flask import Flask, render_template
import cv2
import concurrent.futures

app = Flask(__name__)

def get_frame(camera_index):
    cap = cv2.VideoCapture(camera_index)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')
    cap.release()

@app.route('/camera/<camera_index>')
def camera(camera_index):
    return render_template('camera.html', src=f'/video_feed/{camera_index}')

@app.route('/video_feed/<camera_index>')
def video_feed(camera_index):
    return Response(get_frame(int(camera_index)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(threaded=True)
