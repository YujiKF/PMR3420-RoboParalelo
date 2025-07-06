/* 
 * File:      led_rgb.h
 * Author:    Jun Okamoto Jr.
 * Date:      11/03/2016
 * Comments:  Controla do LED RGB do robô pela interface SPI
 * Revision history:
 */
 
#ifndef LED_RGB_H
#define	LED_RGB_H

#include <xc.h> // include processor files - each processor file is guarded. 

#define BLACK   0
#define BLUE    1
#define GREEN   2
#define CYAN    3
#define RED     4
#define MAGENTA 5
#define YELLOW  6
#define WHITE   7

void led_rgb_init(void); ///< inicializa LED RGB, utiliza SPI

void led_rgb_set_color(char led_color); ///< define cor do led, inclusive apagado

void led_rgb_set_red_level(uint8_t level); ///< define a intensidade do canal vermelho

void led_rgb_set_green_level(uint8_t level); ///< define a intensidade do canal verde

void led_rgb_set_blue_level(uint8_t level); ///< define a intensidade do canal azul

#endif	/* LED_RGB_H */

