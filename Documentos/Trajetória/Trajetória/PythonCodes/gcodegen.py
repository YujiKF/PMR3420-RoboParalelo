import math

def gerar_gcode_circulo(cx, cy, raio, passos=100):
    gcode = ["G21 ; usar mm", "G90 ; coordenadas absolutas"]

    # Começa no ponto inicial do círculo (ângulo 0)
    x0 = cx + raio
    y0 = cy
    gcode.append(f"G00 X{round(x0,3)} Y{round(y0,3)}")

    # Traça o círculo com linhas (G01)
    for i in range(1, passos + 1):
        ang = 2 * math.pi * i / passos
        x = cx + raio * math.cos(ang)
        y = cy + raio * math.sin(ang)
        gcode.append(f"G01 X{round(x,3)} Y{round(y,3)}")
    return gcode

def gerar_gcode_triangulo(cx, cy, lado, tipo="equilatero"):
    gcode = ["G21 ; usar mm", "G90 ; coordenadas absolutas"]
    pontos = []
    if tipo == "equilatero":
        h = math.sqrt(3) / 2 * lado
        pontos = [
            (cx, cy + 2/3 * h),
            (cx - lado/2, cy - 1/3 * h),
            (cx + lado/2, cy - 1/3 * h),
            (cx, cy + 2/3 * h)
        ]
    elif tipo == "isosceles":
        h = math.sqrt(lado**2 - (lado/2)**2)
        pontos = [
            (cx, cy + h/2),
            (cx - lado/2, cy - h/2),
            (cx + lado/2, cy - h/2),
            (cx, cy + h/2)
        ]
    else:
        raise ValueError("Tipo de triângulo inválido")

    # Move ao primeiro ponto
    x0, y0 = pontos[0]
    gcode.append(f"G00 X{round(x0,3)} Y{round(y0,3)}")

    # Traça as linhas
    for p in pontos[1:]:
        gcode.append(f"G01 X{round(p[0],3)} Y{round(p[1],3)}")
    return gcode

def salvar_gcode(nome_arquivo, gcode):
    with open(nome_arquivo, 'w') as f:
        for linha in gcode:
            f.write(linha + "\n")
    print(f"G-code salvo em {nome_arquivo}")

def main():
    print("=== GCODE PARA CDPR PLANAR ===")
    largura = 30
    altura = 40
    # O centro do desenho está no meio da área de trabalho
    cx = 15.0
    cy = 20.0

    tipo = input("Trajetória (circulo ou triangulo)? ").strip().lower()

    if tipo == "circulo":
        raio = float(input("Raio (cm): "))
        gcode = gerar_gcode_circulo(cx, cy, raio)
    elif tipo == "triangulo":
        lado = float(input("Lado (cm): "))
        tipo_triangulo = input("Tipo (equilatero ou isosceles)? ").strip().lower()
        gcode = gerar_gcode_triangulo(cx, cy, lado, tipo_triangulo)
    else:
        print("Tipo inválido")
        return

    nome = input("Nome do arquivo GCODE (ex: traj.gcode): ")
    salvar_gcode(nome, gcode)

if __name__ == "__main__":
    main()
