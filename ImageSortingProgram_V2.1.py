import os
import json
import shutil
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk

CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            return config
    return {}


def save_config(config):
    config["text_to_replace"] = ";".join(config.get("text_to_replace", []))
    config["replace_with"] = ";".join(config.get("replace_with", []))
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)


class ConfigWindow:
    def __init__(self, root, on_start):
        self.root = root
        self.on_start = on_start

        # Load saved config
        self.config = load_config()

        self.config_window = tk.Toplevel(root)
        self.config_window.title("Configuration")

        # Bind the close window event (when the user clicks the "X" button)
        self.config_window.protocol("WM_DELETE_WINDOW", self.on_close)

        # Image folder
        tk.Label(self.config_window, text="Image Folder:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.image_folder_entry = tk.Entry(self.config_window, width=50)
        self.image_folder_entry.grid(row=0, column=1, padx=10, pady=5)
        self.image_folder_entry.insert(0, self.config.get("image_folder", ""))
        tk.Button(self.config_window, text="Browse", command=self.browse_image_folder).grid(row=0, column=2, padx=10, pady=5)

        # Preview folder
        tk.Label(self.config_window, text="Preview Folder:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.preview_folder_entry = tk.Entry(self.config_window, width=50)
        self.preview_folder_entry.grid(row=1, column=1, padx=10, pady=5)
        self.preview_folder_entry.insert(0, self.config.get("preview_folder", ""))
        tk.Button(self.config_window, text="Browse", command=self.browse_preview_folder).grid(row=1, column=2, padx=10, pady=5)

        # Sorted folder
        tk.Label(self.config_window, text="Sorted Folder (Optional):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.sorted_folder_entry = tk.Entry(self.config_window, width=50)
        self.sorted_folder_entry.grid(row=2, column=1, padx=10, pady=5)
        self.sorted_folder_entry.insert(0, self.config.get("sorted_folder", ""))
        tk.Button(self.config_window, text="Browse", command=self.browse_sorted_folder).grid(row=2, column=2, padx=10, pady=5)

        # Display size for images
        tk.Label(self.config_window, text="Display Size for Loaded Images (Height x Width):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.image_height_entry = tk.Entry(self.config_window, width=10)
        self.image_height_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.image_width_entry = tk.Entry(self.config_window, width=10)
        self.image_width_entry.grid(row=3, column=1, padx=10, pady=5, sticky="e")
        self.image_height_entry.insert(0, self.config.get("image_height", "800"))
        self.image_width_entry.insert(0, self.config.get("image_width", "600"))

        # Display size for preview images
        tk.Label(self.config_window, text="Display Size for Preview Images (Height x Width):").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.preview_height_entry = tk.Entry(self.config_window, width=10)
        self.preview_height_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        self.preview_width_entry = tk.Entry(self.config_window, width=10)
        self.preview_width_entry.grid(row=4, column=1, padx=10, pady=5, sticky="e")
        self.preview_height_entry.insert(0, self.config.get("preview_height", "400"))
        self.preview_width_entry.insert(0, self.config.get("preview_width", "300"))

        # Button names
        tk.Label(self.config_window, text="Button Names (semi-colon separated):").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.button_names_entry = tk.Entry(self.config_window, width=50)
        self.button_names_entry.grid(row=5, column=1, padx=10, pady=5)
        self.button_names_entry.insert(0, ",".join(self.config.get("button_names", ["1 - Good", "2 - Maybe", "3 - Bad", "4 - Concept", "5 - Clothing", "6 - Redo"])))

        # Text Replacement Configuration
        tk.Label(self.config_window, text="Text to Replace (semi-colon-separated):").grid(row=6, column=0, padx=10, pady=5,
                                                                                     sticky="w")
        self.text_to_replace_entry = tk.Entry(self.config_window, width=50)
        self.text_to_replace_entry.grid(row=6, column=1, padx=10, pady=5)
        self.text_to_replace_entry.insert(0, self.config.get("text_to_replace", ""))

        tk.Label(self.config_window, text="Replace With (semi-colon-separated):").grid(row=7, column=0, padx=10, pady=5,
                                                                                  sticky="w")
        self.replace_with_entry = tk.Entry(self.config_window, width=50)
        self.replace_with_entry.grid(row=7, column=1, padx=10, pady=5)
        self.replace_with_entry.insert(0, self.config.get("replace_with", ""))

        # Checkbox to hide preview
        self.hide_preview_var = tk.BooleanVar(value=self.config.get("hide_preview", False))
        tk.Checkbutton(self.config_window, text="Hide Preview", variable=self.hide_preview_var).grid(row=8, column=0, columnspan=3, padx=10, pady=5)

        # Start button
        tk.Button(self.config_window, text="Start Sorting", command=self.start_sorting).grid(row=8, column=1, pady=10)

    def on_close(self):
        """Callback to handle the case when the config window is closed without starting the sorting."""
        self.config_window.destroy()
        # Terminate the root window to close the entire application
        self.root.quit()

    def browse_image_folder(self):
        folder = filedialog.askdirectory(title="Select Image Folder")
        if folder:
            self.image_folder_entry.delete(0, tk.END)
            self.image_folder_entry.insert(0, folder)

    def browse_preview_folder(self):
        folder = filedialog.askdirectory(title="Select Preview Folder")
        if folder:
            self.preview_folder_entry.delete(0, tk.END)
            self.preview_folder_entry.insert(0, folder)

    def browse_sorted_folder(self):
        folder = filedialog.askdirectory(title="Select Sorted Folder")
        if folder:
            self.sorted_folder_entry.delete(0, tk.END)
            self.sorted_folder_entry.insert(0, folder)

    def start_sorting(self):
        image_folder = self.image_folder_entry.get()
        preview_folder = self.preview_folder_entry.get()
        # sorted_folder = self.sorted_folder_entry.get() or image_folder
        # Only save the sorted folder if it has been set by the user
        sorted_folder = self.sorted_folder_entry.get()
        if not sorted_folder:  # If user didn't set a sorted folder, default to empty
            sorted_folder = image_folder
        image_height = int(self.image_height_entry.get())
        image_width = int(self.image_width_entry.get())
        preview_height = int(self.preview_height_entry.get())
        preview_width = int(self.preview_width_entry.get())
        button_names = [name.strip() for name in self.button_names_entry.get().split(",")]

        '''
        text_to_replace = self.text_to_replace_entry.get("1.0", tk.END).strip()
        replace_with = self.replace_with_entry.get("1.0", tk.END).strip()
        '''

        text_to_replace = [item.strip() for item in self.text_to_replace_entry.get().split(";")]
        replace_with = [item.strip() for item in self.replace_with_entry.get().split(";")]

        # Include the hide preview setting
        hide_preview = self.hide_preview_var.get()

        # Save config
        config = {
            "image_folder": image_folder,
            "preview_folder": preview_folder,
            # "sorted_folder": sorted_folder,
            "sorted_folder": self.sorted_folder_entry.get() if self.sorted_folder_entry.get() else "",
            "image_height": image_height,
            "image_width": image_width,
            "preview_height": preview_height,
            "preview_width": preview_width,
            "button_names": button_names,
            "text_to_replace": text_to_replace,
            "replace_with": replace_with,
            "hide_preview": hide_preview  # Save checkbox state
        }
        save_config(config)

        self.config_window.destroy()
        self.on_start(image_folder, preview_folder, sorted_folder, image_height, image_width, preview_height, preview_width, button_names, text_to_replace, replace_with, hide_preview)


class ImageSorter:
    def __init__(self, root, image_folder, preview_folder, sorted_folder, image_height, image_width, preview_height, preview_width, button_names, text_to_replace, replace_with, hide_preview):
        self.root = root
        self.root.title("Image Sorter")

        self.image_index = 0
        self.image_list = []
        self.current_image_path = ""
        self.previous_image_path = ""
        self.previous_image_dest = ""

        self.image_folder = image_folder
        self.preview_folder = preview_folder
        self.sorted_folder = sorted_folder
        self.image_height = image_height
        self.image_width = image_width
        self.preview_height = preview_height
        self.preview_width = preview_width
        self.button_names = button_names
        self.text_to_replace = text_to_replace
        self.replace_with = replace_with
        self.hide_preview = hide_preview

        self.setup_gui()
        self.load_images()

    def setup_gui(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)

        self.image_label = tk.Label(self.main_frame)
        self.image_label.pack(side="left", padx=10, pady=10)

        if not self.hide_preview:
            self.preview_frame = tk.Frame(self.main_frame)
            self.preview_frame.pack(side="left", padx=10, pady=10)

            # Use grid layout to ensure no overlap
            self.preview_text_label = tk.Label(self.preview_frame, text="", font=("Helvetica", 16),
                                               wraplength=self.preview_width)
            self.preview_text_label.grid(row=0, column=0, pady=5)

            self.preview_image_label = tk.Label(self.preview_frame)
            self.preview_image_label.grid(row=1, column=0)

        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(side="right", padx=10, pady=10)

        self.buttons = []

        for i, text in enumerate(self.button_names):
            button = tk.Button(button_frame, text=text, command=lambda t=text: self.move_image(t))
            button.pack(pady=5)
            self.root.bind(str(i+1), lambda event, t=text: self.move_image(t))
            self.buttons.append(button)

        undo_button = tk.Button(button_frame, text="Undo", command=self.undo_move)
        undo_button.pack(pady=5)
        self.root.bind("z", lambda event: self.undo_move())

    def load_images(self):
        for file_name in os.listdir(self.image_folder):
            if file_name.lower().endswith(('.png', '.webp', '.jpg', '.jpeg', '.gif', '.bmp')):
                self.image_list.append(file_name)

        if self.image_list:
            self.display_image()
        else:
            tk.messagebox.showinfo("No images", "No images found in the selected folder.")
            self.root.destroy()

    def display_image(self):
        if self.image_index < len(self.image_list):
            self.current_image_path = os.path.join(self.image_folder, self.image_list[self.image_index])
            image_name = os.path.basename(self.current_image_path)

            # Update the window title
            self.root.title(f"Image Sorter - {image_name} ({self.image_index + 1}/{len(self.image_list)})")

            image = Image.open(self.current_image_path)
            image.thumbnail((self.image_width, self.image_height))
            photo = ImageTk.PhotoImage(image)

            self.image_label.config(image=photo)
            self.image_label.image = photo

            # Load and display the preview image
            if not self.hide_preview:
                preview_file_name = self.get_preview_image_name(image_name)
                print(preview_file_name)
                preview_path = os.path.join(self.preview_folder, preview_file_name)
                if os.path.exists(preview_path):
                    preview_image = Image.open(preview_path)
                    preview_image.thumbnail((self.preview_width, self.preview_height))
                    preview_photo = ImageTk.PhotoImage(preview_image)

                    # Set the size of the preview label
                    self.preview_image_label.config(width=self.preview_width, height=self.preview_height)

                    # Calculate the padding to center the image within the fixed-size label
                    pad_x = (self.preview_width - preview_photo.width()) // 2
                    pad_y = (self.preview_height - preview_photo.height()) // 2

                    # Set the image and apply padding to center it
                    self.preview_image_label.config(image=preview_photo, padx=pad_x, pady=pad_y)
                    self.preview_image_label.image = preview_photo  # Keep reference to prevent garbage collection

                    preview_text = preview_file_name.replace(".preview.png", "")
                    self.preview_text_label.config(text=preview_text)
                else:
                    # Create a blank image with the same dimensions as the preview pane
                    blank_image = Image.new('RGB', (self.preview_width, self.preview_height), color='white')
                    blank_photo = ImageTk.PhotoImage(blank_image)

                    # Set the blank image to the label
                    self.preview_image_label.config(image=blank_photo, padx=0, pady=0)
                    self.preview_image_label.image = blank_photo  # Keep a reference to prevent garbage collection

                    self.preview_text_label.config(text="No Preview Available")

    def get_preview_image_name(self, image_name):
        preview_image_name = image_name
        for to_replace, replace_with in zip(self.text_to_replace, self.replace_with):
            preview_image_name = preview_image_name.replace(to_replace, replace_with)
        return preview_image_name

    def move_image(self, button_name):
        if self.image_index < len(self.image_list):
            self.previous_image_path = self.current_image_path
            self.previous_image_dest = os.path.join(self.sorted_folder, button_name)
            os.makedirs(self.previous_image_dest, exist_ok=True)

            destination_path = os.path.join(self.previous_image_dest, os.path.basename(self.current_image_path))
            shutil.move(self.current_image_path, destination_path)

            self.image_index += 1
            if self.image_index < len(self.image_list):
                self.display_image()
            else:
                tk.messagebox.showinfo("Sorting Complete", "All images have been sorted.")
                self.root.quit()

    def undo_move(self):
        if self.previous_image_path and self.previous_image_dest:
            undo_destination_path = os.path.join(self.previous_image_dest, os.path.basename(self.previous_image_path))
            if os.path.exists(undo_destination_path):
                shutil.move(undo_destination_path, self.previous_image_path)
                self.previous_image_path = ""
                self.previous_image_dest = ""
                self.image_index -= 1
                if self.image_index >= 0:
                    self.display_image()
                else:
                    tk.messagebox.showinfo("Undo Complete", "No more images to undo.")
                    self.root.quit()

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main root window

    def start_sorting(image_folder, preview_folder, sorted_folder, image_height, image_width, preview_height, preview_width, button_names, text_to_replace, replace_with, hide_preview):
        root.deiconify()  # Show the main root window
        ImageSorter(root, image_folder, preview_folder, sorted_folder, image_height, image_width, preview_height, preview_width, button_names, text_to_replace, replace_with, hide_preview)
        root.mainloop()

    ConfigWindow(root, start_sorting)
    root.mainloop()

if __name__ == "__main__":
    main()
