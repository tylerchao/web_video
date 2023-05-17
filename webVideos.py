from flask import Flask,render_template,Response
import cv2

app=Flask(__name__)
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        ## read the camera frame 
        success,frame = camera.read()
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpeg', frame)
            frame=buffer.tobytes()
        
        yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n')

# add the directory containing your templates to the app's search path
app.template_folder = '/Users/tyler/Documents/web_browser_videos/'

# alternatively, you can use the add_template_folder method
#app.add_template_folder('/path/to/templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)