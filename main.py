from PIL import Image, ImageTk
import tkinter as tk
import random

def move_bird_key(event):
    global x, y, game_over
    if not game_over:
        y -= 30
        canvas.coords(bird, x, y)

def move_bird():
    global x, y, game_over
    y += 5
    canvas.coords(bird, x, y)
    if y < 0 or y > window.winfo_height():
        game_end()

    if not game_over:
        window.after(50, move_bird)

def move_pipe():
    global score, game_over, speed
    canvas.move(pipe_top, -speed, 0)
    canvas.move(pipe_down, -speed, 0)
    if canvas.coords(pipe_down)[0] < -100:
        h = window.winfo_height()
        num = random.choice([i for i in range(160, h, 160)])
        canvas.coords(pipe_down, window.winfo_width(), num + 160)
        canvas.coords(pipe_top, window.winfo_width(), num - 900)

    if 145 < canvas.coords(pipe_down)[0] < 155:
        score += 1
        speed += 1
        canvas.itemconfigure(text_score, text=str(score))

    if canvas.bbox(bird) and (canvas.bbox(pipe_down) or canvas.bbox(pipe_top)):
        if canvas.bbox(bird)[0] < canvas.bbox(pipe_down)[2] and canvas.bbox(bird)[2] > canvas.bbox(pipe_down)[0]:
            if canvas.bbox(bird)[1] < canvas.bbox(pipe_top)[3] or canvas.bbox(bird)[3] > canvas.bbox(pipe_down)[1]:
                game_end()

    if not game_over:
        window.after(50, move_pipe)

def reset_game():
    global x, y, score, speed, game_over
    x = 150
    y = 300
    score = 0
    speed = 10
    canvas.coords(bird, x, y)
    canvas.coords(pipe_top, 1700, 550)
    canvas.coords(pipe_down, 1700, 550)
    canvas.itemconfigure(text_score, text="0")
    lbl_game_over.place_forget()
    bt_reset.place_forget()
    game_over = False
    move_bird()
    move_pipe()

def game_end():
    global game_over
    game_over = True
    lbl_game_over.place(relx=0.5, rely=0.5, anchor='center')
    bt_reset.place(relx=0.5, rely=0.7, anchor='center')

window = tk.Tk()
window.geometry('1000x600')
window.title('Adalberto Bird')

x = 350
y = 300
score = 0
speed = 10
game_over = False

img_bird = Image.open('imagenes/bird.png')
img_bird = img_bird.resize((50, 50), Image.LANCZOS)  # Ajusta el tamaño si es necesario
img_bird = ImageTk.PhotoImage(img_bird)

img_pipe_down = Image.open('imagenes/pipe.png')
img_pipe_top = img_pipe_down.rotate(180)
img_pipe_down = ImageTk.PhotoImage(img_pipe_down)
img_pipe_top = ImageTk.PhotoImage(img_pipe_top)

img_reset = Image.open('imagenes/images.jpeg')
img_reset = img_reset.resize((100, 50), Image.LANCZOS)  # Ajusta el tamaño si es necesario
img_reset = ImageTk.PhotoImage(img_reset)

canvas = tk.Canvas(window, highlightthickness=0, bg='#00bfff', bd=0)  # Sin borde
canvas.place(relwidth=1, relheight=1)

text_score = canvas.create_text(50, 50, text='0', fill='white', font=('3D Egoistism outline', 30))

bird = canvas.create_image(x, y, anchor='nw', image=img_bird)
pipe_top = canvas.create_image(1200, -550, anchor='nw', image=img_pipe_top)
pipe_down = canvas.create_image(1200, 550, anchor='nw', image=img_pipe_down)

window.bind("<space>", move_bird_key)

lbl_game_over = tk.Label(window, text='Game Over!', font=('D3 Egoistism outline', 30), fg='white', bg='#00bfff')
bt_reset = tk.Button(window, border=0, image=img_reset, activebackground='#00bfff', bg='#00bfff', command=reset_game)

window.after(50, move_bird)
window.after(50, move_pipe)

window.mainloop()
