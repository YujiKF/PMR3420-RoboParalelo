//*****************
//function prototypes

void ser_init(void);
#ifndef __CLANG__ // [jo:240316] para compatibilidade com C90
void putch(char c);
char getch(void);
#endif
void putst(register const char * str);
unsigned char usart_timeout(void);
unsigned char getch_timeout(void);  // [jo:091211]
unsigned char chkchr(void);         // [jo:091211]
void putchdec(unsigned char c);
void putchhex(unsigned char c);
void putinthex(unsigned int c);
void clear_usart_errors(void);

#define putlf putst("\n") //put line feed



