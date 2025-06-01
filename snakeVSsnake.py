from machine import Pin, I2C
import ssd1306
import urandom
import utime

'''
+++ AGORA DUAS COBRAS DISPUTAM COMIDA E SOBREVIVÊNCIA!!! +++

NOVAS REGRAS:
1. Uma comida por vez → Se ambas as cobras vão até a comida, só a que alcançar primeiro ganha o ponto (e cresce).

2. Opção de ataque → Se uma cobra estiver próxima da outra, pode escolher se vai atrás da comida ou tenta morder a outra.

.3 Evitar ser comida → Cada cobra tentará prever a posição da outra e fugir do "raio de ataque".

4. Punição ao ser mordida → Ao ser atacada, perde parte do corpo.

5. 10 rodadas → Após 10 turnos de surgimento de comida, o tamanho das cobras é comparado.
'''

# Configurações do display
WIDTH = 128
HEIGHT = 64
GRID_SIZE = 4 #cada bloco da cobra será 4x4 px
COLS = WIDTH//GRID_SIZE
ROWS = HEIGHT//GRID_SIZE

# inicializa I2C e display
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)
oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

class Snake:
    def __init__(self, x, y, name):
        self.body = [(x, y)]  # corpo da cobra como lista de blocos (x, y)
        self.dir = (0, 1)  # direção inicial: descendo
        self.grow_next = False
        self.name = name

    def head(self):
        return self.body[0]

    def move(self):
        hx, hy = self.head()
        dx, dy = self.dir
        new_head = ((hx + dx) % COLS, (hy + dy) % ROWS)
        self.body.insert(0, new_head)

        if self.grow_next:
            self.grow_next = False
        else:
            self.body.pop()  # remove o rabo (normal)

    def grow(self):
        self.grow_next = True

    def shrink(self):
        if len(self.body) > 1:
            self.body.pop()

    def set_direction(self, dx, dy):
        # Previne direção oposta instantânea
        if (-dx, -dy) != self.dir:
            self.dir = (dx, dy)

    def draw(self, oled, color=1):
        for x, y in self.body:
            oled.fill_rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE, color)

def generate_food(snake1, snake2):
    while True:
        x = urandom.getrandbits(6) % COLS
        y = urandom.getrandbits(6) % ROWS
        if (x, y) not in snake1.body and (x, y) not in snake2.body:
            return (x, y)

# INICIALIZAÇÕES
snake1 = Snake(3, 3, "Cobra 1")
snake2 = Snake(COLS - 4, ROWS - 4, "Cobra 2")
snake2.set_direction(0, -1)  # indo para cima

food = generate_food(snake1, snake2)
rodadas = 0

while rodadas < 10:
    oled.fill(0)

    # --- IA SIMPLES: VAI EM DIREÇÃO À COMIDA ---
    for snake in [snake1, snake2]:
        hx, hy = snake.head()
        fx, fy = food

        dx = 1 if fx > hx else -1 if fx < hx else 0
        dy = 1 if fy > hy else -1 if fy < hy else 0

        # Chance de escolher eixo horizontal ou vertical
        if urandom.getrandbits(1):
            snake.set_direction(dx, 0)
        else:
            snake.set_direction(0, dy)

        snake.move()

    # --- COLISÃO COM A COMIDA ---
    for snake in [snake1, snake2]:
        if snake.head() == food:
            snake.grow()
            food = generate_food(snake1, snake2)
            rodadas += 1
            break  # Só uma cobra pode comer por rodada

    # --- DESENHO ---
    snake1.draw(oled)
    snake2.draw(oled)
    fx, fy = food
    oled.fill_rect(fx * GRID_SIZE, fy * GRID_SIZE, GRID_SIZE, GRID_SIZE, 1)
    oled.show()
    utime.sleep_ms(100)

# --- RESULTADO FINAL ---
oled.fill(0)
oled.text("Jogo Encerrado", 10, 0)
oled.text("Cobra 1: {}".format(len(snake1.body)), 0, 30)
oled.text("Cobra 2: {}".format(len(snake2.body)), 0, 40)
if len(snake1.body) > len(snake2.body):
    oled.text("Venceu: Cobra 1", 0, 55)
elif len(snake1.body) < len(snake2.body):
    oled.text("Venceu: Cobra 2", 0, 55)
else:
    oled.text("Empate!", 30, 55)
oled.show()
