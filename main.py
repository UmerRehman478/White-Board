import tkinter as tk
from tkinter.colorchooser import askcolor

class WhiteboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Whiteboard")

        # Initialize default color and canvas
        self.color = "black"
        self.brush_size = 5
        self.canvas = tk.Canvas(self.root, bg="white", width=700, height=600, bd=5, relief="ridge")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Bind mouse events
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

        # Create control panel
        self.create_controls()

        # Variables for smooth lines
        self.last_x, self.last_y = None, None

    def create_controls(self):
        controls_frame = tk.Frame(self.root, bg="white", pady=10)
        controls_frame.pack(side=tk.TOP, fill=tk.X)

        # Primary colors with labels
        primary_colors = [("Red", "red"), ("Blue", "blue"), ("Yellow", "yellow"), ("Black", "black")]
        for color_name, color in primary_colors:
            btn = tk.Button(
                controls_frame, bg=color, width=10, height=2,
                relief="groove", borderwidth=2, fg="black",
                text=color_name, font=("Arial", 15, "bold"),
                command=lambda c=color: self.change_color(c)
            )
            btn.pack(side=tk.LEFT, padx=5)

        # Custom color button
        custom_btn = tk.Button(
            controls_frame, text="Custom Color", width=12, height=2,
            bg="white", fg="black", relief="groove", borderwidth=2,
            font=("Arial", 15, "bold"),
            command=self.choose_color
        )
        custom_btn.pack(side=tk.LEFT, padx=5)

        # Clear button
        clear_btn = tk.Button(
            controls_frame, text="Clear", width=10, height=2,
            bg="white", fg="black", relief="groove", borderwidth=2,
            font=("Arial", 15, "bold"),
            command=self.clear_canvas
        )
        clear_btn.pack(side=tk.LEFT, padx=5)

        # Brush size slider with "Thickness" label
        brush_frame = tk.Frame(controls_frame, bg="white")
        brush_frame.pack(side=tk.LEFT, padx=10)
        
        brush_label = tk.Label(brush_frame, text="Thickness:", bg="white", fg="black", font=("Arial", 20, "bold"))
        brush_label.pack(side=tk.TOP)
        
        brush_slider = tk.Scale(
            brush_frame, from_=1, to=20, orient=tk.HORIZONTAL, bg="white",
            command=self.adjust_brush_size
        )
        brush_slider.set(self.brush_size)
        brush_slider.pack(side=tk.BOTTOM)

    def change_color(self, new_color):
        self.color = new_color

    def choose_color(self):
        color_code = askcolor(title="Choose a color")[1]
        if color_code:
            self.color = color_code

    def clear_canvas(self):
        self.canvas.delete("all")

    def adjust_brush_size(self, size):
        self.brush_size = int(size)

    def paint(self, event):
        if self.last_x and self.last_y:
            # Create smooth lines by connecting previous and current points
            self.canvas.create_line(
                self.last_x, self.last_y, event.x, event.y,
                fill=self.color, width=self.brush_size, capstyle=tk.ROUND, smooth=True
            )
        self.last_x, self.last_y = event.x, event.y

    def reset(self, event):
        # Reset the last_x and last_y for smooth drawing
        self.last_x, self.last_y = None, None

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = WhiteboardApp(root)
    root.mainloop()
