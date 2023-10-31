import tkinter as tk
from PIL import Image, ImageTk
import random

class MemoryGame:
    def __init__(self, root, grid_size=4):
        self.root = root
        self.root.title("Jogo da Memória")
        self.grid_size = grid_size
        self.images = ["CR7.JPG", "Kaká.JPG", "LM10.JPG", "Pelé.JPG", "RF9.JPG", "RG9.JPG", "VamosPular.JPG", "VeioDoPó.JPG"]
        self.images *= (grid_size * grid_size // 2)
        random.shuffle(self.images)

        self.buttons = [[None for _ in range(grid_size)] for _ in range(grid_size)]
        self.selected_cards = []
        self.load_images()
        self.create_buttons()

    def load_images(self):
        self.image_objects = []
        for image_path in self.images:
            image = Image.open(image_path)
            image = image.resize((100, 100), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.image_objects.append(photo)

    def create_buttons(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                index = i * self.grid_size + j
                button = tk.Button(self.root, width=100, height=100, command=lambda idx=index: self.flip_card(idx))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

    def flip_card(self, index):
        i, j = divmod(index, self.grid_size)
        if (i, j) not in self.selected_cards and len(self.selected_cards) < 2:
            self.buttons[i][j].config(image=self.image_objects[index])
            self.selected_cards.append((i, j))
            if len(self.selected_cards) == 2:
                self.root.after(1000, self.check_match)
        elif (i, j) in self.selected_cards:
            self.selected_cards.remove((i, j))
            self.buttons[i][j].config(image="")

    def check_match(self):
        i1, j1 = self.selected_cards[0]
        i2, j2 = self.selected_cards[1]
        index1 = i1 * self.grid_size + j1
        index2 = i2 * self.grid_size + j2
        if self.images[index1] == self.images[index2]:
            self.buttons[i1][j1].config(state=tk.DISABLED)
            self.buttons[i2][j2].config(state=tk.DISABLED)
        else:
            self.buttons[i1][j1].config(image="")
            self.buttons[i2][j2].config(image="")
        self.selected_cards.clear()

root = tk.Tk()
game = MemoryGame(root, grid_size=4)
root.mainloop()
