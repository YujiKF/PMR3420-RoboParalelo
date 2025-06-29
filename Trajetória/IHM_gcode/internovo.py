import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

pontos = []
nome_arquivo = ""

def ler_pontos(caminho):
    pontos_lidos = []
    with open(caminho, 'r') as f:
        for linha in f:
            try:
                x, y = map(float, linha.strip().split())
                pontos_lidos.append((x, y))
            except:
                continue
    return pontos_lidos

def gerar_gcode(pontos):
    if not pontos:
        return []

    linhas = [
        "G21;",
        "G90;"
    ]
    x0, y0 = pontos[0]
    linhas.append(f"G1 X{x0:.2f} Y{y0:.2f};")

    for x, y in pontos[1:]:
        linhas.append(f"G1 X{x:.2f} Y{y:.2f};")
    
    return linhas

def salvar_gcode(gcode):
    caminho = filedialog.asksaveasfilename(defaultextension=".gcode", filetypes=[("G-code files", "*.gcode")])
    if caminho:
        with open(caminho, 'w') as f:
            f.write('\n'.join(gcode))
        messagebox.showinfo("Sucesso", "G-code salvo com sucesso!")

def carregar_arquivo():
    global pontos, nome_arquivo
    caminho = filedialog.askopenfilename(filetypes=[("Arquivos de texto", "*.txt *.csv")])
    if caminho:
        nome_arquivo = os.path.splitext(os.path.basename(caminho))[0]
        pontos = ler_pontos(caminho)

        if not pontos:
            messagebox.showerror("Erro", "Nenhum ponto válido encontrado.")
            return

        # Exibir conteúdo do arquivo de pontos
        with open(caminho, 'r') as f:
            conteudo_txt = f.read()

        text_area_input.config(state=tk.NORMAL)
        text_area_input.delete(1.0, tk.END)
        text_area_input.insert(tk.END, conteudo_txt)
        text_area_input.config(state=tk.DISABLED)
        label_input.config(text=nome_arquivo + ".txt")

        # Gera G-code e mostra no campo ao lado
        gcode = gerar_gcode(pontos)
        text_area_gcode.config(state=tk.NORMAL)
        text_area_gcode.delete(1.0, tk.END)
        text_area_gcode.insert(tk.END, "\n".join(gcode))
        text_area_gcode.config(state=tk.DISABLED)
        label_output.config(text=nome_arquivo + ".gcode")

        atualizar_grafico()

def atualizar_grafico():
    if not pontos:
        return

    x_vals = [p[0] for p in pontos]
    y_vals = [p[1] for p in pontos]

    fig.clear()
    ax = fig.add_subplot(111)
    ax.plot(x_vals, y_vals, 'o-', color='blue', linewidth=1.5, markersize=4, label='Trajetória')
    ax.set_title('Visualização da Trajetória G-code', fontsize=14, fontweight='bold')
    ax.set_xlabel('X (mm)', fontsize=12) # Título do eixo X
    ax.set_ylabel('Y (mm)', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_xlim(0, 364)
    ax.set_ylim(0, 364)
    ax.set_aspect('equal', adjustable='box')
    ax.legend(fontsize=10)
    ax.tick_params(axis='both', which='major', labelsize=10)

    canvas.draw()

def salvar():
    if not pontos:
        messagebox.showerror("Erro", "Nenhum ponto carregado.")
        return
    gcode = gerar_gcode(pontos)
    salvar_gcode(gcode)

# === INTERFACE ===
root = tk.Tk()
root.title("Gerador de G-code Robo Paralelo")
root.geometry("1000x750")

# Cria um Canvas com scrollbar
canvas_main = tk.Canvas(root)
canvas_main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas_main.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas_main.configure(yscrollcommand=scrollbar.set)
canvas_main.bind('<Configure>', lambda e: canvas_main.configure(scrollregion=canvas_main.bbox("all")))

scrollable_frame = tk.Frame(canvas_main)
canvas_main.create_window((0, 0), window=scrollable_frame, anchor="nw", width=1000) # Define a largura para 1000 pixels

# TOPO: Botões
frame_topo = tk.Frame(scrollable_frame) # Usar scrollable_frame
frame_topo.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

btn_abrir = tk.Button(frame_topo, text="Abrir Arquivo de Pontos", command=carregar_arquivo)
btn_abrir.pack(side=tk.LEFT, padx=5)

btn_salvar = tk.Button(frame_topo, text="Salvar G-code", command=salvar)
btn_salvar.pack(side=tk.LEFT, padx=5)

# MEIO: Textos lado a lado
frame_textos = tk.Frame(scrollable_frame) # Usar scrollable_frame
frame_textos.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

# === Coluna da esquerda: pontos (entrada)
frame_esq = tk.Frame(frame_textos)
frame_esq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

label_input = tk.Label(frame_esq, text="Arquivo de Pontos")
label_input.pack()

text_area_input = scrolledtext.ScrolledText(frame_esq, width=50, height=20)
text_area_input.pack(fill=tk.BOTH, expand=True)
text_area_input.config(state=tk.DISABLED)

# === Coluna da direita: G-code (saída)
frame_dir = tk.Frame(frame_textos)
frame_dir.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

label_output = tk.Label(frame_dir, text="Arquivo G-code Gerado")
label_output.pack()

text_area_gcode = scrolledtext.ScrolledText(frame_dir, width=50, height=20)
text_area_gcode.pack(fill=tk.BOTH, expand=True)
text_area_gcode.config(state=tk.DISABLED)

# BASE: Gráfico
frame_plot = tk.Frame(scrollable_frame) # Usar scrollable_frame
frame_plot.pack(side=tk.BOTTOM, fill=tk.X, expand=False, padx=20, pady=5) # Adicionado padx e fill=tk.X para ajustar largura

fig = plt.Figure(figsize=(6, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=frame_plot)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


# Start
root.mainloop()