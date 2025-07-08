# modbus_crc.py

def calculate_crc16(data: bytes) -> bytes:
    """
    Calcula o CRC-16 Modbus para uma sequência de bytes.
    Retorna o CRC como bytes (LSB primeiro).
    """
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if (crc & 0x0001):
                crc >>= 1
                crc ^= 0xA001  # Polinômio Modbus
            else:
                crc >>= 1
    # Modbus RTU usa o CRC com o byte menos significativo (LSB) primeiro
    return crc.to_bytes(2, 'little')

if __name__ == '__main__':
    # Teste de exemplo: A mensagem '1103006B0003' deve ter CRC '76B1' (do documento Modbus)
    # Exemplo: '01030000000A' (Endereço 01, FC 03, Endereço Inicial 0000, 10 Registradores)
    test_data_hex = "01030000000A"
    test_data_bytes = bytes.fromhex(test_data_hex)
    calculated_crc = calculate_crc16(test_data_bytes)
    print(f"Dados: {test_data_bytes.hex().upper()}")
    print(f"CRC Calculado (hex LSB first): {calculated_crc.hex().upper()}") # Deve ser B5CD para 01030000000A

    # Outro teste: '01060001000A' (Endereço 01, FC 06, Reg 0001, Valor 000A)
    test_data_hex_2 = "01060001000A"
    test_data_bytes_2 = bytes.fromhex(test_data_hex_2)
    calculated_crc_2 = calculate_crc16(test_data_bytes_2)
    print(f"Dados: {test_data_bytes_2.hex().upper()}")
    print(f"CRC Calculado (hex LSB first): {calculated_crc_2.hex().upper()}") # Deve ser 99EA