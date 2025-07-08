# modbus_comm.py
import serial
import struct
import time
from modbus_crc import calculate_crc16 # Certifique-se de que este arquivo existe e contém a função

class ModbusMaster:
    def __init__(self, port, baudrate, slave_id=1):
        self.port = port
        self.baudrate = baudrate
        self.slave_id = slave_id
        self.ser = None

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1) # Aumentar timeout para testes
            print(f"Conectado à porta serial {self.port} a {self.baudrate} bps.")
            return True
        except serial.SerialException as e:
            print(f"Erro ao conectar à porta serial: {e}")
            self.ser = None
            return False

    def disconnect(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Porta serial desconectada.")

    def _send_and_receive(self, adu_packet: bytes, expected_response_length: int = -1) -> bytes:
        """
        Envia um pacote Modbus ADU e recebe a resposta, validando o CRC.
        :param adu_packet: O pacote Modbus ADU (incluindo SlaveID, FC, Data, CRC).
        :param expected_response_length: Comprimento esperado da resposta. Use -1 para leitura dinâmica.
        :return: A resposta Modbus ADU se válida, caso contrário b''.
        """
        if not self.ser or not self.ser.is_open:
            print("Erro: Porta serial não conectada.")
            return b''

        self.ser.flushInput() # Limpa o buffer de entrada antes de enviar
        self.ser.write(adu_packet)

        # Pequena pausa para o slave processar e responder (ajuste se necessário)
        time.sleep(0.02) # 20ms para permitir que o Pico responda.

        response = b''
        if expected_response_length != -1:
            # Tenta ler o número exato de bytes esperado
            response = self.ser.read(expected_response_length)
        else:
            # Leitura dinâmica: lê o cabeçalho e depois o restante com base no Byte Count
            # Isso é mais complexo e pode ser feito de forma mais robusta em um loop.
            # Para Read Holding Registers (FC 0x03), a resposta é:
            # [SlaveID][FC][ByteCount][Data...][CRC L][CRC H]
            # Mínimo 5 bytes (1+1+1+2 para CRC)
            header = self.ser.read(3) # SlaveID (1) + FC (1) + ByteCount (1)
            if len(header) < 3:
                print("Resposta muito curta para cabeçalho.")
                return b''
            
            # Verificar se é uma resposta de exceção (FC com MSB setado)
            if (header[1] & 0x80) == 0x80:
                # É uma exceção: [SlaveID][FC|0x80][ExCode][CRC L][CRC H]
                # Comprimento total esperado = 5 bytes
                remaining_bytes = self.ser.read(2) # ExCode + 2 CRC bytes
                response = header + remaining_bytes
                if len(response) == 5:
                    print(f"Resposta de exceção Modbus: {response.hex().upper()}")
                    # Validação CRC da exceção
                    received_crc_ex = (response[4] << 8) | response[3]
                    calculated_crc_ex = calculate_crc16(response[:3])
                    if received_crc_ex == (calculated_crc_ex & 0xFFFF):
                         # Retorna a exceção para que o chamador possa tratá-la
                        return response
                    else:
                        print("CRC inválido na resposta de exceção.")
                        return b''
                else:
                    print("Resposta de exceção incompleta.")
                    return b''


            byte_count = header[2] # ByteCount para FC 0x03
            if byte_count > 0:
                # Ler os bytes de dados + 2 bytes de CRC
                data_and_crc = self.ser.read(byte_count + 2)
                response = header + data_and_crc
            else:
                # Se ByteCount for 0 ou inválido, pode ser um erro ou fim de mensagem.
                # Para FC 0x03, ByteCount deve ser > 0 se há registradores.
                print("ByteCount inválido ou zero na resposta.")
                return b''


        if not response:
            print("Nenhuma resposta Modbus recebida.")
            return b''

        if len(response) < 2:
            print("Resposta muito curta para conter CRC.")
            return b''

        # Modbus RTU CRC é LSB primeiro (little-endian)
        received_crc_val = int.from_bytes(response[-2:], 'little')
        calculated_response_crc_val = int.from_bytes(calculate_crc16(response[:-2]), 'little')

        if received_crc_val != calculated_response_crc_val:
            print(f"Erro de CRC na resposta. Recebido: {hex(received_crc_val).upper()}, Calculado: {hex(calculated_response_crc_val).upper()}")
            print(f"Resposta bruta: {response.hex().upper()}")
            return b''

        return response

    def _parse_exception_response(self, response: bytes) -> tuple[int, int]:
        """
        Parses an exception response and returns (function_code, exception_code).
        Assumes CRC has already been validated.
        """
        if len(response) == 5 and (response[1] & 0x80) == 0x80:
            return response[1] & 0x7F, response[2]
        return 0, 0 # Not an exception response

    def read_holding_registers(self, starting_address: int, quantity: int) -> list[int] | None:
        """
        Lê um ou mais registradores de retenção (Holding Registers) do slave (FC 0x03).
        :param starting_address: Endereço inicial do registrador.
        :param quantity: Número de registradores a ler.
        :return: Uma lista de inteiros (valores dos registradores) ou None em caso de erro.
        """
        if not (1 <= quantity <= 125): # Limite para FC 0x03
            print(f"Erro: Quantidade de registradores inválida ({quantity}). Deve ser entre 1 e 125.")
            return None

        # FC 0x03 Request: [SlaveID] [0x03] [Addr High] [Addr Low] [Quantity High] [Quantity Low] [CRC L] [CRC H]
        pdu = bytearray([
            self.slave_id,
            0x03,
            (starting_address >> 8) & 0xFF,
            starting_address & 0xFF,
            (quantity >> 8) & 0xFF,
            quantity & 0xFF
        ])
        crc = calculate_crc16(pdu)
        adu = pdu + crc
        print(f"Enviando (FC 0x03): {adu.hex().upper()}")

        # Resposta esperada: SlaveID (1) + FC (1) + ByteCount (1) + (quantity * 2) + CRC (2)
        expected_response_len = 1 + 1 + 1 + (quantity * 2) + 2
        response = self._send_and_receive(adu, expected_response_len)

        if not response:
            return None

        # Checar se é uma resposta de exceção
        if (response[1] & 0x80) == 0x80:
            fc_error, ex_code = self._parse_exception_response(response)
            print(f"Erro do slave (FC 0x03): Função {fc_error}, Exception Code {ex_code}")
            return None

        # Validar a estrutura da resposta de sucesso
        if len(response) != expected_response_len or \
           response[0] != self.slave_id or \
           response[1] != 0x03 or \
           response[2] != (quantity * 2):
            print(f"Resposta inválida (FC 0x03). Recebido: {response.hex().upper()}")
            return None

        # Extrair os valores dos registradores
        registers = []
        for i in range(quantity):
            # Os valores dos registradores são big-endian (MSB primeiro)
            value = (response[3 + (i * 2)] << 8) | response[4 + (i * 2)]
            registers.append(value)

        print(f"Resposta de sucesso (FC 0x03): {response.hex().upper()}. Registros: {registers}")
        return registers

    def write_single_register(self, register_address: int, value: int) -> bool:
        """
        Escreve um único registrador de retenção (Holding Register) no slave (FC 0x06).
        :param register_address: Endereço do registrador a escrever.
        :param value: Valor inteiro (0-65535) a ser escrito.
        :return: True se a escrita foi bem-sucedida, False caso contrário.
        """
        # FC 0x06 Request: [SlaveID] [0x06] [Addr High] [Addr Low] [Value High] [Value Low] [CRC L] [CRC H]
        pdu = bytearray([
            self.slave_id,
            0x06,
            (register_address >> 8) & 0xFF,
            register_address & 0xFF,
            (value >> 8) & 0xFF,
            value & 0xFF
        ])
        crc = calculate_crc16(pdu)
        adu = pdu + crc
        print(f"Enviando (FC 0x06): {adu.hex().upper()}")

        # Resposta de sucesso para FC 0x06 é um eco da requisição (8 bytes)
        response = self._send_and_receive(adu, len(adu)) # Espera o mesmo comprimento que a requisição

        if not response:
            return False

        # Checar se é uma resposta de exceção
        if (response[1] & 0x80) == 0x80:
            fc_error, ex_code = self._parse_exception_response(response)
            print(f"Erro do slave (FC 0x06): Função {fc_error}, Exception Code {ex_code}")
            return False

        # Resposta de sucesso para FC 0x06 é o eco exato da requisição
        if response == adu:
            print(f"Resposta de sucesso (FC 0x06): {response.hex().upper()}")
            return True
        else:
            print(f"Resposta inválida (FC 0x06). Recebido: {response.hex().upper()}")
            return False

    def write_multiple_registers(self, starting_address: int, values: list[int]) -> bool:
        """
        Escreve múltiplos registradores de retenção (Holding Registers) no slave (FC 0x10).
        :param starting_address: Endereço inicial do primeiro registrador a escrever.
        :param values: Lista de valores inteiros (0-65535) a serem escritos.
        :return: True se a escrita foi bem-sucedida, False caso contrário.
        """
        num_registers = len(values)
        if not (1 <= num_registers <= 123): # Limite para FC 0x10
            print(f"Erro: Número de registradores inválido ({num_registers}). Deve ser entre 1 e 123.")
            return False
        
        byte_count = num_registers * 2 # Cada registrador tem 2 bytes

        # FC 0x10 Request: [SlaveID] [0x10] [Addr H] [Addr L] [Num Reg H] [Num Reg L] [Byte Count] [Reg1_H] [Reg1_L] ... [CRC L] [CRC H]
        pdu = bytearray([
            self.slave_id,
            0x10,
            (starting_address >> 8) & 0xFF,
            starting_address & 0xFF,
            (num_registers >> 8) & 0xFF,
            num_registers & 0xFF,
            byte_count
        ])

        for val in values:
            pdu.extend(val.to_bytes(2, 'big')) # Valores dos registradores são big-endian

        crc = calculate_crc16(pdu)
        adu = pdu + crc
        print(f"Enviando (FC 0x10): {adu.hex().upper()}")

        # Resposta esperada para FC 0x10 sucesso: [SlaveID] [0x10] [Addr H] [Addr L] [Num Reg H] [Num Reg L] [CRC L] [CRC H] (8 bytes)
        expected_response_len = 8
        response = self._send_and_receive(adu, expected_response_len)

        if not response:
            return False

        # Checar se é uma resposta de exceção
        if (response[1] & 0x80) == 0x80:
            fc_error, ex_code = self._parse_exception_response(response)
            print(f"Erro do slave (FC 0x10): Função {fc_error}, Exception Code {ex_code}")
            return False

        # Validar a estrutura da resposta de sucesso
        if len(response) != expected_response_len or \
           response[0] != self.slave_id or \
           response[1] != 0x10 or \
           (response[2] << 8 | response[3]) != starting_address or \
           (response[4] << 8 | response[5]) != num_registers:
            print(f"Resposta inválida (FC 0x10). Recebido: {response.hex().upper()}")
            return False

        print(f"Resposta de sucesso (FC 0x10): {response.hex().upper()}")
        return True


    def write_file_record(self, file_number: int, record_number: int, values: list[int]) -> bool:
        """
        Escreve um registro em um arquivo no slave (FC 0x15).
        Os valores são inteiros de 16 bits.
        :param file_number: Número do arquivo (1 a 65535).
        :param record_number: Número do registro dentro do arquivo (0 a 9999).
        :param values: Lista de valores inteiros (16 bits) a serem escritos no registro.
        :return: True se a escrita foi bem-sucedida, False caso contrário.
        """
        record_length = len(values) # Record length in words
        if not (1 <= record_length <= 0x7D): # Record Length (0x01 a 0x7D words, ou seja, 1 a 125 palavras)
            print(f"Erro: Comprimento do registro inválido ({record_length}). Deve ser entre 1 e 125.")
            return False

        # Calculate Request Data Length:
        # 1 byte (Reference Type) + 2 bytes (File Number) + 2 bytes (Record Number) + 2 bytes (Record Length)
        # + (record_length * 2) bytes (Record Data)
        request_data_length = 1 + 2 + 2 + 2 + (record_length * 2)

        # FC 0x15 Request:
        # [SlaveID] [0x15] [Request Data Length]
        # [Reference Type (0x06)] [File Number H] [File Number L]
        # [Record Number H] [Record Number L] [Record Length H] [Record Length L]
        # [Record Data...] [CRC L] [CRC H]
        pdu = bytearray([
            self.slave_id,
            0x15,
            request_data_length, # This is the length of the PDU's data part (after FC)
            0x06, # Reference Type for File Record
            (file_number >> 8) & 0xFF,
            file_number & 0xFF,
            (record_number >> 8) & 0xFF,
            record_number & 0xFF,
            (record_length >> 8) & 0xFF, # Note: Record Length is in words, not bytes
            record_length & 0xFF
        ])

        for val in values:
            pdu.extend(val.to_bytes(2, 'big')) # Record Data (big-endian)

        crc = calculate_crc16(pdu)
        adu = pdu + crc
        print(f"Enviando (FC 0x15): {adu.hex().upper()}")

        # A resposta esperada para FC 0x15 de sucesso é um ECO EXATO da ADU da requisição
        expected_response_len = len(adu) # Agora, espera-se o mesmo tamanho da requisição
        response = self._send_and_receive(adu, expected_response_len)

        if not response:
            return False

        # Checar se é uma resposta de exceção
        if (response[1] & 0x80) == 0x80:
            fc_error, ex_code = self._parse_exception_response(response)
            print(f"Erro do slave (FC 0x15): Função {fc_error}, Exception Code {ex_code}")
            return False

        # A resposta de sucesso para FC 0x15 deve ser um eco exato da requisição ADU
        if response == adu:
            print(f"Resposta de sucesso (FC 0x15): {response.hex().upper()} (Eco da requisição)")
            return True
        else:
            print(f"Resposta inválida (FC 0x15). Recebido: {response.hex().upper()} | Esperado: {adu.hex().upper()}")
            return False

# O bloco __main__ no modbus_comm.py pode permanecer o mesmo, apenas o teste para 0x15 agora espera um eco completo.

# Exemplo de uso:
if __name__ == '__main__':
    # Adapte a porta serial para a que o Raspberry Pi Pico está conectado
    SERIAL_PORT = 'COM9' # <--- ALtere para a sua porta (Windows: 'COMx', Linux/macOS: '/dev/ttyACM0' ou '/dev/ttyUSB0')
    BAUD_RATE = 115200

    master = ModbusMaster(SERIAL_PORT, BAUD_RATE)

    if master.connect():
        # --- Teste FC 0x06: Write Single Register ---
        print("\n--- Teste Write Single Register (FC 0x06) ---")
        success_06 = master.write_single_register(0x0000, 123)
        print(f"Envio FC 0x06 {'SUCESSO' if success_06 else 'FALHA'}")
        time.sleep(0.5)

        # --- Teste FC 0x03: Read Holding Registers ---
        print("\n--- Teste Read Holding Registers (FC 0x03) ---")
        # Espera que o registrador 0x0000 tenha sido escrito para 123
        # E que o 0x0001 e 0x0002 tenham sido escritos em um teste FC 0x10 anterior
        read_registers = master.read_holding_registers(0x0000, 3) # Ler 3 registradores a partir do 0x0000
        if read_registers is not None:
            print(f"Registradores lidos: {read_registers}")
        else:
            print("Falha ao ler registradores.")
        time.sleep(0.5)

        # --- Teste FC 0x10: Write Multiple Registers ---
        print(f"\n--- Teste Write Multiple Registers (FC 0x10) ---")
        x_scaled = int(10.5 * 1000)
        y_scaled = int(20.75 * 1000)
        data_points = [x_scaled, y_scaled]
        print(f"Enviando X={x_scaled}, Y={y_scaled} para registradores 0x0001 e 0x0002")
        success_10 = master.write_multiple_registers(0x0001, data_points)
        print(f"Envio FC 0x10 {'SUCESSO' if success_10 else 'FALHA'}")
        time.sleep(0.5)
        
        # --- Teste FC 0x03 novamente para confirmar valores FC 0x10 ---
        print("\n--- Teste Read Holding Registers (FC 0x03) após FC 0x10 ---")
        read_registers_after_10 = master.read_holding_registers(0x0000, 3)
        if read_registers_after_10 is not None:
            print(f"Registradores lidos: {read_registers_after_10}")
        else:
            print("Falha ao ler registradores após FC 0x10.")
        time.sleep(0.5)


        # --- Teste FC 0x15: Write File Record ---
        print("\n--- Teste Write File Record (FC 0x15) ---")
        # Exemplo: Escrever no File 1, Record 0, com 2 valores
        # Note que o Pico terá que implementar o conceito de "arquivos" e "registros"
        # que é uma abstração a mais que simples registradores de holding.
        file_num = 1
        record_num = 0
        file_data = [0xAAAA, 0xBBBB, 0xCCCC] # 3 valores de 16 bits
        print(f"Enviando valores {file_data} para File {file_num}, Record {record_num}")
        success_15 = master.write_file_record(file_num, record_num, file_data)
        print(f"Envio FC 0x15 {'SUCESSO' if success_15 else 'FALHA'}")
        time.sleep(0.5)

        master.disconnect()
    else:
        print("Não foi possível conectar ao Raspberry Pi Pico. Verifique a porta e a conexão.")