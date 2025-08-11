
import cv2
from tkinter import Tk, Label, Button, filedialog, messagebox, Frame, Canvas
from PIL import Image, ImageTk

class SignatureVerificationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Signature Verification System")
        self.root.geometry("800x600")
        self.root.configure(bg="#0D1B2A")  # Dark blue background

        # Variables to store loaded images
        self.input_signature = None
        self.reference_signature = None
        self.input_path = ""
        self.reference_path = ""

        # Custom font styles
        header_font = ("Arial", 22, "bold")
        button_font = ("Arial", 14, "bold")
        result_font = ("Arial", 16, "italic")
        attribution_font = ("Arial", 10, "italic")

        # Title
        self.title_label = Label(
            root, text="Signature Verification System", font=header_font, bg="#0D1B2A", fg="#FFFFFF"
        )
        self.title_label.pack(pady=(20, 10))

        # Frames for images
        self.image_frame = Frame(root, bg="#0D1B2A")
        self.image_frame.pack(pady=20)

        # Input Signature Label
        self.input_label = Label(self.image_frame, text="Input Signature", bg="#0D1B2A", fg="#FFFFFF", font=button_font)
        self.input_label.grid(row=0, column=0, padx=20)

        # Reference Signature Label
        self.reference_label = Label(self.image_frame, text="Reference Signature", bg="#0D1B2A", fg="#FFFFFF", font=button_font)
        self.reference_label.grid(row=0, column=1, padx=20)

        # Canvas for images with borders
        self.input_canvas = Canvas(self.image_frame, bg="#1B263B", width=220, height=220, highlightthickness=2, highlightbackground="#E63946")
        self.input_canvas.grid(row=1, column=0, padx=20, pady=10)

        self.reference_canvas = Canvas(self.image_frame, bg="#1B263B", width=220, height=220, highlightthickness=2, highlightbackground="#E63946")
        self.reference_canvas.grid(row=1, column=1, padx=20, pady=10)

        # Load Input Signature Button
        self.input_button = Button(
            root, text="Load Input Signature", font=button_font,
            bg="#1F4068", fg="#FFFFFF", command=self.load_input_signature,
            activebackground="#162447", relief="raised", bd=4
        )
        self.input_button.pack(pady=10, ipadx=15, ipady=7)

        # Load Reference Signature Button
        self.reference_button = Button(
            root, text="Load Reference Signature", font=button_font,
            bg="#1F4068", fg="#FFFFFF", command=self.load_reference_signature,
            activebackground="#162447", relief="raised", bd=4
        )
        self.reference_button.pack(pady=10, ipadx=15, ipady=7)

        # Verify Signature Button
        self.verify_button = Button(
            root, text="Verify Signature", font=button_font,
            bg="#E63946", fg="#FFFFFF", command=self.verify_signature,
            activebackground="#B22234", relief="raised", bd=4
        )
        self.verify_button.pack(pady=10, ipadx=15, ipady=7)

        # Result Label
        self.result_label = Label(root, text="", font=result_font, bg="#0D1B2A", fg="#FFFFFF")
        self.result_label.pack(pady=20)

        # Attribution Label
        self.attribution_label = Label(
            root, text="Implemented by LAKSHMI HK & LIKITHA HM", font=attribution_font, bg="#0D1B2A", fg="#A8DADC"
        )
        self.attribution_label.pack(side="bottom", pady=10)

    def load_input_signature(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.input_path = file_path
            self.input_signature = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            if self.input_signature is not None and self.input_signature.size > 0:
                messagebox.showinfo("Info", "Input Signature Loaded Successfully")
                self.display_image(self.input_path, self.input_canvas)
            else:
                self.input_signature = None
                messagebox.showerror("Error", "Invalid image file. Please select a valid input signature.")

    def load_reference_signature(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.reference_path = file_path
            self.reference_signature = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            if self.reference_signature is not None and self.reference_signature.size > 0:
                messagebox.showinfo("Info", "Reference Signature Loaded Successfully")
                self.display_image(self.reference_path, self.reference_canvas)
            else:
                self.reference_signature = None
                messagebox.showerror("Error", "Invalid image file. Please select a valid reference signature.")

    def display_image(self, image_path, canvas):
        img = Image.open(image_path).resize((200, 200))
        img_tk = ImageTk.PhotoImage(img)
        canvas.create_image(110, 110, image=img_tk, anchor="center")
        canvas.image = img_tk

    def verify_signature(self):
        if self.input_signature is None or self.reference_signature is None:
            messagebox.showwarning("Warning", "Please load both signatures first.")
            return

        # Signature matching logic using FLANN-based matcher
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(self.input_signature, None)
        kp2, des2 = orb.detectAndCompute(self.reference_signature, None)

        if des1 is None or des2 is None:
            messagebox.showerror("Error", "Could not find keypoints in one or both images.")
            return

        index_params = dict(algorithm=6, table_number=6, key_size=12, multi_probe_level=1)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)

        matches = flann.knnMatch(des1, des2, k=2)

        # Apply Lowe's ratio test for filtering good matches
        good_matches = [m for m, n in matches if m.distance < 0.7 * n.distance]

        match_percentage = len(good_matches) / min(len(des1), len(des2)) * 100 if min(len(des1), len(des2)) > 0 else 0
        threshold = 20  # Match threshold for stricter verification

        if match_percentage > threshold:
            self.result_label.config(text="Signature Verified", fg="#4CAF50")
            messagebox.showinfo("Result", f"Signatures Match! Match Percentage: {match_percentage:.2f}%")
        else:
            self.result_label.config(text="Signature Not Verified", fg="#FF0000")
            messagebox.showinfo("Result", f"Signatures Do Not Match. Match Percentage: {match_percentage:.2f}%")

# Main application
if __name__ == "__main__":
    root = Tk()
    app = SignatureVerificationApp(root)
    root.mainloop()