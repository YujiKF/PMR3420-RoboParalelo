#define DEBUG // comentar se não debug

#include <xc.h>
#include "always.h"

#include "protocol.h"
#include "serial.h"
#include <stdio.h>

// protocol states
#define HUNTING_SOT 0
#define HUNTING_MY_ADDRESS 1
#define HUNTING_CMD 2
#define HUNTING_EOT 3
#define MESSAGE_READY 4

// misc
#define NO_CHAR 255
#define SOT_CHAR ':'
#define EOT_CHAR ';'

// internal storage
unsigned char pro_myAddress;
unsigned char pro_incoming[MAX_LEN+2];
unsigned char pro_status;
unsigned char pro_ptr;

_MESSAGE completeMessage;


/*
   Auxiliary functions 
*/

// descomentar para teste sem serial
//extern unsigned char chkchr_test(void); // para teste sem serial

void cleanupBuffer(void) {
  unsigned char i;
  for (i=0; i<MAX_LEN; i++) {
    pro_incoming[i] = 0;
    completeMessage.value[i]=0;
  }
  pro_incoming[MAX_LEN] = 0;
  pro_incoming[MAX_LEN+1] = 0;
  pro_ptr = 0;
} // cleanupBuffer


void framingError(void) {
  pro_status = HUNTING_SOT;
  cleanupBuffer();
} // framingError

int isValidCmd(unsigned char aChar) {
   if ( (aChar == 'p') ||
        (aChar == 'h') ||
        (aChar == 'g') ||
        (aChar == 'i') ||
        (aChar == 'd'))
      return TRUE;
   return FALSE;
} // isValidCmd

void addToIncomingBuffer(unsigned char aChar) {
  pro_incoming[pro_ptr] = aChar;
  pro_ptr++;
} // addToIncomingBuffer

unsigned char toMsgType(unsigned char aChar) {
  if (aChar == 'p')
    return PRO_SET_POSITION;
  if (aChar == 'h')
    return PRO_SET_HOME;
  if (aChar == 'g')
    return PRO_SET_PROPORTIONAL_GAIN;
  if (aChar == 'i')
    return PRO_SET_INTEGRAL_GAIN;
  if (aChar == 'd')
    return PRO_SET_DERIVATIVE_GAIN;
  return PRO_NO_MESSAGE;
} // toMsgType


int isValid(unsigned char aChar) {
   if (pro_ptr >= MAX_LEN) 
      return FALSE;
   if ( (aChar == '-') ||
        (aChar == '.') ||
        ((aChar >= '0')&&(aChar <= '9')) ) 
      return TRUE;
   return FALSE;
   
} // isValid

/************************************************************
   pro_getMessage
*/
_MESSAGE pro_getMessage(void) {
  unsigned char aChar;

  if (pro_status == MESSAGE_READY) {
    pro_status = HUNTING_SOT;
  }

  completeMessage.messageType = PRO_NO_MESSAGE;

  aChar = chkchr(); // comentar para teste sem serial
  // for protocol test:
//  aChar = chkchr_test(); // para loop sem usar recepção serial

  if (aChar != NO_CHAR) {  // IF_THEN instead of SWITCH is faster
#ifdef DEBUG
    putch(aChar);  // [jo:231021] echo para testes
#endif    
    switch (pro_status) {
      case HUNTING_SOT:
        if (aChar == SOT_CHAR) {
          pro_status = HUNTING_MY_ADDRESS;
        } else {
          framingError();
        }
        break;
      case HUNTING_MY_ADDRESS:
        if (aChar == pro_myAddress) {
          cleanupBuffer(); 
          pro_status = HUNTING_CMD;
        } else {
          framingError();
        }
        break;
      case HUNTING_CMD:
        if (isValidCmd(aChar)) {
           addToIncomingBuffer(aChar);
           pro_status = HUNTING_EOT;
        } else {
           framingError();
        }
        break;
      case HUNTING_EOT:
        if (aChar == EOT_CHAR) {
          completeMessage.messageType = toMsgType(pro_incoming[0]);
#ifdef DEBUG
          putch('\n'); // [jo:240322] para testes
#endif
          for (unsigned char i = 0; i < MAX_LEN - 1; i++) {
            completeMessage.value[i] = pro_incoming[i+1];
#ifdef DEBUG
            putch(completeMessage.value[i]); // [jo:240321] para testes
#endif
          }
          pro_status = MESSAGE_READY;
        } else {
          if (isValid(aChar)) {
            addToIncomingBuffer(aChar);
          } else {
            framingError();
          }
        }
        break;
      default:
         framingError();
    } // switch
  } else {
    clear_usart_errors();
  }     
  return completeMessage;
} // pro_getMessage

/*
   pro_init
*/
void pro_init(void) {
   pro_status = HUNTING_SOT;
   completeMessage.messageType = PRO_NO_MESSAGE;
   cleanupBuffer();
   ser_init();
} // pro_init

/*
   pro_setMyId
*/
void pro_setMyId(unsigned char id) {
  pro_myAddress = id;
} // pro_setMyId
 


