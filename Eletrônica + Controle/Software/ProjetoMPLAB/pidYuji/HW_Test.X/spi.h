/* 
 * File:     spi.h 
 * Author:   Bruno Alan Miyamoto
 * Date:     7/02/2016
 * Comments: Controla interface SPI
 * Revision history: 
 */

#ifndef SPI_H
#define	SPI_H

#include <xc.h> 
#include <stdint.h>

void spi_init(void); ///< inicializa o spi no modo 0,0 master

uint8_t spi_exchange(uint8_t data); ///< transmite e recebe por spi

uint8_t spi_read(void); ///< lê byte pelo SPI

void spi_write(uint8_t data); ///< escreve byte pelo SPI

#endif