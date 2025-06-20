#ifndef PROTOCOL_H
#define PROTOCOL_H

/* PROTOCOL FRAME FORMAT
   <SOT><ADDR+CMD><VALUE><EOT>
   where
   <SOT> start of text. Always ´:´ 0x3A
   <ADDR> address in the form with 0x4x
              station 1 is 0x41 (a)
              station 2 is 0x42 (b)
   <CMD> command. 
          'p' for position
          ´h´ for home
          ´g´ for proportional gain
          ´d´ for derivative gain
          ´i´ for integral gain
   <VALUE> [-]<digits_or_dot>
   <EOT> end of text. Always ´;´ 0x3B

   Example: 
      set position of station 1 to -100. 
      :ap-100;
      0x3A 0x41 0x2D 0x31 0x30 0x30 0x3B

      set proportional gain of station 2 to 0.32
      :bg0.32;
*/

#include "pid.h"

/* Message types */
#define PRO_NO_MESSAGE 0
#define PRO_SET_POSITION 1
#define PRO_SET_HOME 2
#define PRO_SET_PROPORTIONAL_GAIN 3
#define PRO_SET_INTEGRAL_GAIN 4
#define PRO_SET_DERIVATIVE_GAIN 5

/* _MESSAGE datatype */
#define MAX_LEN 10
typedef struct {
  unsigned char messageType;
  unsigned char value[MAX_LEN];
} _MESSAGE;


extern void pro_init(void);
extern _MESSAGE pro_getMessage(void);
extern void pro_setMyId(unsigned char id);

#endif
