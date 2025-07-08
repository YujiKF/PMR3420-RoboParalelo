# modbus_handler.py (VERSÃO ATUALIZADA PARA USAR SEU modbus_comm.py)

import time
import serial.tools.list_ports # Para listar portas disponíveis, útil para depuração

# Importa a sua classe ModbusMaster do seu arquivo modbus_comm.py
from modbus_comm import ModbusMaster

class ModbusHandler:
    def __init__(self, port, baudrate, slave_id=1, timeout=0.5):
        self.port = port
        self.baudrate = baudrate
        self.slave_id = slave_id
        # Cria uma instância do SEU ModbusMaster
        self.master = ModbusMaster(port=self.port, baudrate=self.baudrate, slave_id=self.slave_id)
        self.is_connected = False
        self.timeout = timeout # Embora seu ModbusMaster já tenha um timeout, mantemos aqui para consistência

    def connect(self):
        """Tenta conectar à porta serial Modbus usando seu ModbusMaster."""
        if self.is_connected:
            print("ModbusHandler: Já conectado.")
            return True

        print(f"ModbusHandler: Tentando conectar ao {self.port} @ {self.baudrate} bps...")
        if self.master.connect(): # Chama o método connect do seu ModbusMaster
            self.is_connected = True
            print("ModbusHandler: Conectado com sucesso.")
            return True
        else:
            self.is_connected = False
            print("ModbusHandler: Falha ao conectar.")
            return False

    def disconnect(self):
        """Desconecta da porta serial Modbus usando seu ModbusMaster."""
        if self.is_connected:
            self.master.disconnect() # Chama o método disconnect do seu ModbusMaster
            self.is_connected = False
            print("ModbusHandler: Desconectado.")
        else:
            print("ModbusHandler: Já desconectado.")

    def write_multiple_registers(self, address, values):
        """
        Escreve múltiplos registradores no slave Modbus.
        :param address: Endereço inicial do registrador.
        :param values: Lista de valores (inteiros) a serem escritos.
        :return: True se a escrita for bem-sucedida, False caso contrário.
        """
        if not self.is_connected:
            print("ModbusHandler: Erro: Não conectado para escrever múltiplos registradores.")
            return False
        # Chama o método do seu ModbusMaster
        success = self.master.write_multiple_registers(address, values)
        if success:
            print(f"ModbusHandler: Escrita FC0x10 em addr {address} com {values} - SUCESSO")
        else:
            print(f"ModbusHandler: Escrita FC0x10 em addr {address} com {values} - FALHA")
        return success

    def read_holding_registers(self, address, quantity):
        """
        Lê múltiplos registradores do slave Modbus.
        :param address: Endereço inicial do registrador.
        :param quantity: Quantidade de registradores a ler.
        :return: Lista de valores lidos ou None em caso de erro.
        """
        if not self.is_connected:
            print("ModbusHandler: Erro: Não conectado para ler holding registers.")
            return None
        # Chama o método do seu ModbusMaster
        response = self.master.read_holding_registers(address, quantity)
        if response is not None:
            print(f"ModbusHandler: Leitura FC0x03 de addr {address}, qty {quantity}: {response} - SUCESSO")
        else:
            print(f"ModbusHandler: Leitura FC0x03 de addr {address}, qty {quantity}: FALHA")
        return response

    def write_single_register(self, address, value):
        """
        Escreve um único registrador no slave Modbus.
        :param address: Endereço do registrador.
        :param value: Valor (inteiro) a ser escrito.
        :return: True se a escrita for bem-sucedida, False caso contrário.
        """
        if not self.is_connected:
            print("ModbusHandler: Erro: Não conectado para escrever single register.")
            return False
        # Chama o método do seu ModbusMaster
        success = self.master.write_single_register(address, value)
        if success:
            print(f"ModbusHandler: Escrita FC0x06 em addr {address} com {value} - SUCESSO")
        else:
            print(f"ModbusHandler: Escrita FC0x06 em addr {address} com {value} - FALHA")
        return success

    # Adicione outros wrappers se precisar usar FC 0x15 (Write File Record)
    def write_file_record(self, file_number, record_number, record_data):
        if not self.is_connected:
            print("ModbusHandler: Erro: Não conectado para escrever file record.")
            return False
        success = self.master.write_file_record(file_number, record_number, record_data)
        if success:
            print(f"ModbusHandler: Escrita FC0x15 (File {file_number}, Record {record_number}) - SUCESSO")
        else:
            print(f"ModbusHandler: Escrita FC0x15 (File {file_number}, Record {record_number}) - FALHA")
        return success


# --- Exemplo de uso para teste do modbus_handler.py (usando seu ModbusMaster) ---
if __name__ == "__main__":
    # Liste as portas seriais disponíveis para ajudar na escolha
    print("Portas seriais disponíveis:")
    ports = serial.tools.list_ports.comports()
    if ports:
        for p in ports:
            print(f"  {p.device} - {p.description}")
    else:
        print("  Nenhuma porta serial encontrada.")

    # Certifique-se de que o Pico W está conectado e rodando o slave Modbus
    # e que a porta COM está correta (verifique no Gerenciador de Dispositivos)
    COM_PORT = 'COM9' # <-- AJUSTE A PORTA CONFORME SEU SISTEMA!
    BAUD_RATE = 115200

    print(f"\nTeste do ModbusHandler usando seu ModbusMaster na porta {COM_PORT}...")
    modbus = ModbusHandler(port=COM_PORT, baudrate=BAUD_RATE)

    if modbus.connect():
        # Teste de escrita (FC 0x06) - Endereço 0, Valor 123
        print("\n--- Teste Write Single Register (FC 0x06) ---")
        modbus.write_single_register(0x0000, 123)
        time.sleep(0.5)

        # Teste de leitura (FC 0x03) - 3 registradores a partir do endereço 0
        print("\n--- Teste Read Holding Registers (FC 0x03) ---")
        read_values = modbus.read_holding_registers(0x0000, 3)
        if read_values is not None:
            print(f"Valores lidos: {read_values}")
        time.sleep(0.5)

        # Teste de escrita múltipla (FC 0x10) - Endereço 1, Valores [10500, 20750]
        print("\n--- Teste Write Multiple Registers (FC 0x10) ---")
        modbus.write_multiple_registers(0x0001, [10500, 20750])
        time.sleep(0.5)

        # Leitura novamente para confirmar
        print("\n--- Teste Read Holding Registers (FC 0x03) após FC 0x10 ---")
        read_values_after_write = modbus.read_holding_registers(0x0000, 3)
        if read_values_after_write is not None:
            print(f"Valores lidos após escrita múltipla: {read_values_after_write}")

    print("\nEncerrando teste do ModbusHandler.")
    modbus.disconnect()