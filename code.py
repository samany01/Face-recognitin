from tkinter import *
import cv2
import face_recognition
from tkinter import messagebox


class MyWindow:
    def __init__(self, win):

        self.button1 = Button(win, image=btn_pic, borderwidth=0,
                              command=self.recognition)

        self.button1.place(x=45, y=600, height=122, width=510)

        win.bind('<Return>', self.recognition)

    def recognition(self, _event=None):
        global results
        me = face_recognition.load_image_file("me.jpg")
        me_rgb = cv2.cvtColor(me, cv2.COLOR_BGR2RGB)
        face_location = face_recognition.face_locations(me_rgb)
        me_face_encoding = face_recognition.face_encodings(me_rgb,
                                                           face_location, num_jitters=1)[0]

        known_face_encodings = [me_face_encoding]
        known_face_names = ["Samany"]

        # Get a reference to webcam
        video_capture = cv2.VideoCapture(0)

        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_frame = frame[:, :, ::-1]

            # Find all the faces in the current frame of video
            face_locations_test = face_recognition.face_locations(rgb_frame)
            face_encoding_test = face_recognition.face_encodings(rgb_frame,
                                                                 face_locations_test)

            # Display the results
            for (top, right, bottom, left), face_encoding in zip(face_locations_test, face_encoding_test):
                results = face_recognition.compare_faces(known_face_encodings, face_encoding,
                                                         tolerance=.6)

                if results[0]:
                    name = known_face_names[0]

                else:
                    name = "Unknown"

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 100), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom + 30), (right, bottom), (0, 255, 100), cv2.FILLED)
                font = cv2.FONT_HERSHEY_TRIPLEX
                cv2.putText(frame, name, (left + 8, bottom + 25), font, 1, (0, 0, 0), 1)
            # Display the resulting image
            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if results[0]:
                messagebox.showinfo("info", "Welcome home Samany")
                break

            else:
                messagebox.showinfo("info", "Unknown, please try again")
                break

        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    global results
    window = Tk()
    btn_pic = PhotoImage(file="Picture16.png")
    img = PhotoImage(file='Picture99.png')
    color = "#001736"
    Label(window, image=img).pack()
    dd = PhotoImage(file="910662.png")
    window.iconphoto(False, dd)
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    width = 601
    height = 725
    left = (screenWidth - width) / 2
    top = (screenHeight - height) / 2 - 50
    window.geometry("%dx%d+%d+%d" % (width, height, left, top))
    window.minsize(601, 725)
    window.maxsize(601, 725)
    window.title("Face_unlock")
    mywindow = MyWindow(window)
    window.mainloop
