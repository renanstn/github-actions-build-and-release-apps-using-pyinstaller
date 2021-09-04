import tkinter as tk


class App:
    """
    This app is a simple GUI with a counter click button.
    """

    def __init__(self, root):
        self.click_counter = 0

        root.title("Test App")
        root.geometry("400x70")
        root.resizable(False, False)

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill='x')

        tk.Label(
            self.main_frame,
            text="Hello World!",

        ).pack(fill='x')

        tk.Button(
            self.main_frame,
            text="Click Me",
            width=10,
            command=self.click
        ).pack(fill='x')

        self.label_click_count = tk.Label(
            self.main_frame,
            text=f"{self.click_counter} clicks!"
        )
        self.label_click_count.pack(fill='x')

    def click(self):
        self.click_counter += 1
        self.update_click_counter_label()

    def update_click_counter_label(self):
        self.label_click_count['text'] = f"{self.click_counter} clicks!"


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
