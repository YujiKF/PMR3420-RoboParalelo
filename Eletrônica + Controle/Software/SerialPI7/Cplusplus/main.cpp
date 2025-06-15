#include <iostream>
#include <string>
#include <vector>
#include <thread>
#include <chrono>
#include <limits> 
#include "serialib.h"

// =================================================================
//                      CONFIGURAÇÕES
// =================================================================
#define SERIAL_PORT "\\\\.\\COM8" // Alterar para a porta COM correta
#define BAUDRATE 115200

// Função para enviar o comando
void sendCommandToPIC(serialib &serial, const std::string &command) {
    std::cout << "\n-> Enviando comando: " << command << std::endl;

    // O protocolo exige um delay de 1ms entre cada caractere 
    for (char c : command) {
        serial.writeChar(c);
        std::this_thread::sleep_for(std::chrono::milliseconds(1));
    }
    std::cout << "   Comando enviado com sucesso." << std::endl;
}

void display_menu() {
    std::cout << "\n--- Controlador Interativo do PIC (PI-7) ---" << std::endl;
    std::cout << "1. Definir Posição (p)" << std::endl;
    std::cout << "2. Definir Ganho Proporcional (g)" << std::endl;
    std::cout << "3. Definir Ganho Integral (i)" << std::endl;
    std::cout << "4. Definir Ganho Derivativo (d)" << std::endl;
    std::cout << "5. Enviar Comando Home (h)" << std::endl;
    std::cout << "6. Sair" << std::endl;
    std::cout << "Escolha uma opção: ";
}

int main() {
    serialib serial;

    if (serial.openDevice(SERIAL_PORT, BAUDRATE) != 1) {
        std::cerr << "ERRO: Não foi possível abrir a porta " << SERIAL_PORT << std::endl;
        system("pause");
        return 1;
    }

    std::cout << "Conectado com sucesso a " << SERIAL_PORT << "!" << std::endl;

    int choice;
    double value;
    char command_buffer[100]; // Buffer para formatar a string final

    while (true) {
        display_menu();
        std::cin >> choice;

        // Validação de entrada: verifica se o usuário digitou um número
        if (std::cin.fail()) {
            std::cout << "\nOpção inválida. Por favor, digite um número." << std::endl;
            std::cin.clear(); // Limpa o estado de erro
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // Descarta a entrada ruim
            continue;
        }

        if (choice == 6) {
            break; // Sai do loop
        }

        // Para comandos que não precisam de valor
        if (choice == 5) { // Comando Home
            sendCommandToPIC(serial, ":ah;");
            continue; // Volta para o menu
        }

        // Pede o valor para os outros comandos
        if (choice >= 1 && choice <= 4) {
            std::cout << "Digite o valor: ";
            std::cin >> value;
            if (std::cin.fail()) {
                std::cout << "\nValor inválido. Por favor, digite um número." << std::endl;
                std::cin.clear();
                std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
                continue;
            }
        }

        std::string command_str;
        switch (choice) {
            case 1: // Posição
                snprintf(command_buffer, sizeof(command_buffer), ":ap%.2f;", value);
                command_str = command_buffer;
                break;
            case 2: // Ganho Proporcional
                snprintf(command_buffer, sizeof(command_buffer), ":ag%.2f;", value);
                command_str = command_buffer;
                break;
            case 3: // Ganho Integral
                snprintf(command_buffer, sizeof(command_buffer), ":ai%.2f;", value);
                command_str = command_buffer;
                break;
            case 4: // Ganho Derivativo
                snprintf(command_buffer, sizeof(command_buffer), ":ad%.2f;", value);
                command_str = command_buffer;
                break;
            default:
                std::cout << "\nOpção desconhecida. Tente novamente." << std::endl;
                continue; // Pula o envio e volta para o menu
        }
        
        sendCommandToPIC(serial, command_str);
    }

    serial.closeDevice();
    std::cout << "Porta serial fechada. Encerrando." << std::endl;

    return 0;
}