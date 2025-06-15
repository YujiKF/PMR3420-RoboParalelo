G21 ; Define unidades em milímetros
G90 ; Define posicionamento absoluto

; --- Seção de Homing (Movimento para Chave Fim de Curso) ---
; Este G-code move o efetuador para a posição da chave fim de curso.
; O controlador (Raspberry Pi) deve ser programado para mover o robô
; para X0 Y400 e parar o movimento quando a chave fim de curso for acionada,
; e então, internamente, ele "sabe" que está em X0 Y400.
G00 X0 Y400 F2000 ; Move rapidamente para a posição da chave fim de curso (X0, Y400)
                  ; Use uma velocidade razoável para o homing (F2000 mm/min)

; --- Movimento para o Ponto de Início da Primeira Figura (Circunferência) ---
; Após o homing, o robô está em X0 Y400.
; O centro da circunferência é X150 Y200, Raio 40mm.
; Vamos iniciar o círculo em X190 Y200 (centro + raio na direção X positiva)
G00 X190 Y200 F2000 ; Move rapidamente para o ponto de início da circunferência

; --- Trajetória da Circunferência (Sentido Horário - G02) ---
; Centro: X150 Y200, Raio: 40mm
; Ponto inicial: X190 Y200
; Ponto final: X190 Y200 (para um círculo completo)
; I e J são os offsets do centro do arco em relação ao ponto inicial.
; Centro (150, 200) - Ponto Inicial (190, 200) = (-40, 0)
G02 X190 Y200 I-40 J0 F1600 ; Desenha a circunferência horária (CW)
                           ; X190 Y200: Ponto final do arco (o mesmo que o inicial para um círculo completo)
                           ; I-40 J0: Offset do centro do arco (150,200) em relação ao ponto inicial (190,200)

; --- Movimento para o Ponto de Início da Segunda Figura (Triângulo) ---
; Ponto de início do triângulo. Vamos assumir um triângulo equilátero com 60mm de lado,
; centralizado abaixo do círculo.
; Assumindo um ponto de partida em X150 Y100 (abaixo do centro do círculo)
G00 X150 Y100 F2000 ; Move rapidamente para o ponto de início do triângulo

; --- Trajetória do Triângulo ---
; Assumindo:
; Ponto 1: X150 Y100 (base central)
; Ponto 2: X120 Y50 (canto inferior esquerdo, 30mm à esquerda, 50mm para baixo do P1)
; Ponto 3: X180 Y50 (canto inferior direito, 30mm à direita, 50mm para baixo do P1)
; Vamos começar no ponto central da base do triângulo (X150 Y100).
G01 F1100 ; Define a velocidade de avanço para o triângulo

G01 X120 Y50 ; Move para o primeiro vértice (inferior esquerdo)
G01 X180 Y50 ; Move para o segundo vértice (inferior direito)
G01 X150 Y100 ; Move de volta para o ponto inicial do triângulo (fecha o triângulo)

; --- Fim do Programa ---
M30 ; Fim do programa