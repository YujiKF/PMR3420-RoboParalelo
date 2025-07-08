import tkinter as tk
from tkinter import filedialog, messagebox
import threading # IMPORTE O MÓDULO THREADING PARA OPERAÇÕES NÃO BLOQUEANTES
import time      # IMPORTE TIME PARA PEQUENOS ATRASOS

# Importar suas funções de parsing e geração de trajetória
from parse_gcode import parse_gcode_file
from trajectory_generator import TrajectoryGenerator

# IMPORTA A SUA CLASSE ModbusHandler
from modbus_handler import ModbusHandler

# --- Constantes Modbus (ajuste conforme o seu setup) ---
MODBUS_PORT = 'COM10'       # <--- AJUSTE A PORTA SERIAL DO SEU FTDI/PICO W
MODBUS_BAUDRATE = 115200   # <--- AJUSTE PARA A BAUD RATE CONFIGURADA NO PICO W
MODBUS_SLAVE_ID = 1        # ID do seu Raspberry Pi Pico W
MODBUS_REG_X_POS = 0x0000  # Endereço do registrador para a coordenada X (Pico W)
MODBUS_REG_Y_POS = 0x0001  # Endereço do registrador para a coordenada Y (Pico W)
MODBUS_REG_CONTROL_FLAG = 0x0004 # Um flag para o Master sinalizar "novo ponto" ou "processar"

# Escalonamento para Modbus (DEVE SER O MESMO DO SEU CÓDIGO NO PICO W)
SCALING_FACTOR = 10.0


class RobotControlGUI:
    def __init__(self, master):
        self.master = master
        master.title("Controle de Robô Paralelo")

        self.trajectory_points = []
        self.current_x = 0.0 # Posição X atual do efetuador (mantida pela GUI)
        self.current_y = 0.0 # Posição Y atual do efetuador

        # INSTANCIA O SEU ModbusHandler
        self.modbus_handler = ModbusHandler(
            port=MODBUS_PORT,
            baudrate=MODBUS_BAUDRATE,
            slave_id=MODBUS_SLAVE_ID
        )

        # --- Frames para organização ---
        self.conn_frame = tk.LabelFrame(master, text="Conexão Modbus")
        self.conn_frame.pack(pady=5, padx=10, fill="x")

        self.file_frame = tk.LabelFrame(master, text="Arquivo G-code")
        self.file_frame.pack(pady=5, padx=10, fill="x")

        self.control_frame = tk.LabelFrame(master, text="Controles do Robô")
        self.control_frame.pack(pady=5, padx=10, fill="x")

        self.log_frame = tk.LabelFrame(master, text="Log de Status")
        self.log_frame.pack(pady=5, padx=10, fill="both", expand=True)

        # --- Componentes do Frame de Conexão ---
        self.btn_connect = tk.Button(self.conn_frame, text="Conectar Modbus", command=self.connect_modbus_gui)
        self.btn_connect.pack(side="left", padx=5, pady=5)
        self.btn_disconnect = tk.Button(self.conn_frame, text="Desconectar Modbus", command=self.disconnect_modbus_gui, state=tk.DISABLED)
        self.btn_disconnect.pack(side="left", padx=5, pady=5)
        self.status_label = tk.Label(self.conn_frame, text="Status: Desconectado", fg="red")
        self.status_label.pack(side="left", padx=10)

        # --- Componentes do Frame de Arquivo ---
        self.btn_open_gcode = tk.Button(self.file_frame, text="Abrir G-code", command=self.open_gcode_file)
        self.btn_open_gcode.pack(side="left", padx=5, pady=5)

        # O botão Enviar Trajetória é desabilitado até um G-code ser carregado E Modbus conectado
        self.btn_send_trajectory = tk.Button(self.file_frame, text="Enviar Trajetória", command=self.send_trajectory_thread, state=tk.DISABLED)
        self.btn_send_trajectory.pack(side="left", padx=5, pady=5)

        # --- Componentes do Frame de Controle ---
        self.manual_controls_label = tk.Label(self.control_frame, text="Movimento Manual (Passo ~1mm):")
        self.manual_controls_label.grid(row=0, column=0, columnspan=3, pady=5)

        # Botões de movimento manual, desabilitados por padrão
        self.btn_up = tk.Button(self.control_frame, text="Cima (+Y)", command=lambda: self.move_manual(0, 1), state=tk.DISABLED)
        self.btn_up.grid(row=1, column=1, padx=5, pady=5)

        self.btn_left = tk.Button(self.control_frame, text="Esquerda (-X)", command=lambda: self.move_manual(-1, 0), state=tk.DISABLED)
        self.btn_left.grid(row=2, column=0, padx=5, pady=5)

        self.btn_right = tk.Button(self.control_frame, text="Direita (+X)", command=lambda: self.move_manual(1, 0), state=tk.DISABLED)
        self.btn_right.grid(row=2, column=2, padx=5, pady=5)

        self.btn_down = tk.Button(self.control_frame, text="Baixo (-Y)", command=lambda: self.move_manual(0, -1), state=tk.DISABLED)
        self.btn_down.grid(row=3, column=1, padx=5, pady=5)

        # --- Componentes do Log ---
        self.log_text = tk.Text(self.log_frame, height=10, state=tk.DISABLED)
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Ao fechar a janela, garantir desconexão
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Atualiza o estado inicial dos botões
        self.update_button_states()

    def log_message(self, message):
        """Adiciona uma mensagem ao log da GUI e atualiza a interface."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END) # Auto-scroll para o final
        self.log_text.config(state=tk.DISABLED)
        self.master.update_idletasks() # Força a atualização da GUI

    def update_button_states(self):
        """Atualiza o estado (habilitado/desabilitado) dos botões da GUI."""
        is_connected = self.modbus_handler.is_connected
        has_trajectory = bool(self.trajectory_points)

        self.btn_connect.config(state=tk.DISABLED if is_connected else tk.NORMAL)
        self.btn_disconnect.config(state=tk.NORMAL if is_connected else tk.DISABLED)
        self.status_label.config(text="Status: Conectado" if is_connected else "Status: Desconectado",
                                 fg="green" if is_connected else "red")

        self.btn_send_trajectory.config(state=tk.NORMAL if is_connected and has_trajectory else tk.DISABLED)

        manual_buttons_state = tk.NORMAL if is_connected else tk.DISABLED
        self.btn_up.config(state=manual_buttons_state)
        self.btn_down.config(state=manual_buttons_state)
        self.btn_left.config(state=manual_buttons_state)
        self.btn_right.config(state=manual_buttons_state)


    def connect_modbus_gui(self):
        """Tenta conectar ao Modbus e atualiza o status da GUI."""
        self.log_message(f"Tentando conectar Modbus à {MODBUS_PORT}...")
        if self.modbus_handler.connect():
            self.log_message("Modbus conectado com sucesso!")
        else:
            self.log_message("Falha ao conectar Modbus.")
        self.update_button_states()

    def disconnect_modbus_gui(self):
        """Desconecta do Modbus e atualiza o status da GUI."""
        self.modbus_handler.disconnect()
        self.log_message("Modbus desconectado.")
        self.update_button_states()

    def on_closing(self):
        """Chamado ao fechar a janela, garante a desconexão do Modbus."""
        self.disconnect_modbus_gui()
        self.master.destroy()

    def open_gcode_file(self):
        """Abre um diálogo para selecionar um arquivo G-code, faz o parsing e gera a trajetória."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Arquivos G-code", "*.gcode"), ("Todos os arquivos", "*.*")]
        )
        if file_path:
            self.log_message(f"Abrindo arquivo: {file_path}")
            try:
                parsed_commands = parse_gcode_file(file_path)
                if parsed_commands:
                    self.log_message(f"G-code parseado. {len(parsed_commands)} comandos encontrados.")
                    # Passa a posição atual para o gerador de trajetória.
                    # Isso é importante para que as trajetórias G02/G03 comecem do ponto correto.
                    generator = TrajectoryGenerator(
                        current_x=self.current_x,
                        current_y=self.current_y
                    )
                    self.trajectory_points = generator.generate_from_gcode_commands(parsed_commands)
                    self.log_message(f"Trajetória gerada: {len(self.trajectory_points)} pontos.")
                    messagebox.showinfo("Sucesso", "Arquivo G-code carregado e trajetória gerada.")
                else:
                    self.log_message("Erro ao parsear G-code ou nenhum comando encontrado.")
                    self.trajectory_points = [] # Limpa a trajetória se houver erro
            except Exception as e:
                self.log_message(f"Erro no processamento do G-code: {e}")
                messagebox.showerror("Erro", f"Erro no processamento do G-code: {e}")
            finally:
                self.update_button_states() # Sempre atualiza o estado dos botões

        else:
            self.log_message("Seleção de arquivo cancelada.")
            self.update_button_states()

    def send_trajectory_thread(self):
        """Inicia o envio da trajetória em uma thread separada para não travar a GUI."""
        if not self.trajectory_points:
            self.log_message("Nenhum ponto de trajetória para enviar.")
            return

        if not self.modbus_handler.is_connected:
            self.log_message("Modbus não conectado. Não é possível enviar trajetória.")
            messagebox.showwarning("Aviso", "Conecte-se ao Modbus primeiro.")
            return

        # Desabilita botões enquanto a trajetória é enviada
        self.btn_send_trajectory.config(state=tk.DISABLED)
        self.btn_open_gcode.config(state=tk.DISABLED)
        self.btn_up.config(state=tk.DISABLED)
        self.btn_down.config(state=tk.DISABLED)
        self.btn_left.config(state=tk.DISABLED)
        self.btn_right.config(state=tk.DISABLED)
        self.btn_disconnect.config(state=tk.DISABLED) # Desabilita desconectar durante o envio

        self.log_message("Iniciando thread de envio da trajetória...")
        # Cria e inicia a nova thread
        thread = threading.Thread(target=self._send_trajectory_worker)
        thread.daemon = True # Permite que o programa principal saia mesmo se a thread estiver rodando
        thread.start()

    # def _send_trajectory_worker(self):
    #     """Função que será executada na thread para enviar a trajetória via Modbus."""
    #     self.log_message(f"Enviando {len(self.trajectory_points)} pontos da trajetória via Modbus...")
    #     try:
    #         for i, point in enumerate(self.trajectory_points):
    #             # Escalonar as coordenadas X e Y para inteiros antes de enviar via Modbus
    #             x_scaled = int(point['x'] * SCALING_FACTOR)
    #             y_scaled = int(point['y'] * SCALING_FACTOR)

    #             # Usa o método write_multiple_registers do seu ModbusHandler
    #             # Assume que o Pico W espera X no reg 0x0000 e Y no reg 0x0001
    #             # success = self.modbus_handler.write_multiple_registers(
    #             #     address=MODBUS_REG_X_POS,
    #             #     values=[x_scaled, y_scaled]
    #             # )
    #             if i = 0:
    #             success = self.modbus_handler.write_single_register(
    #             address=MODBUS_REG_X_POS,
    #             values=[x_scaled, y_scaled]
    #             )
                
    #             if success:
    #                 # Atualiza a posição atual da GUI apenas se o envio for bem-sucedido
    #                 self.current_x = point['x']
    #                 self.current_y = point['y']
    #                 self.log_message(f"  Ponto {i+1}/{len(self.trajectory_points)} enviado: X={self.current_x:.3f}, Y={self.current_y:.3f}")
    #             else:
    #                 self.log_message(f"  Falha ao enviar Ponto {i+1}. Abortando trajetória.")
    #                 messagebox.showerror("Erro de Envio", "Falha na comunicação Modbus durante a trajetória. Verifique o Pico W.")
    #                 break # Aborta o envio em caso de falha

    #             # Pequeno atraso para não sobrecarregar o Pico W e permitir processamento
    #             time.sleep(0.1) # Atraso de 100ms entre cada ponto enviado

    #         else: # Este bloco é executado se o loop `for` for concluído (sem `break`)
    #             self.log_message("Envio da trajetória concluído!")
    #             messagebox.showinfo("Sucesso", "Trajetória enviada com sucesso!")

    #     except Exception as e:
    #         self.log_message(f"Erro inesperado durante o envio da trajetória: {e}")
    #         messagebox.showerror("Erro", f"Erro inesperado no envio: {e}")
    #     finally:
    #         # Reabilita os botões após o término (ou falha) na thread principal da GUI
    #         self.master.after(100, self.update_button_states) # Agenda a chamada para a thread principal da GUI

    #usando single_register em vez de multiple
    def _send_trajectory_worker(self):
        """Função que será executada na thread para enviar a trajetória via Modbus."""
        self.log_message(f"Enviando {len(self.trajectory_points)} pontos da trajetória via Modbus...")
        try:
            for i, point in enumerate(self.trajectory_points):
                # Escalonar as coordenadas X e Y para inteiros antes de enviar via Modbus
                x_scaled = int(point['x'] * SCALING_FACTOR)
                y_scaled = int(point['y'] * SCALING_FACTOR)

                # --- Utilizando write_single_register para X ---
                success_x = self.modbus_handler.write_single_register(
                    address=MODBUS_REG_X_POS,
                    value=x_scaled
                )

                # --- Utilizando write_single_register para Y ---
                success_y = self.modbus_handler.write_single_register(
                    address=MODBUS_REG_Y_POS,
                    value=y_scaled
                )

                success_flag = self.modbus_handler.write_single_register(
                    MODBUS_REG_CONTROL_FLAG, 
                    1
                )
                

                # Verifica se AMBAS as escritas foram bem-sucedidas
                if success_x and success_y and success_flag:
                    # Atualiza a posição atual da GUI apenas se o envio for bem-sucedido
                    self.current_x = point['x']
                    self.current_y = point['y']
                    self.log_message(f"  Ponto {i+1}/{len(self.trajectory_points)} enviado: X={self.current_x:.3f}, Y={self.current_y:.3f}")
                else:
                    self.log_message(f"  Falha ao enviar Ponto {i+1}. Abortando trajetória.")
                    messagebox.showerror("Erro de Envio", "Falha na comunicação Modbus durante a trajetória. Verifique o Pico W.")
                    break # Aborta o envio em caso de falha

                # Pequeno atraso para não sobrecarregar o Pico W e permitir processamento
                time.sleep(1) # Atraso de 100ms entre cada ponto enviado

            else: # Este bloco é executado se o loop `for` for concluído (sem `break`)
                self.log_message("Envio da trajetória concluído!")
                messagebox.showinfo("Sucesso", "Trajetória enviada com sucesso!")

        except Exception as e:
            self.log_message(f"Erro inesperado durante o envio da trajetória: {e}")
            messagebox.showerror("Erro", f"Erro inesperado no envio: {e}")
        finally:
            # Reabilita os botões após o término (ou falha) na thread principal da GUI
            self.master.after(100, self.update_button_states) # Agenda a chamada para a thread principal da GUI


    def move_manual(self, dx_factor, dy_factor):
        """
        Calcula a nova posição alvo para o movimento manual e envia via Modbus.
        dx_factor e dy_factor são -1, 0 ou 1, indicando a direção.
        """
        if not self.modbus_handler.is_connected:
            self.log_message("Modbus não conectado para controle manual.")
            messagebox.showwarning("Aviso", "Conecte-se ao Modbus primeiro.")
            return

        # Define o passo do movimento manual
        manual_step_mm = 1.0 # Por exemplo, 1 mm por clique para maior precisão

        # Calcula a nova posição alvo (acumulativa a partir da posição atual)
        target_x = self.current_x + (dx_factor * manual_step_mm)
        target_y = self.current_y + (dy_factor * manual_step_mm)

        # Opcional: Adicione limites para X e Y se o robô tiver uma área de trabalho definida
        # Ex:
        # max_x, min_x = 100.0, -100.0
        # max_y, min_y = 100.0, -100.0
        # target_x = max(min_x, min(max_x, target_x))
        # target_y = max(min_y, min(max_y, target_y))

        x_scaled = int(target_x * SCALING_FACTOR)
        y_scaled = int(target_y * SCALING_FACTOR)

        self.log_message(f"Movimento manual para: X={target_x:.3f}, Y={target_y:.3f} (Modbus: {x_scaled}, {y_scaled})")
        
        # Envia a nova posição alvo para o Pico W usando write_multiple_registers
        # Também pode usar write_single_register se o Pico W tiver um registrador específico para comandos manuais
        success = self.modbus_handler.write_multiple_registers(
            address=MODBUS_REG_X_POS, # Usa os mesmos registradores para X e Y
            values=[x_scaled, y_scaled]
        )
        if success:
            self.log_message("  Comando de movimento manual enviado com sucesso.")
            # Atualiza a posição atual da GUI para a nova posição alvo
            self.current_x = target_x
            self.current_y = target_y
        else:
            self.log_message("  Falha ao enviar comando de movimento manual.")
        
        # Não usamos thread aqui pois movimentos manuais são tipicamente rápidos e únicos.
        # Se você fizer vários cliques rápidos, eles serão processados em sequência.


if __name__ == "__main__":
    root = tk.Tk()
    app = RobotControlGUI(root)
    # Tenta conectar ao Modbus automaticamente ao iniciar a aplicação
    # Isso pode ser ajustado para só conectar ao clicar no botão "Conectar Modbus"
    app.connect_modbus_gui()
    root.mainloop()