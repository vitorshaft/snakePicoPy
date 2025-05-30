# SssssnakePicoPy
(Raspberry Pi Pico + SSD1306 OLED)

Este é um projeto em MicroPython que simula o jogo Snake com uma IA básica que busca a comida automaticamente, rodando em um Raspberry Pi Pico com um display OLED I2C SSD1306.

## Funcionalidades

- Animação suave no display OLED
- IA básica: a cobra sempre tenta se mover em direção à comida
- Comida aleatória com proteção contra sobreposição na cobra
- Reinício automático em caso de colisão com o próprio corpo

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