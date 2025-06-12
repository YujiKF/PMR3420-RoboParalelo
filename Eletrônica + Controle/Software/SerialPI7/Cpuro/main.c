#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// =================================================================
//                      CONFIGURAÇÕES
// =================================================================
// Alterar "\\\\.\\COMx" para porta serial correta.
// As quatro barras invertidas são necessárias para o formato da string em C.
#define SERIAL_PORT_NAME "\\\\.\\COM3"

// Baudrate correto para o firmware pidx.X, conforme o README e o código-fonte serial.c
#define BAUD_RATE CBR_115200

// Protótipo da função
void sendCommandToPIC(HANDLE hSerial, const char* command);
void display_menu();

int main() {
    HANDLE hSerial; // "Handle" é como o Windows identifica a conexão
    DCB dcbSerialParams = {0}; // Estrutura para configurar os parâmetros da serial

    // --- 1. Abrir a Porta Serial ---
    hSerial = CreateFileA(
        SERIAL_PORT_NAME,        // Nome da porta
        GENERIC_WRITE,           // Abrir para escrita
        0,                       // Sem compartilhamento
        NULL,                    // Sem segurança
        OPEN_EXISTING,           // Abrir apenas se a porta existir
        FILE_ATTRIBUTE_NORMAL,   // Atributos normais
        NULL                     // Sem template
    );

    if (hSerial == INVALID_HANDLE_VALUE) {
        fprintf(stderr, "ERRO: Nao foi possivel abrir a porta %s. Verifique se esta correta e nao esta em uso.\n", SERIAL_PORT_NAME);
        system("pause"); // Pausa para o usuário ler o erro antes de fechar
        return 1;
    }

    // --- 2. Configurar a Porta Serial ---
    dcbSerialParams.DCBlength = sizeof(dcbSerialParams);
    if (!GetCommState(hSerial, &dcbSerialParams)) {
        fprintf(stderr, "ERRO: Nao foi possivel obter as configuracoes da porta.\n");
        CloseHandle(hSerial);
        return 1;
    }

    dcbSerialParams.BaudRate = BAUD_RATE;     // Definindo o Baudrate
    dcbSerialParams.ByteSize = 8;             // 8 bits de dados
    dcbSerialParams.StopBits = ONESTOPBIT;    // 1 stop bit
    dcbSerialParams.Parity   = NOPARITY;      // Sem paridade

    if (!SetCommState(hSerial, &dcbSerialParams)) {
        fprintf(stderr, "ERRO: Nao foi possivel definir as configuracoes da porta.\n");
        CloseHandle(hSerial);
        return 1;
    }

    printf("--- Terminal de Teste em C Puro para PIC ---\n");
    printf("Conectado com sucesso a %s!\n", SERIAL_PORT_NAME);

    // --- 3. Loop Principal com Menu Interativo ---
    int choice;
    double value;
    char command_buffer[100];

    while (1) {
        display_menu();
        if (scanf("%d", &choice) != 1) {
            printf("\nOpcao invalida. Por favor, digite um numero.\n");
            // Limpa o buffer de entrada do teclado
            while (getchar() != '\n');
            continue;
        }

        if (choice == 6) {
            break;
        }

        // Comando 'home' não precisa de valor
        if (choice == 5) {
            sendCommandToPIC(hSerial, ":ah;");
            continue;
        }
        
        // Pede um valor para os outros comandos
        if (choice >= 1 && choice <= 4) {
            printf("Digite o valor: ");
            if (scanf("%lf", &value) != 1) {
                printf("\nValor invalido. Por favor, digite um numero.\n");
                while (getchar() != '\n');
                continue;
            }

            // Monta a string de comando de forma segura
            switch (choice) {
                case 1: snprintf(command_buffer, sizeof(command_buffer), ":ap%.2f;", value); break;
                case 2: snprintf(command_buffer, sizeof(command_buffer), ":ag%.2f;", value); break;
                case 3: snprintf(command_buffer, sizeof(command_buffer), ":ai%.2f;", value); break;
                case 4: snprintf(command_buffer, sizeof(command_buffer), ":ad%.2f;", value); break;
            }
            sendCommandToPIC(hSerial, command_buffer);
        } else {
            printf("\nOpcao desconhecida. Tente novamente.\n");
        }
    }

    // --- 4. Fechar a Conexão ---
    CloseHandle(hSerial);
    printf("Porta serial fechada. Encerrando.\n");
    return 0;
}

// Função que envia o comando para o PIC, caractere por caractere
void sendCommandToPIC(HANDLE hSerial, const char* command) {
    DWORD bytes_written;
    size_t len = strlen(command);
    
    printf("\n-> Enviando comando: %s\n", command);

    // O protocolo do PI-7 exige um delay de 1ms entre cada caractere
    for (size_t i = 0; i < len; ++i) {
        if (!WriteFile(hSerial, &command[i], 1, &bytes_written, NULL)) {
            fprintf(stderr, "ERRO: Falha ao escrever na porta serial.\n");
            return;
        }
        Sleep(1); // Pausa de 1ms 
    }
    printf("   Comando enviado com sucesso.\n");
}

// Função que apenas exibe o menu de opções
void display_menu() {
    printf("\n--- Controlador Interativo do PIC (PI-7) ---\n");
    printf("1. Definir Posicao (p)\n");
    printf("2. Definir Ganho Proporcional (g)\n");
    printf("3. Definir Ganho Integral (i)\n");
    printf("4. Definir Ganho Derivativo (d)\n");
    printf("5. Enviar Comando Home (h)\n");
    printf("6. Sair\n");
    printf("Escolha uma opcao: ");
}