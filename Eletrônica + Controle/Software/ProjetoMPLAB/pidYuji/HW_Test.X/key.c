/* 
 * File:     key.c 
 * Author:   Jun Okamoto Jr.
 * Date:     7/02/2016
 * Comments: Controla leitura de chave
 * Revision history: 
 */

#ifndef KEY_C
#define	KEY_C

#include "always.h"
#include "key.h"

#define KEY RB6           // bit de entrada de chave

// variáveis globais
volatile char keyPressed;        // chave pressionada
volatile char debounce;         // contador usado para debounce da chave
volatile char keyStateChanged;  // marca mudança de estado da chave de H-L ou L-H

///
/// Inicializa uso da chave por interrupção-na-mudança da porta B.
/// Por enquanto só para bit 6.
///
void key_init(void) {
  nRBPU = 0;   // permite usar pull-ups no Port B
  TRISB6 = 1;  // bit 6 da porta B é entrada chave
//  TRISB |= 1 << 6;
  WPUB6 = 1;   // weak pull-up enabled para chave
  IOCB6 = 1;   // interrupt on change enabled
  RBIE = 1;    // habilita interrupção da Porta B
}

///
/// Retira o bounce da chave dando um tempo controlado pelo parâmetro cycles
/// O período de debounce deve ser de 5 a 10 ms.
/// Essa rotina deve ser colcada dentre de uma interrução periódica de algum Timer.
/// Para uma interrupção periódica de 5 ms cycles é 2 o que dá 5 a 10 ms.
/// cycles deve ser alterado de acordo com o período de interrupção do
/// timer onde a rotina está incluída.
/// @param cycles número de vezes que a interrupçào deve ocorrer para dar 
///               cerca de 10 ms.
///
void key_debounce(int cycles) {
  if (++debounce >= cycles) {  // espera no. de ciclos para dar de 5 a 10 ms
    debounce = 0;              // reseta contador de debounce
    keyStateChanged = FALSE;   // reseta estado de mudança da chave
  } // fim - debounce da chave

}

///
/// Faz a leitura da chave.
/// Essa rotina deve ser colocada numa interrupção-na-mudança da porta B.
/// @param port valor lido da porta
///
void key_read(char port) {
  static char key_old = 1;  // valor anterior da chave (1 é o estado inativo)

  // Trata chave
  char key =  (port & 0b01000000) >> 6; // retira o bit 6 que corresponde a chave e coloca com bit menos significativo
  if (key == 0 && key_old == 1) { // detecta borda de subida
    if (!keyStateChanged) { // passou o periodo de debounce e a chave pode ser tratada
      keyPressed = TRUE; // marca como pressionada
      keyStateChanged = TRUE; // marca como mudança de estado
      debounce = 0; // reseta debounce
      key_old = key;
    }
  }
  if (key == 1 && key_old == 0) { // detrecta borda de descida
    keyPressed = FALSE; // marca com não pressionada
    keyStateChanged = TRUE;  // marca como mudança de estado
    debounce = 0; // reseta debounce
    key_old = key;
  }  
}

///
/// Testa se a chave está pressionada. Se a chave estiver pressionada
/// reseta o seu estado para não acionada, com isso detecta só a borda.
/// Essa rotina deve ser colocada no ponto do programa onde se deseja
/// testar se a chave foi pressionada.
/// @return state TRUE acionada; FALSE não acionada
///
char key_pressed(void) {
  char state = FALSE;       // estado inicial é não pressionada
  if (keyPressed == TRUE) { // se a variável global estiver setada
    keyPressed = FALSE;     // reseta o estado da variável
    state = TRUE;           // muda o estado para pressionada
  }
  return state;             // retorna o estado da chave
}
#endif
