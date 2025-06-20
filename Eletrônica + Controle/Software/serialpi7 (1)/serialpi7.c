#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// =================================================================
//                      CONFIGURAÇÕES
// =================================================================
// Altere "\\\\.\\COMx" para a sua porta serial.
// Verifique no "Gerenciador de Dispositivos" do Windows.
#define SERIAL_PORT_NAME "\\\\.\\COM3"

// Taxa de comunicação para a aplicação, conforme a documentação
#define BAUD_RATE CBR_19200

// Função para enviar o comando, respeitando o protocolo do PIC
void sendCommandToPIC(HANDLE hSerial, const char* command) {
    DWORD bytes_written;
    size_t len = strlen(command);
    
    printf("-> Enviando comando: %s\n", command);

    // O protocolo do PI-7 exige um delay de 1ms entre cada caractere
    for (size_t i = 0; i < len; ++i) {
        if (!WriteFile(hSerial, &command[i], 1, &bytes_written, NULL)) {
            fprintf(stderr, "ERRO: Falha ao escrever na porta serial.\n");
            return;
        }
        Sleep(1); 
    }
    printf("   Comando enviado com sucesso.\n");
}

int main() {
    HANDLE hSerial;
    DCB dcbSerialParams = {0};

    // 1. Abrir a Porta Serial
    hSerial = CreateFileA(SERIAL_PORT_NAME, GENERIC_WRITE, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);

    if (hSerial == INVALID_HANDLE_VALUE) {
        fprintf(stderr, "ERRO: Nao foi possivel abrir a porta %s. Verifique se esta correta e nao esta em uso.\n", SERIAL_PORT_NAME);
        system("pause"); // Pausa para o usuário ler o erro
        return 1;
    }

    // 2. Configurar a Porta Serial
    dcbSerialParams.DCBlength = sizeof(dcbSerialParams);
    if (!GetCommState(hSerial, &dcbSerialParams)) {
        fprintf(stderr, "ERRO ao obter configuracoes da porta.\n");
        CloseHandle(hSerial);
        return 1;
    }

    dcbSerialParams.BaudRate = BAUD_RATE;
    dcbSerialParams.ByteSize = 8;
    dcbSerialParams.StopBits = ONESTOPBIT;
    dcbSerialParams.Parity   = NOPARITY;

    if (!SetCommState(hSerial, &dcbSerialParams)) {
        fprintf(stderr, "ERRO ao definir configuracoes da porta.\n");
        CloseHandle(hSerial);
        return 1;
    }

    // 3. Loop Principal
    printf("--- Terminal de Teste em C para PIC (PI-7) ---\n");
    printf("Conectado a %s. Digite os comandos (ex: p30.0, ag1.2) ou 'exit' para sair.\n", SERIAL_PORT_NAME);
    printf("-------------------------------------------------\n");

    char input_buffer[256];
    char command_buffer[260];

    while (1) {
        printf("Comando para o PIC 'a' > a");
        if (fgets(input_buffer, sizeof(input_buffer), stdin) == NULL) {
            break;
        }

        input_buffer[strcspn(input_buffer, "\r\n")] = 0;

        if (stricmp(input_buffer, "exit") == 0 || stricmp(input_buffer, "quit") == 0) {
            break;
        }

        // Monta o comando completo no formato do protocolo ":a<comando>;"
        snprintf(command_buffer, sizeof(command_buffer), ":a%s;", input_buffer);
        
        sendCommandToPIC(hSerial, command_buffer);
    }

    // 4. Fechar a porta
    CloseHandle(hSerial);
    printf("Porta serial fechada. Encerrando.\n");
    return 0;
}