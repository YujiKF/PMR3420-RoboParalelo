/* 
 * File:     lcd8x2.h 
 * Authors:  Jun Okamoto Jr.
 *           Bruno Alan Miyamoto
 * Date:     7/02/2016
 * Comments: Controle do display LCD 8x2 do robô
 * Revision history: 
 */

#ifndef LCD8X2_H
#define LCD8X2_H

#include <xc.h>
#include <stdint.h>

extern void lcd_init(void); ///< inicializa display, utiliza SPI

extern void lcd_clear(void); ///< limpa e coloca cursor na linha 1 coluna 1

extern void lcd_puts(const char * s); ///< escreve um string de caracteres no LCD

extern void lcd_goto(uint8_t pos); ///< move o cursor para determinada posição

extern void lcd_show_cursor(int on); ///< desliga ou liga cursor

extern void lcd_putchar(char c); ///< escreve um caracter no LCD

extern void lcd_set_display_movement(uint8_t dir); ///< desloca display para direita ou esquerda

extern uint8_t lcd_get_cursor_position(); ///< retorna a posição do cursor

extern void lcd_set_cursor_movement(uint8_t dir); ///< move o cursor para direita ou esquerda

extern void lcd_passthrough_command(uint8_t command); ///< passa comando direto para LCD

extern void lcd_passthrough_data(uint8_t data); ///< passa dado diretor para LCD

#endif