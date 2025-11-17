#include <wiringPi.h>
#include <wiringSerial.h>

int main() {
    int fd = serialOpen("/dev/serial0", 9600);
    serialPuts(fd, "Hello UART\n");
    serialClose(fd);
    return 0;
}
