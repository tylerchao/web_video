from flask import Flask,render_template,Response
from pypylon import pylon
import cv2

camera=None

def setup():
   print("Setup invoked")
   global camera
   if camera != None:
       print("already initialized")
       return
   
   # Connect to the first available camera
   camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

   # Set camera parameters
   camera.Open()
 
   camera.OffsetX.SetValue(0)
   camera.OffsetY.SetValue(0)
   camera.Width.SetValue(1600)
   camera.Height.SetValue(1200)
   camera.ReverseX.SetValue(True)
   camera.ReverseY.SetValue(True)
   camera.PixelFormat.SetValue("RGB8")  # Set pixel format to RGB8

# Create a video writer object to save the video
#fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#out = cv2.VideoWriter('output.mp4v', fourcc, 25.0, (1600, 1200))

# Start the video capture
   camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

def generate_frames():
    while camera.IsGrabbing():
        ## read the camera frame 
        # Wait for a new frame
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        if not grabResult.GrabSucceeded():
            break
        else:
            # Convert the image to a numpy array and display it
            img = grabResult.Array
#           cv2.imshow("Live Feed", img)
            # Write the frame to the video file
#           out.write(img)
            ret, buffer = cv2.imencode('.jpeg', img)
            frame=buffer.tobytes()
            # Release the current frame
            grabResult.Release()
        
            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n')

app=Flask(__name__)

# add the directory containing your templates to the app's search path
app.template_folder = '/Users/Cognex/Desktop/web_browser_videos/'

# alternatively, you can use the add_template_folder method
#app.add_template_folder('/path/to/templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    try:
      setup()
      app.run(host='0.0.0.0',debug=True, use_reloader=False)
    finally:
       print("closing all ressources")
       # Release resources and close windows
       camera.StopGrabbing()
       # out.release()
       cv2.destroyAllWindows()
       camera.Close()
