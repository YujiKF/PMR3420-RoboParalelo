import serial
import time
import sys

# =================================================================
#                      CONFIGURAÇÕES
# =================================================================
# Altere para a porta COM correta
SERIAL_PORT = 'COM3' 

# Baudrate CORRETO para o firmware pidx.X, conforme o README.md
BAUD_RATE = 115200

def send_command_to_pic(serial_connection, command):
    """
    Envia um comando para o PIC, caractere por caractere,
    respeitando o delay de 1ms exigido pelo protocolo.
    """
    print(f"\n-> Enviando comando: {command}")
    try:
        for char in command:
            serial_connection.write(char.encode('ascii'))
            time.sleep(0.001) # Pausa de 1ms
        print("   Comando enviado com sucesso.")
    except serial.SerialException as e:
        print(f"ERRO ao enviar dados: {e}")

def display_menu():
    """Exibe o menu de opções para o usuário."""
    print("\n--- Controlador Interativo do PIC (Python) ---")
    print("1. Definir Posição (p)")
    print("2. Definir Ganho Proporcional (g)")
    print("3. Definir Ganho Integral (i)")
    print("4. Definir Ganho Derivativo (d)")
    print("5. Enviar Comando Home (h)")
    print("6. Sair")
    return input("Escolha uma opção: ")

def main():
    """Função principal do programa."""
    try:
        # 1. Abre a porta serial
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Conectado com sucesso a {SERIAL_PORT}!")
    except serial.SerialException as e:
        print(f"ERRO: Nao foi possivel abrir a porta {SERIAL_PORT}.")
        print(f"Detalhe: {e}")
        sys.exit(1)

    # 2. Loop principal
    while True:
        choice = display_menu()

        if choice == '6':
            break
        
        command_to_send = ""
        
        if choice == '5': # Comando Home (não precisa de valor)
            command_to_send = ":ah;"
            send_command_to_pic(ser, command_to_send)
            continue

        try:
            # Pede o valor para os outros comandos
            if choice in ['1', '2', '3', '4']:
                value = float(input("Digite o valor: "))
                
                if choice == '1': # Posição
                    command_to_send = f":ap{value:.2f};"
                elif choice == '2': # Ganho Proporcional
                    command_to_send = f":ag{value:.2f};"
                elif choice == '3': # Ganho Integral
                    command_to_send = f":ai{value:.2f};"
                elif choice == '4': # Ganho Derivativo
                    command_to_send = f":ad{value:.2f};"
                
                send_command_to_pic(ser, command_to_send)
            else:
                print("\nOpção inválida. Tente novamente.")

        except ValueError:
            print("\nEntrada inválida. Por favor, digite um número para o valor.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    # 3. Fecha a porta ao sair
    ser.close()
    print("Porta serial fechada. Encerrando.")


if __name__ == "__main__":
    main()