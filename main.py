from machine import Pin, I2C
import ssd1306
import utime
import urandom

# === CONFIGURAÇÕES ===
WIDTH = 128
HEIGHT = 64
GRID_SIZE = 4
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# === INICIALIZAÇÃO I2C e DISPLAY ===
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)
oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

# === ESTADO DO JOGO ===
snake = [(5, 5)]
direction = (1, 0)

def spawn_food():
    while True:
        x = urandom.getrandbits(6) % GRID_WIDTH
        y = urandom.getrandbits(6) % GRID_HEIGHT
        if (x, y) not in snake:
            return (x, y)

food = spawn_food()

# === FUNÇÕES ===

def draw():
    oled.fill(0)
    for segment in snake:
        x, y = segment
        oled.fill_rect(x*GRID_SIZE, y*GRID_SIZE, GRID_SIZE, GRID_SIZE, 1)
    fx, fy = food
    oled.fill_rect(fx*GRID_SIZE, fy*GRID_SIZE, GRID_SIZE, GRID_SIZE, 1)
    oled.show()

def move():
    global food
    head_x, head_y = snake[0]

    # --- Simples IA para buscar a comida ---
    dx, dy = direction
    fx, fy = food

    if fx > head_x:
        dx, dy = (1, 0)
    elif fx < head_x:
        dx, dy = (-1, 0)
    elif fy > head_y:
        dx, dy = (0, 1)
    elif fy < head_y:
        dx, dy = (0, -1)

    new_head = ((head_x + dx) % GRID_WIDTH, (head_y + dy) % GRID_HEIGHT)

    if new_head in snake:
        reset_game()
        return

    snake.insert(0, new_head)

    if new_head == food:
        food = spawn_food()
    else:
        snake.pop()

def reset_game():
    global snake, direction, food
    snake = [(5, 5)]
    direction = (1, 0)
    food = spawn_food()

# === LOOP PRINCIPAL ===
while True:
    move()
    draw()
    utime.sleep_ms(150)
