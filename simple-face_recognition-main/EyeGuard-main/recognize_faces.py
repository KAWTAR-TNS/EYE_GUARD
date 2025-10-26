import cv2
import face_recognition
import numpy as np
import os
import csv
from datetime import datetime

def load_known_faces(known_faces_dir):
    known_face_encodings = []
    known_face_names = []

    for filename in os.listdir(known_faces_dir):
        image_path = os.path.join(known_faces_dir, filename)
        if os.path.isfile(image_path):
            name = os.path.splitext(filename)[0]
            face_image = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(face_image)[0]
            known_face_encodings.append(face_encoding)
            known_face_names.append(name)

    return known_face_encodings, known_face_names

def recognize_faces(video_capture, known_face_encodings, known_face_names):
    # Capture current date
    now = datetime.now()
    concurrent_date = now.strftime("%Y-%m-%d")
    print("Date of detection:", concurrent_date)

    # Open CSV file for writing
    with open(concurrent_date + '.csv', 'w+', newline='') as f:
        lnwriter = csv.writer(f)

        process_this_frame = True

        while True:
            ret, frame = video_capture.read()

            if process_this_frame:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                    else:
                        print("Intruder Detected")
                        # Capture current time
                        current_time = now.strftime("%H-%M-%S")
                        print("Time of detection:", current_time)

                        # Write to CSV file
                        lnwriter.writerow([name, current_time])

                    face_names.append(name)

            process_this_frame = not process_this_frame

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_capture = cv2.VideoCapture(0)
    known_faces_dir = "authorized_faces"
    known_face_encodings, known_face_names = load_known_faces(known_faces_dir)
    recognize_faces(video_capture, known_face_encodings, known_face_names)
