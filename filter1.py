import numpy as np
import cv2
import face_recognition

class Camera:

    def resize_image(self, image, width):
        import PIL
        from PIL import Image

        face_width = width
        img = image
        wpercent = (face_width / img.shape[1])
        hsize = int(((img.shape[0]) * float(wpercent)))
        img = cv2.resize(img, (face_width, hsize))
        return img
    

    def main(self):
        cam = cv2.VideoCapture(0)
        
        helm = cv2.imread('j4helm.png', -1) 
        flame = cv2.imread('flame.png', -1)
        

        process = True
        
        while True:
            ret, frame = cam.read()
            frame = cv2.flip(frame, 1)

            face_landmarks_list = face_recognition.face_landmarks(frame)
            face_locations = face_recognition.face_locations(frame)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
            frame_h, frame_w, frame_c = frame.shape
            
            flame = cv2.resize(flame,(frame_w, frame_h))
            flame_h, flame_w, flame_c = flame.shape
            
            overlay = np.zeros((frame_h, frame_w, 4), dtype = 'uint8')
            if process is True:
                if len(face_locations) != 0:
                    for (top, right, bottom, left) in face_locations:
                        face_width = int((2 * (right - left)))
                        helm = self.resize_image(helm, face_width)
                        helm_h, helm_w, helm_c = helm.shape
                    
                        for i in range(helm_h):
                            for j in range(helm_w):
                                if helm[i,j][3] != 0:
                                    if (top + i - helm_h//2 - 25) >0 and (left + j -face_width//4)<=frame_w:
                                        frame[top + i - helm_h//2 - 25,left +  j - face_width//4] = helm[i, j]
                                    else:
                                        break
                        
                        for i in range(flame_h):
                            for j in range(flame_w):
                                if flame[i,j][3] != 0:
                                    overlay[i,j] = flame[i, j]
                                    
                        frame = cv2.addWeighted(overlay, 0.10, frame, 1, 0)
            	    
            cv2.imshow('filter', frame)
                     
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


        cam.release()
        cv2.destroyAllWindows()

camera = Camera()
camera.main()
