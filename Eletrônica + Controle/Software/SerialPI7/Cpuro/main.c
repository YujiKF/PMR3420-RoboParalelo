#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// =================================================================
//                      CONFIGURAÇÕES
// =================================================================
#define SERIAL_PORT_NAME "\\\\.\\COM14"
#define BAUD_RATE CBR_115200

void sendCommandToPIC(HANDLE hSerial, const char* command);
void display_menu();

int main() {
    HANDLE hSerial;
    DCB dcbSerialParams = {0};

    // --- Abrir Porta Serial ---
    hSerial = CreateFileA(
        SERIAL_PORT_NAME,
        GENERIC_READ | GENERIC_WRITE, // Permitir leitura e escrita
        0,
        NULL,
        OPEN_EXISTING,
        FILE_ATTRIBUTE_NORMAL,
        NULL
    );

    if (hSerial == INVALID_HANDLE_VALUE) {
        fprintf(stderr, "ERRO: Nao foi possivel abrir a porta %s.\n", SERIAL_PORT_NAME);
        system("pause");
        return 1;
    }

    // --- Configurar Porta Serial ---
    dcbSerialParams.DCBlength = sizeof(dcbSerialParams);
    if (!GetCommState(hSerial, &dcbSerialParams)) {
        fprintf(stderr, "ERRO: Nao foi possivel obter configuracoes.\n");
        CloseHandle(hSerial);
        return 1;
    }

    dcbSerialParams.BaudRate = BAUD_RATE;
    dcbSerialParams.ByteSize = 8;
    dcbSerialParams.StopBits = ONESTOPBIT;
    dcbSerialParams.Parity   = NOPARITY;

    if (!SetCommState(hSerial, &dcbSerialParams)) {
        fprintf(stderr, "ERRO: Nao foi possivel definir configuracoes.\n");
        CloseHandle(hSerial);
        return 1;
    }

    // --- Configurar Timeouts ---
    COMMTIMEOUTS timeouts = {0};
    timeouts.ReadIntervalTimeout = 50;
    timeouts.ReadTotalTimeoutConstant = 50;
    timeouts.ReadTotalTimeoutMultiplier = 10;
    timeouts.WriteTotalTimeoutConstant = 50;
    timeouts.WriteTotalTimeoutMultiplier = 10;
    SetCommTimeouts(hSerial, &timeouts);

    printf("--- Terminal de Teste para PIC (com loopback) ---\n");
    printf("Conectado com sucesso a %s!\n", SERIAL_PORT_NAME);

    // --- Loop Principal ---
    int choice;
    double value;
    char command_buffer[100];

    while (1) {
        display_menu();
        if (scanf("%d", &choice) != 1) {
            printf("\nOpcao invalida. Digite um numero.\n");
            while (getchar() != '\n');
            continue;
        }

        if (choice == 6) {
            break;
        }

        if (choice == 5) {
            sendCommandToPIC(hSerial, ":ah;");
            continue;
        }

        if (choice >= 1 && choice <= 4) {
            printf("Digite o valor: ");
            if (scanf("%lf", &value) != 1) {
                printf("\nValor invalido. Digite um numero.\n");
                while (getchar() != '\n');
                continue;
            }

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

    // --- Fechar Porta Serial ---
    CloseHandle(hSerial);
    printf("Porta serial fechada. Encerrando.\n");
    return 0;
}

void sendCommandToPIC(HANDLE hSerial, const char* command) {
    DWORD bytes_written;
    DWORD bytes_read;
    char response[256] = {0};

    size_t len = strlen(command);
    printf("\n-> Enviando comando: %s\n", command);

    for (size_t i = 0; i < len; ++i) {
        if (!WriteFile(hSerial, &command[i], 1, &bytes_written, NULL)) {
            fprintf(stderr, "ERRO: Falha ao escrever na porta serial.\n");
            return;
        }
        Sleep(1);
    }

    printf("   Comando enviado com sucesso.\n");

    Sleep(100); // Aguarda resposta

    if (!ReadFile(hSerial, response, sizeof(response) - 1, &bytes_read, NULL)) {
        fprintf(stderr, "ERRO: Falha ao ler da porta serial.\n");
        return;
    }

    if (bytes_read > 0) {
        response[bytes_read] = '\0';
        printf("   Eco recebido: %s\n", response);
    } else {
        printf("   Nenhuma resposta recebida.\n");
    }
}

void display_menu() {
    printf("\n--- Menu de Comandos ---\n");
    printf("1. Definir Posicao (p)\n");
    printf("2. Definir Ganho Proporcional (g)\n");
    printf("3. Definir Ganho Integral (i)\n");
    printf("4. Definir Ganho Derivativo (d)\n");
    printf("5. Enviar Comando Home (h)\n");
    printf("6. Sair\n");
    printf("Escolha uma opcao: ");
}
