import tkinter as tk
from tkinter import messagebox
import pandas as pd
import cv2
import threading
import queue
import time

# Load the Excel file into a DataFrame
excel_file = "qr_data.xlsx"

def load_data():
    try:
        print("Loading data from Excel...")
        df = pd.read_excel(excel_file)
        if "foodcount" not in df.columns:
            df["foodcount"] = 1  # Initialize foodcount if not present
        print("Data loaded successfully!")
        return df
    except FileNotFoundError:
        messagebox.showerror("Error", f"{excel_file} not found.")
        exit()

def save_data(df):
    print("Saving data to Excel...")
    df.to_excel(excel_file, index=False)
    print("Data saved successfully!")

def process_qr_data(qr_text, df):
    try:
        print(f"Processing QR Code: {qr_text}")
        teamid, hackode = map(int, qr_text.split(","))
        
        # Check if the QR code exists in the file
        row = df[(df["teamid"] == teamid) & (df["hackode"] == hackode)]
        if not row.empty:
            idx = row.index[0]
            # Check foodcount
            if df.at[idx, "foodcount"] > 0:
                df.at[idx, "foodcount"] -= 1  # Decrement food count
                save_data(df)  # Save updated data
                print(f"Food granted: Team ID {teamid}, Remaining Food Count: {df.at[idx, 'foodcount']}")
                return teamid, df.at[idx, "foodcount"]
            else:
                print(f"Food tokens exceeded for Team ID {teamid}")
                return teamid, -1  # Exceeded food count
        else:
            print(f"Invalid QR Code: No matching team found.")
            return None, None  # Invalid QR
    except ValueError:
        print(f"Invalid QR Code format: {qr_text}")
        return None, None  # Invalid QR Format


def start_multiple_cameras(ni):
    print(f"Starting {ni} cameras in parallel...")
    df = load_data()  # Load the Excel data
    threads = []  # To track threads

    for cam_id in range(1, ni + 1):
        print(f"Starting thread for camera {cam_id}...")

        # Create a new Tkinter window for each camera
        camera_window = tk.Toplevel()
        camera_window.title(f"Camera {cam_id}")
        camera_window.geometry("400x300")

        # Create labels for displaying team ID and food count
        teamid_text = StringVar()
        foodcount_text = StringVar()

        teamid_label = Label(camera_window, textvariable=teamid_text, font=("Arial", 14))
        teamid_label.pack(pady=20)

        foodcount_label = Label(camera_window, textvariable=foodcount_text, font=("Arial", 14))
        foodcount_label.pack(pady=20)

        # Initialize default values
        teamid_text.set("Team ID: N/A")
        foodcount_text.set("Remaining Food Count: N/A")

        # Start the thread for the camera
        thread = threading.Thread(
            target=start_camera,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
            args=(cam_id, df, camera_window, teamid_text, foodcount_text),
        )
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

def update_gui(root, result_queue, labels):
    while not result_queue.empty():
        cam_id, teamid, foodcount = result_queue.get()
        if teamid == "Error":
            labels[cam_id].config(text=f"Camera {cam_id}: Error accessing camera")
        elif teamid == "Invalid":
            labels[cam_id].config(text=f"Camera {cam_id}: Invalid QR")
        else:
            labels[cam_id].config(text=f"Camera {cam_id}: Team ID {teamid}, Food Count {foodcount}")

    root.after(100, update_gui, root, result_queue, labels)

def start_multiple_cameras(ni):
    df = load_data()
    result_queue = queue.Queue()
    labels = {}

    root = tk.Toplevel()
    root.title("Multi-Camera QR Scanner")

    for cam_id in range(1, ni + 1):
        label = tk.Label(root, text=f"Camera {cam_id}: Initializing...", font=("Arial", 14))
        label.pack(pady=10)
        labels[cam_id] = label

        thread = threading.Thread(target=start_camera, args=(cam_id, df, result_queue), daemon=True)
        thread.start()

    root.after(100, update_gui, root, result_queue, labels)

def main():
    ni = 2  # Number of cameras
    root = tk.Tk()
    root.title("Multi-Camera QR Scanner")
    root.geometry("300x200")

    label = tk.Label(root, text="Multi-Camera QR Scanner", font=("Arial", 14))
    label.pack(pady=20)

    start_button = tk.Button(root, text="Start Scanners", command=lambda: start_multiple_cameras(ni), font=("Arial", 12))
    start_button.pack(pady=10)

    exit_button = tk.Button(root, text="Exit", command=root.quit, font=("Arial", 12))
    exit_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    print("Starting the program...")
    main()
