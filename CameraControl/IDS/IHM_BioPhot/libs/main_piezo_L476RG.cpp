
#include "mbed.h"
#include <cstdint>

#define     _VERSION_       "01"
#define     ADC_LEVELS      4000

#define WAIT_TIME_MS 500 
DigitalOut  led1(LED1);

/* Piezo Hardware Link */
BufferedSerial      myLink(USBTX, USBRX);
char                command[10];
char                transmitData[20];
uint8_t             usbDataCpt;
uint8_t             endReceived;
char                commandReceived;
bool                connected;
/* Initialize USB Link to computer interface */
void    initUSBLink(void);
/* Interrupt SubRoutine on USB receiving */
void    ISR_usb(void);
/* Test if data is received */
bool    isDataReady(void);
/* Data is treated */
void    resetDataReady(void);
/* Process command received */
void    processCommand(void);
/* Piezo Control */
AnalogOut           myPiezoOut(A2);
uint16_t            pos_um;
uint16_t            pos_nm;
/* Initialize Piezo position */
void    initPiezo(void);
/* Move piezo */
void    movePiezo(uint16_t um, uint16_t nm);

/* List of commands */
#define     CMD_CONNECT     'C'
#define     CMD_IS_CONN     'I'
#define     CMD_DISCONN     'D'
#define     CMD_VERSION     'V'
#define     CMD_GET_POS     'G'
#define     CMD_SET_POS     'M'



/* MAIN PROGRAM */
int main()
{
    initUSBLink();
    initPiezo();

    while (true)
    {
        if(isDataReady() == true){
            processCommand();
            resetDataReady();
        }
        wait_us(1000);
    }
}


/* Initialize USB Link to computer interface */
void initUSBLink(void){
    myLink.set_baud(115200);
    myLink.sigio(callback(ISR_usb));
    usbDataCpt = 0;
    endReceived = 0;
    connected = false;
}

/* Interrupt SubRoutine on USB receiving */
void ISR_usb(void){
	// Récupération de la donnée sur la liaison série
    char data = '_';
    if(myLink.readable()){
        myLink.read(&data, 1);
    }
	// Détection du premier octet ('_')
    if(data == '_')
        usbDataCpt = 0;
    else
        usbDataCpt++;
	// Stocktage de la donnée reçue
    command[usbDataCpt] = data;
    // End of the transmission
	if(data == '!'){
        led1 = !led1;
        endReceived = 1;
        commandReceived = command[1];
    }
}

/* Test if data is received */
bool    isDataReady(void){
    if(endReceived == 1){
        return true;
    }
    else {
        return false;
    }
}

/* Data is treated */
void    resetDataReady(void){
    endReceived = 0;
}


/* Process command received */
void    processCommand(void){
    switch(commandReceived){
        case    CMD_CONNECT:
            sprintf(transmitData, "_C1!");
            connected = true;
            myLink.write(transmitData, 4);
            break;
        case    CMD_IS_CONN:
            if(connected == true)
                sprintf(transmitData, "_I1!");
            else
                sprintf(transmitData, "_I0!");
            myLink.write(transmitData, 4);
            break;
        case    CMD_DISCONN:
            sprintf(transmitData, "_D1!");
            connected = false;
            myLink.write(transmitData, 4);
            break;
        case    CMD_GET_POS:
            if(connected == true){
                sprintf(transmitData, "_G%2d.%3d!", pos_um, pos_nm);
                myLink.write(transmitData, 9);
            }
            else{
                sprintf(transmitData, "_I0!");
                myLink.write(transmitData, 4);
            }
            break;
        case    CMD_SET_POS:
            if(connected == true){
                // process data
                pos_um = 0;
                pos_nm = 0;
                // sscanf(command, "_S%2d.%3d", &pos_um, &pos_nm);
                if(command[2] != ' ')
                    pos_um += (command[2]-'0') * 10;
                if(command[3] != ' ')
                    pos_um += (command[3]-'0') * 1;
                if(command[5] != ' ')
                    pos_nm += (command[5]-'0') * 100;
                if(command[6] != ' ')
                    pos_nm += (command[6]-'0') * 10;
                if(command[7] != ' ')
                    pos_nm += (command[7]-'0') * 1;

                if(pos_um == 10) pos_nm = 0;

                movePiezo(pos_um, pos_nm);
                // sending ack
                sprintf(transmitData, "_M1!");
                myLink.write(transmitData, 4);
            }
            else{
                sprintf(transmitData, "_I0!");
                myLink.write(transmitData, 4);
            }

            break;
        case    CMD_VERSION:
            if(connected == true){
                sprintf(transmitData, "_V%s!", _VERSION_);
                myLink.write(transmitData, 5);
            }            
            else{
                sprintf(transmitData, "_I0!");
                myLink.write(transmitData, 4);
            }
            break;
        default:
            if(connected == true)
                sprintf(transmitData, "_I1!");
            else
                sprintf(transmitData, "_I0!");
            myLink.write(transmitData, 4);
            break;
            break;
    }
}

/* Initialize Piezo position */
void    initPiezo(void){
    pos_nm = 0;
    pos_um = 0;
    movePiezo(pos_um, pos_nm);
}

/* Move piezo */
void    movePiezo(uint16_t um, uint16_t nm){
    // TO DO SET TO POSITION
    uint16_t    adc_val = 0;

    // Total motion : 10 um
    if(um < 10){
        adc_val += um * ADC_LEVELS / 10.0;
        if(nm < 1000){
            adc_val += nm / 1000.0 * ADC_LEVELS / 10.0;
        }
    }
    else{
        adc_val = 4000;
    }
    myPiezoOut.write_u16(adc_val << 4);
}