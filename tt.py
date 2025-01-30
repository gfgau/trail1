import cv2

def list_active_cameras():
    for cam_id in range(5):  # Test up to 5 camera indices
        cap = cv2.VideoCapture(cam_id)
        if cap.isOpened():
            print(f"Camera {cam_id} is available.")
            cap.release()
        else:
            print(f"Camera {cam_id} is not available.")
    cv2.destroyAllWindows()

if __name__ == "__main__":
    list_active_cameras()
