/* mbed Microcontroller Library
 * Copyright (c) 2019 ARM Limited
 * SPDX-License-Identifier: Apache-2.0
 */

#include "mbed.h"

DigitalOut      led1(LED1);
InterruptIn     bpToSend(BUTTON1);

UnbufferedSerial        my_pc(USBTX, USBRX);
char    message[128];
char    data_to_send[5] = {0x10, 0x20, 0x35, 0x65, 0x50};

char data;

void ISR_my_pc_reception(void);
void ISR_my_pc_transmit(void);

int main()
{    
    my_pc.baud(115200);
    my_pc.attach(&ISR_my_pc_reception, UnbufferedSerial::RxIrq);
    bpToSend.fall(&ISR_my_pc_transmit);

    while (true)
    {}
}

void ISR_my_pc_reception(void){
    my_pc.read(&data, 1);
    if(data == 'a'){    led1 = 1;   } 
    if(data == 'e'){    led1 = 0;   }    
    my_pc.write(&data, 1);
}

void ISR_my_pc_transmit(void){
    my_pc.write(data_to_send, 5);
}