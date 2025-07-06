/* 
 * File:     lcd8x2.c 
 * Authors:  Jun Okamoto Jr.
 *           Bruno Alan Miyamoto
 * Date:     7/02/2016
 * Comments: Controle do display LCD 8x2 do robô
 * Revision history: 
 *  13/06/2024 - chama spi_init() no init daqui
 */

#ifndef LCD8X2_C
#define LCD8X2_C

#include "lcd8x2.h"
#include "always.h"
#include "spi.h"

#define LCD_DEVICE_CODE 2 // Código do LCD 8x2 no robô
#define DATA_READY RB0    // Pino de entrada para receber indicação de data pronto para recepção

///
/// Inicializa LCD
///
void lcd_init(void) {
  TRISB0 = INPUT;    // inicializa RB0 como entrada para receber DATA READY
  ANS12 = DIGITAL;   // RB0 não é analógico
  spi_init();  // [jo:240713] SPI deve ser inicializado antes para o LCD funcionar
}

///
/// Envia comando para interface SPI que controla display
/// @param: command  - no formato dddccccc
///                    onde bbb é o código do display 8x2 no robô
///                    ccccc é o código do comando
///
void spi_send_command(uint8_t command) {
  uint8_t command_byte;
  command_byte = LCD_DEVICE_CODE << 5; // os 3 bits mais significativos são o dispositivo
  command_byte |= command;    // o comando se existir está nos 5 bits menos significativos
  spi_exchange(command_byte); // traca um byte por SPI
}

///
/// Envia um byte que complementa o comando em alguns casos
/// @param: data - corresponde a um 2o. byte de um comando
///
void spi_send_data(uint8_t data) {
  spi_exchange(data); // envia dado de 8-bits como segundo byte
}

///
/// 	Limpa LCD
///
void lcd_clear(void) {
  spi_send_command(2); // 2 - clear
}

///
/// Move o cursor para a posição pos no display. Cada linha do display
/// possui 40 posições
/// @param: pos - posição no display,
///               0 - 39   linha 1
///               64 - 103 linha 2
///
void lcd_goto(uint8_t pos) {
  spi_send_command(17); // 17 - move cursor to
  spi_send_data(pos);   // nova posição do cursor
}

/// 
/// Liga/desliga cursor
/// @param: on - 0: cursor desligado; 1: cursor ligado
///
void lcd_show_cursor(int on) {
  if (on) {          // se on for true - liga
    spi_send_command(5); // 5  - turn on cursor
  } else {           // se on for false - desliga
    spi_send_command(6); // 6 - turn off cursor
  }
}

///
/// Escreve um caracter no display
/// @param: c - caracter a ser mostrado no display
///
void lcd_putchar(char c) {
  spi_send_command(18); // 18 - put char
  spi_send_data(c);
}

///
/// Escreve um string no display
/// @param: s - string a ser mostrado no display
///
void lcd_puts(const char * s) {
  while(*s)
    lcd_putchar(*s++);
}

///
/// Desloca o display na direção dir
/// @param: dir - 0 desloca para a direita
///               1 desloca para a esquerda
///
void lcd_set_display_movement(uint8_t dir) {
  if (dir) {
    spi_send_command(14);
  } else {
    spi_send_command(13);
  }
}

///
/// Define a direção de deslocamento do cursor
/// @param: dir - 0 desloca para a direita
///               1 desloca para a esquerda
///
void lcd_set_cursor_movement(uint8_t dir) {
  if (dir) {
    spi_send_command(11);
  } else {
    spi_send_command(12);
  }
}

///
/// Lê a posição do cursor
/// @return: posição do cursor 0 - 39, 64 - 103
///
uint8_t lcd_get_cursor_position() {
  uint8_t pos;
  spi_send_command(15);
  while (!DATA_READY); // espera os dados estarem prontos para leitura
  pos = spi_exchange(0x00);  // envia 0x00 para ler um byte
  return pos;
}

#endif
