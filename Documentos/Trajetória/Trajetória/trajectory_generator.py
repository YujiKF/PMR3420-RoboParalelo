# trajectory_generator.py

from parse_gcode import parse_gcode_file# Importa sua função de parsing
import math

class TrajectoryGenerator:
    def __init__(self, current_x=0.0, current_y=0.0, interpolation_step=0.1):
        """
        Inicializa o gerador de trajetórias.
        :param current_x: Posição X inicial do efetuador.
        :param current_y: Posição Y inicial do efetuador.
        :param interpolation_step: Tamanho do passo para interpolação (ex: 0.1 mm ou 0.1 unidades).
                                   Pontos serão gerados a cada 'interpolation_step' ao longo da trajetória.
        """
        self.current_x = current_x
        self.current_y = current_y
        self.trajectory_points = [] # Armazenará a sequência de pontos (x, y)

        # Usado para limitar o número de pontos gerados em G00 (movimento rápido)
        self.fast_move_points_count = 5
        self.interpolation_step = interpolation_step

    
    def generate_from_gcode_commands(self, gcode_commands):
        """
        Gera a trajetória a partir de uma lista de comandos G-Code parseados.
        :param gcode_commands: Lista de dicionários de comandos G-Code (saída do GCodeDataExtractor).
        """
        self.trajectory_points = [] # Resetar pontos para cada nova geração

        for command in gcode_commands:
            cmd_type = command.get('type')
            target_x = command.get('X')
            target_y = command.get('Y')

            if cmd_type == 'G00':
                # G00: Movimento rápido. Podemos gerar um número limitado de pontos
                # ou apenas o ponto final. Para visualização, vamos gerar alguns.
                self._add_linear_points(self.current_x, self.current_y, target_x, target_y, is_fast_move=True)
                self.current_x = target_x if target_x is not None else self.current_x
                self.current_y = target_y if target_y is not None else self.current_y
            elif cmd_type == 'G01':
                # G01: Interpolação Linear. Gerar pontos ao longo da linha.
                self._add_linear_points(self.current_x, self.current_y, target_x, target_y)
                self.current_x = target_x if target_x is not None else self.current_x
                self.current_y = target_y if target_y is not None else self.current_y
            elif cmd_type in ['G02', 'G03']:
                # G02/G03: Interpolação Circular.
                i_offset = command.get('I')
                j_offset = command.get('J')
                radius = command.get('R')

                # Certifique-se que X e Y de destino foram fornecidos para G02/G03
                if target_x is None or target_y is None:
                    print(f"Aviso: G{cmd_type[-1]} requer coordenadas X e Y de destino. Ignorando comando.")
                    continue

                if (i_offset is not None and j_offset is not None) and radius is None:
                    # Usando I e J
                    self._add_arc_points_ij(self.current_x, self.current_y, target_x, target_y, i_offset, j_offset, cmd_type)
                elif radius is not None and (i_offset is None and j_offset is None):
                    # Usando R (Raio)
                    self._add_arc_points_r(self.current_x, self.current_y, target_x, target_y, radius, cmd_type)
                else:
                    print(f"Aviso: Comando G{cmd_type[-1]} inválido. Forneça I/J ou R, mas não ambos ou nenhum. Ignorando.")
                    continue

                self.current_x = target_x
                self.current_y = target_y
            elif cmd_type == 'M30':
                # M30: Fim do programa. Não gera movimento.
                print("Fim do programa G-Code (M30) atingido.")
                break # Encerra a geração de trajetória
            else:
                print(f"Comando '{cmd_type}' não reconhecido ou suportado. Ignorando.")

        return self.trajectory_points

    def _add_linear_points(self, start_x, start_y, end_x, end_y, is_fast_move=False):
        """
        Adiciona pontos para um movimento linear (G00 ou G01).
        """
        # Se X ou Y de destino não foram fornecidos, usa a posição atual
        end_x = end_x if end_x is not None else start_x
        end_y = end_y if end_y is not None else start_y

        dx = end_x - start_x
        dy = end_y - start_y
        distance = math.sqrt(dx**2 + dy**2)

        if distance < 1e-6: # Se a distância é muito pequena, apenas adiciona o ponto final
            if not is_fast_move: # Para G01, garante que o ponto atual é o primeiro da linha
                self.trajectory_points.append({'x': start_x, 'y': start_y})
            self.trajectory_points.append({'x': end_x, 'y': end_y})
            return

        if is_fast_move:
            # Para G00, gera um número fixo de pontos para "visualização" do movimento rápido
            num_steps = self.fast_move_points_count
        else:
            # Para G01, gera pontos baseados no interpolation_step
            num_steps = max(2, int(distance / self.interpolation_step)) # Mínimo de 2 pontos (inicio e fim)

        for i in range(num_steps + 1):
            t = i / num_steps
            x = start_x + dx * t
            y = start_y + dy * t
            self.trajectory_points.append({'x': x, 'y': y})

    def _add_arc_points_ij(self, start_x, start_y, end_x, end_y, i_offset, j_offset, cmd_type):
        """
        Adiciona pontos para um movimento de arco usando I e J.
        I e J são offsets do centro do arco em relação ao ponto inicial.
        """
        center_x = start_x + i_offset
        center_y = start_y + j_offset

        # Raio do arco
        radius = math.sqrt(i_offset**2 + j_offset**2)

        # Ângulo inicial do ponto de partida em relação ao centro
        start_angle = math.atan2(start_y - center_y, start_x - center_x)
        # Ângulo final do ponto de destino em relação ao centro
        end_angle = math.atan2(end_y - center_y, end_x - center_x)

        # Ajusta os ângulos para garantir o sentido correto (horário ou anti-horário)
        if cmd_type == 'G02': # Horário
            if end_angle > start_angle:
                end_angle -= 2 * math.pi
        elif cmd_type == 'G03': # Anti-horário
            if end_angle < start_angle:
                end_angle += 2 * math.pi

        # Calcula o número de passos para a interpolação do arco
        # Baseado no comprimento do arco (raio * delta_angulo) e no interpolation_step
        angular_distance = abs(end_angle - start_angle)
        arc_length = radius * angular_distance
        num_steps = max(2, int(arc_length / self.interpolation_step))

        for i in range(num_steps + 1):
            t = i / num_steps
            current_angle = start_angle + (end_angle - start_angle) * t
            x = center_x + radius * math.cos(current_angle)
            y = center_y + radius * math.sin(current_angle)
            self.trajectory_points.append({'x': x, 'y': y})

    def _add_arc_points_r(self, start_x, start_y, end_x, end_y, radius, cmd_type):
        """
        Adiciona pontos para um movimento de arco usando o raio R.
        Esta implementação assume o caminho menor para o arco.
        Para lidar com múltiplos caminhos ou ambiguidade, G-code real usa
        parâmetros adicionais ou I/J. Aqui, simplificamos.
        """
        # Calcular distância entre ponto inicial e final
        chord_dist = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)

        # Se o raio é muito pequeno ou a distância é maior que o diâmetro (arco impossível)
        if 2 * radius < chord_dist - 1e-6: # pequena tolerância para floating point
            print(f"Aviso: Raio {radius} é muito pequeno para alcançar ({start_x},{start_y}) a ({end_x},{end_y}). Ignorando arco.")
            return
        if 2 * radius < chord_dist: # Caso limite onde raio é exatamente metade da distância
            # Tratar como linha reta para evitar divisão por zero ou problemas de float
            self._add_linear_points(start_x, start_y, end_x, end_y)
            return

        # Calcular o ponto médio da corda
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2

        # Distância do centro do arco ao ponto médio da corda
        h = math.sqrt(radius**2 - (chord_dist / 2)**2)

        # Encontrar os dois possíveis centros (um para cada lado da corda)
        # Vetor normalizado da corda
        nx = (end_y - start_y) / chord_dist
        ny = -(end_x - start_x) / chord_dist

        # Calcular os dois centros possíveis
        center1_x = mid_x + h * nx
        center1_y = mid_y + h * ny
        center2_x = mid_x - h * nx
        center2_y = mid_y - h * ny

        # Escolher o centro correto dependendo do G-code (G02/G03) e do caminho
        # Esta parte é a mais "complicada" e pode exigir ajustes.
        # Por simplicidade, vamos escolher o centro que produz o arco mais "direto".
        # O G-Code real normalmente usa I, J ou um parâmetro adicional para a escolha do caminho.
        # Para um R-code simples, ele geralmente significa o caminho menor.
        # Aqui, vamos precisar decidir qual centro usar para G02/G03
        # O ANTLR 2025.pdf não especifica como lidar com R-code e escolha do centro.
        # Vou escolher o centro que faz o arco mais "direto" baseado no sentido.

        # Uma abordagem comum para G02/G03 com R é que o centro correto é
        # aquele que permite o movimento no sentido especificado.
        # Para simplificar aqui, vamos usar a heurística do menor arco.

        # Se o raio R for positivo, significa o arco menor. Se negativo, o arco maior.
        # Mas nossa gramática ANTLR permite apenas R positivo.
        # Vamos assumir o arco menor para R positivo e precisamos escolher o centro.

        # Vetor do start ao end
        v_sx = end_x - start_x
        v_sy = end_y - start_y

        # Vetor do start a cada centro
        v_sc1x = center1_x - start_x
        v_sc1y = center1_y - start_y
        v_sc2x = center2_x - start_x
        v_sc2y = center2_y - start_y

        # Produto cruzado 2D (vx*wy - vy*wx) para determinar a "orientação"
        cross_product1 = v_sx * v_sc1y - v_sy * v_sc1x
        cross_product2 = v_sx * v_sc2y - v_sy * v_sc2x

        chosen_center_x, chosen_center_y = 0,0

        if cmd_type == 'G02': # Horário
            # O sentido horário geralmente tem o ponto final "à direita" do vetor (start -> centro)
            # ou o cross_product (start_vec x end_vec) deve ser negativo.
            # Aqui, para R, o centro é escolhido para que a corda forme o lado "esquerdo" ou "direito" do arco
            if cross_product1 < 0: # Para um G02, o centro deve estar à direita da linha start->end
                chosen_center_x, chosen_center_y = center1_x, center1_y
            else:
                chosen_center_x, chosen_center_y = center2_x, center2_y
        elif cmd_type == 'G03': # Anti-horário
            # O sentido anti-horário geralmente tem o ponto final "à esquerda" do vetor (start -> centro)
            # ou o cross_product (start_vec x end_vec) deve ser positivo.
            if cross_product1 > 0: # Para um G03, o centro deve estar à esquerda da linha start->end
                chosen_center_x, chosen_center_y = center1_x, center1_y
            else:
                chosen_center_x, chosen_center_y = center2_x, center2_y

        self._add_arc_points_ij(start_x, start_y, end_x, end_y,
                                chosen_center_x - start_x, chosen_center_y - start_y,
                                cmd_type)

# Exemplo de uso:
if __name__ == "__main__":
    # Crie um arquivo de exemplo de G-Code para testar
    # Salve este conteúdo como 'exemplo.gcode' no mesmo diretório
    gcode_example_content = """
G00 X15.0 Y28.66
G01 X7.5 Y15.67
G01 X22.5 Y15.67
G01 X15.0 Y28.66
"""
    with open("exemplo.gcode", "w") as f:
        f.write(gcode_example_content.strip()) # .strip() para remover quebras de linha extras

    print("Conteúdo do exemplo.gcode:")
    print(gcode_example_content)
    print("-" * 30)

    # 1. Parsear o G-Code usando sua função anterior
    parsed_commands = parse_gcode_file("exemplo.gcode")

    if parsed_commands:
        print("\nComandos G-Code parseados:")
        for command in parsed_commands:
            print(command)
        print("-" * 30)

        # 2. Gerar a trajetória
        # Ajuste a posição inicial se necessário (aqui começa em 0,0)
        trajectory_gen = TrajectoryGenerator(current_x=0.0, current_y=0.0, interpolation_step=0.5)
        generated_points = trajectory_gen.generate_from_gcode_commands(parsed_commands)

        print(f"\nPontos da trajetória gerados ({len(generated_points)} pontos):")
        # Imprime apenas os primeiros e últimos pontos para não sobrecarregar
        for i, point in enumerate(generated_points):
            if i < 5 or i > len(generated_points) - 6:
                print(f"  Ponto {i+1}: X={point['x']:.3f}, Y={point['y']:.3f}")
            elif i == 5 and len(generated_points) > 10:
                print("  ...")
        print("-" * 30)

        # Opcional: Visualizar a trajetória (requer matplotlib)
        try:
            import matplotlib.pyplot as plt
            x_coords = [p['x'] for p in generated_points]
            y_coords = [p['y'] for p in generated_points]

            plt.figure(figsize=(8, 8))
            plt.plot(x_coords, y_coords, 'b-o', markersize=2, linewidth=0.5)
            plt.plot(x_coords[0], y_coords[0], 'go', markersize=8, label='Início') # Ponto inicial
            plt.plot(x_coords[-1], y_coords[-1], 'ro', markersize=8, label='Fim')   # Ponto final
            plt.xlabel("Coordenada X")
            plt.ylabel("Coordenada Y")
            plt.title("Trajetória do Robô (G-Code)")
            plt.grid(True)
            plt.axis('equal') # Garante que a escala dos eixos X e Y é a mesma
            plt.legend()
            plt.show()
        except ImportError:
            print("\nMatplotlib não está instalado. Para visualizar a trajetória, execute 'pip install matplotlib'.")
