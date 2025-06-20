#include <iostream>
#include "serialib.h" // baixe em: https://github.com/imabot2/serialib
#include "serialib.cpp"

int main() {
    serialib serial;

    // Altere a porta COM conforme seu sistema
    // Ex: no Windows, geralmente COM3, COM4 etc
    char port[] = "\\\\.\\COM14"; // substitua pela sua porta

    // Tenta abrir a porta serial
    if (serial.openDevice(port, 19200) != 1) {
        std::cerr << "Erro ao abrir a porta serial!" << std::endl;
        return -1;
    }

    std::cout << "Porta serial aberta com sucesso.\n";

    // Envia uma mensagem
    const char* mensagem = "Ola do PC!\n";
    serial.writeString(mensagem);
    std::cout << "Mensagem enviada: " << mensagem;

    // Espera uma resposta (timeout: 5000 ms)
    char resposta[128];
    int bytesLidos = serial.readString(resposta, '\n', sizeof(resposta), 5000);

    if (bytesLidos > 0) {
        std::cout << "Resposta recebida: " << resposta << std::endl;
    } else {
        std::cout << "Nenhuma resposta recebida." << std::endl;
    }

    serial.closeDevice();
    return 0;
}
