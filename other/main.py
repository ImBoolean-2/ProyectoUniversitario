import customtkinter as ct
import cv2
import numpy as np
from PIL import Image, ImageTk
from tkinter import filedialog

class ImageProcessor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = cv2.imread(image_path)
        self.mask = None

    def remove_background(self):
        # Convert image to grayscale
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Apply threshold to segment out background
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Create mask
        self.mask = thresh

    def save_mask(self, file_path):
        if self.mask is not None:
            # Save mask as image
            cv2.imwrite(file_path, self.mask)

class App(ct.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1920x1080")
        self.title("Background Remover")

        # Create sidebar
        self.sidebar = ct.CTkFrame(self, width=200, height=600, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        # Create buttons
        self.upload_button = ct.CTkButton(self.sidebar, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=20)

        self.remove_background_button = ct.CTkButton(self.sidebar, text="Remove Background", command=self.remove_background)
        self.remove_background_button.pack(pady=20)

        self.save_button = ct.CTkButton(self.sidebar, text="Save Without Background", command=self.save_image)
        self.save_button.pack(pady=20)

        # Create image display
        self.image_display = ct.CTkLabel(self, text="", width=300, height=300)
        self.image_display.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Create mask display
        self.mask_display = ct.CTkLabel(self, text="", width=300, height=300)
        self.mask_display.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Initialize image variables
        self.image_path = ""
        self.image_processor = None
        self.image_pil_object = None
        self.mask_pil_object = None
        self.image_tk = None
        self.mask_tk = None

    def upload_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.image_processor = ImageProcessor(self.image_path)
            self.image_pil_object = Image.fromarray(cv2.cvtColor(self.image_processor.image, cv2.COLOR_BGR2RGB))
            self.image_tk = ImageTk.PhotoImage(self.image_pil_object)
            self.image_display.configure(text="", image=self.image_tk)
            self.image_display.image = self.image_tk  # keep a reference

    def remove_background(self):
        if self.image_processor:
            self.image_processor.remove_background()
            self.mask_pil_object = Image.fromarray(self.image_processor.mask)
            self.mask_tk = ImageTk.PhotoImage(self.mask_pil_object)
            self.mask_display.configure(text="", image=self.mask_tk)
            self.mask_display.image = self.mask_tk  # keep a reference

    def save_image(self):
        if self.image_processor:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
            if file_path:
                self.image_processor.save_mask(file_path)

                # Create RGB boxes
                rgb_boxes = []
                for i in range(3):
                    box = ct.CTkFrame(self, width=50, height=50, corner_radius=0, fg_color=self.get_rgb_color(i))
                    box.pack(side="right", fill="both", expand=True, padx=10, pady=10)
                    rgb_boxes.append(box)

    def get_rgb_color(self, channel):
        if channel == 0:
            return "#FF0000"  # Red
        elif channel == 1:
            return "#00FF00"  # Green
        else:
            return "#0000FF"  # Blue

if __name__ == "__main__":
    app = App()
    app.mainloop()