# SssssnakePicoPy
(Raspberry Pi Pico + SSD1306 OLED)

Este é um projeto em MicroPython que simula o jogo Snake com uma IA básica que busca a comida automaticamente, rodando em um Raspberry Pi Pico com um display OLED I2C SSD1306.

<div style="display: inline_block">
<img align="center" src="/demo.gif" alt="Demonstração"  width="40%">
</div>

## Funcionalidades

- Animação suave no display OLED
- IA básica: a cobra sempre tenta se mover em direção à comida
- Comida aleatória com proteção contra sobreposição na cobra
- Reinício automático em caso de colisão com o próprio corpo

## SNAKE VS SNAKE:
(snakeVSsnake.py)

<div style="display: inline_block">
<img align="center" src="/snakeVS.gif" alt="Demonstração"  width="40%">
</div>

#### DUAS COBRS DISPUTAM COMIDA E SOBREVIVÊNCIA!
1. Uma comida por vez → Se ambas as cobras vão até a comida, só a que alcançar primeiro ganha o ponto (e cresce).

2. Opção de ataque → Se uma cobra estiver próxima da outra, pode escolher se vai atrás da comida ou tenta morder a outra.

3. Evitar ser comida → Cada cobra tentará prever a posição da outra e fugir do "raio de ataque".

4. Punição ao ser mordida → Ao ser atacada, perde parte do corpo.

5. 10 rodadas → Após 10 turnos de surgimento de comida, o tamanho das cobras é comparado.

## Requisitos

- Raspberry Pi Pico
- Display OLED I2C SSD1306
- Firmware MicroPython instalado no Pico

## Ligações

| OLED       | Raspberry Pi Pico |
|------------|-------------------|
| VCC        | 3V3               |
| GND        | GND               |
| SDA        | GP16              |
| SCL        | GP17              |

## Rodando o projeto

1. Suba o `main.py` e a `ssd1306.py` (se necessário) para o Pico.
2. Reinicie o Pico.
3. O jogo começa automaticamente!