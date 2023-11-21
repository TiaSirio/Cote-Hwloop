/*
 *  Displays voltage and current sensors for CubeSatSim
 *
 *  uses python3 code ina219.py
 *
 *  REMEMBER TO COMPILE WITH "-lwiringPi"
 *
 */

#include "main.h"
#include <unistd.h>
#include <sys/time.h>
#include <inttypes.h>

int64_t current_timestamp();

int main(int argc, char *argv[]) {
  int debug = OFF;
  char *filePayload;
  if (argc > 1) {
    filePayload = argv[1];
    if (argc > 2) {
        if ( * argv[2] == 'd') {
            debug = ON;
        }
    }
  }

  //char cmdbuffer[1000];
  //FILE *file1;
  //int count1;
  //int i;
  //int j;
  //char *token;
  //const char space[2] = " ";
  //float voltage[9], current[9];

  //for (i = 0; i < 10; i++){
      //printf("CubeSatSim v1.2 INA219 Voltage and Current Telemetry - Iteration: %d\n", i);
      //map[MINUS_X] = MINUS_Y;
      //map[PLUS_Z] = MINUS_X;
      //map[MINUS_Y] = PLUS_Z;
      //snprintf(busStr, 10, "%d %d", test_i2c_bus(1), test_i2c_bus(3));

//  Reading I2C voltage and current sensors
//   printf("Starting\n");

	
	
	
	
	
	 // don't test for payload if AX5043 is present or CW or SSTV modes
    FILE *fptr;
    //fptr = fopen("/home/pi/CubeSatSim/simulationFiles/nonFuncData/non_func_payload.txt", "a");

    payload = OFF;

    if ((uart_fd = serialOpen("/dev/ttyAMA0", 115200)) >= 0) {  // was 9600
      char c;
      int charss = (char) serialDataAvail(uart_fd);
      if (charss != 0)
        //printf("Clearing buffer of %d chars \n", charss);
      while ((charss--> 0))
        c = (char) serialGetchar(uart_fd); // clear buffer

      unsigned int waitTime;
      int i;
      for (i = 0; i < 2; i++) {
	if (payload != ON) {
          serialPutchar(uart_fd, 'R');
          //printf("Querying payload with R to reset\n");
          waitTime = millis() + 500;
          while ((millis() < waitTime) && (payload != ON)) {
            if (serialDataAvail(uart_fd)) {
              printf("%c", c = (char) serialGetchar(uart_fd));
              fflush(stdout);
              if (c == 'O') {
                printf("%c", c = (char) serialGetchar(uart_fd));
                fflush(stdout);
                if (c == 'K')
                  payload = ON;
              }
            }
            printf("\n");
            //        sleep(0.75);
          }
        }
      }
      if (payload == ON)  {
        //printf("\nSTEM Payload is present!\n");
	sleep(2);  // delay to give payload time to get ready
      }
      else {
        printf("\nSTEM Payload not present!\n -> Is STEM Payload programed and Serial1 set to 115200 baud?\n");
      }
    } else {
      fprintf(stderr, "Unable to open UART: %s\n -> Did you configure /boot/config.txt and /boot/cmdline.txt?\n", strerror(errno));
    }
	
	
	
	
	

	
	
	
	
	


  char c;
  unsigned int waitTime;
  int i, end, trys = 0;
  sensor_payload[0] = 0;
  sensor_payload[1] = 0;

  //for (int i = 0; i < 10; i++){
  while(payload == ON) {
    if (payload == ON) {  // -55
        STEMBoardFailure = 0;

  
        char c;
        unsigned int waitTime;
	int i, end, trys = 0;
	sensor_payload[0] = 0;
	sensor_payload[1] = 0;
	while (((sensor_payload[0] != 'O') || (sensor_payload[1] != 'K')) && (trys++ < 10)) {	      
          i = 0;
	  serialPutchar(uart_fd, '?');
	  sleep(0.05);  // added delay after ?
          //printf("%d Querying payload with ?\n", trys);
          waitTime = millis() + 500;
          end = FALSE;
          //  int retry = FALSE;
          while ((millis() < waitTime) && !end) {
            int chars = (char) serialDataAvail(uart_fd);
            while ((chars > 0) && !end) {
//	      printf("Chars: %d\ ", chars);
	      chars--;
	      c = (char) serialGetchar(uart_fd);
              //	printf ("%c", c);
              //	fflush(stdout);
              if (c != '\n') {
                sensor_payload[i++] = c;
              } else {
                end = TRUE;
              }
            }
          }
	
          sensor_payload[i++] = ' ';
          //  sensor_payload[i++] = '\n';
          sensor_payload[i] = '\0';
          //printf(" Response from STEM Payload board: %s\n", sensor_payload);
	  sleep(0.1);  // added sleep between loops
	}
        if ((sensor_payload[0] == 'O') && (sensor_payload[1] == 'K')) // only process if valid payload response
        {
	  //printf("Timestamp: %" PRId64 "\n", current_timestamp());
          //printf("Timestamp: %d", current_timestamp());
	  int count1;
          char * token;
 
          const char space[2] = " ";
          token = strtok(sensor_payload, space);
          for (count1 = 0; count1 < 17; count1++) {
            if (token != NULL) {
              sensor[count1] = (float) atof(token);
              #ifdef DEBUG_LOGGING
              //  printf("sensor: %f ", sensor[count1]);
              #endif
              token = strtok(NULL, space);
            }
          }
          //printf("\n");
        }
	else
		payload = OFF;  // turn off since STEM Payload is not responding
      }
      if ((sensor_payload[0] == 'O') && (sensor_payload[1] == 'K')) {
	fptr = fopen(filePayload, "a");
        fprintf(fptr, "%" PRId64 ",", current_timestamp());
	for (int count1 = 0; count1 < 17; count1++) {
	  if(count1 != 16){
	    fprintf(fptr, "%.3f,", sensor[count1]);
	  } else {
	    fprintf(fptr, "%.3f\n", sensor[count1]);
	  }
	/*
          if (sensor[count1] < sensor_min[count1])
            sensor_min[count1] = sensor[count1];
          if (sensor[count1] > sensor_max[count1])
            sensor_max[count1] = sensor[count1];
	*/
            //  printf("Smin %f Smax %f \n", sensor_min[count1], sensor_max[count1]);
        }
	fclose(fptr);
	//fflush(fptr);
      }
    }
     /*
     printf("\n");

     printf("+X  | % 4.2f V % 5.0f mA \n", voltage[map[PLUS_X]], current[map[PLUS_X]]);
     printf("+Y  | % 4.2f V % 5.0f mA \n", voltage[map[PLUS_Y]], current[map[PLUS_Y]]);
     printf("+Z  | % 4.2f V % 5.0f mA \n", voltage[map[PLUS_Z]], current[map[PLUS_Z]]);
     printf("-X  | % 4.2f V % 5.0f mA \n", voltage[map[MINUS_X]], current[map[MINUS_X]]);
     printf("-Y  | % 4.2f V % 5.0f mA \n", voltage[map[MINUS_Y]], current[map[MINUS_Y]]);
     printf("-Z  | % 4.2f V % 5.0f mA \n",  voltage[map[MINUS_Z]], current[map[MINUS_Z]]);
     printf("Bat | % 4.2f V % 5.0f mA \n", voltage[map[BAT]], current[map[BAT]]);
     printf("Bus | % 4.2f V % 5.0f mA \n\n", voltage[map[BUS]], current[map[BUS]]);
      */
      //fclose(file1);
     // sleep(5);
  //}

  return 0;
}
/*
int test_i2c_bus(int bus)
{
	int output = bus; // return bus number if OK, otherwise return -1
	char busDev[20] = "/dev/i2c-";
	char busS[5];
	snprintf(busS, 5, "%d", bus);
	strcat (busDev, busS);	
//	printf("Bus Dev String: %s \n", busDev);
	
	if (access(busDev, W_OK | R_OK) >= 0)  {   // Test if I2C Bus is present
//	  	printf("bus is present\n\n");	    
    	  	char result[128];		
    	  	const char command_start[] = "timeout 10 i2cdetect -y ";
		char command[50];
		strcpy (command, command_start);
    	 	strcat (command, busS);
//     	 	printf("Command: %s \n", command);
    	 	FILE *i2cdetect = popen(command, "r");
	
    	 	while (fgets(result, 128, i2cdetect) != NULL) {
    	 		;
//       	 	printf("result: %s", result);
    	 	}	
    	 	int error = pclose(i2cdetect)/256;
//      	 	printf("%s error: %d \n", &command, error);
    	 	if (error != 0) 
    	 	{	
    	 		printf("ERROR: %d bus has a problem \n  Check I2C wiring and pullup resistors \n", bus);
			output = -1;
    		}								
	} else
	{
    	 	printf("ERROR: %d bus has a problem \n  Check software to see if enabled \n", bus);
		output = -1; 
	}
	return(output);	// return bus number or -1 if there is a problem with the bus
}

// code by https://stackoverflow.com/questions/25161377/open-a-cmd-program-with-full-functionality-i-o/25177958#25177958

    FILE *sopen(const char *program)
    {
        int fds[2];
        pid_t pid;

        if (socketpair(AF_UNIX, SOCK_STREAM, 0, fds) < 0)
            return NULL;

        switch(pid=vfork()) {
        case -1:    // Error
            close(fds[0]);
            close(fds[1]);
            return NULL;
        case 0:     // child
            close(fds[0]);
            dup2(fds[1], 0);
            dup2(fds[1], 1);
            close(fds[1]);
            execl("/bin/sh", "sh", "-c", program, NULL);
            _exit(127);
        }
        // parent
        close(fds[1]);
        return fdopen(fds[0], "r+");
    }
*/
/*
int current_timestamp(){
	struct timespec time;
	clock_gettime(CLOCK_MONOTONIC_RAW, &time);
	//gettimeofday(&te, NULL);
	//long long milliseconds = te.tv_sec*1000LL + te.tv_usec/1000;
	int milliseconds = (time.tv_sec) * 1000 + (time.tv_nsec) / 1000000;
	return milliseconds;
}
*/

int64_t current_timestamp(){
	struct timeval time;
	gettimeofday(&time, NULL);
	int64_t s1 = (int64_t)(time.tv_sec) * 1000;
	int64_t s2 = (time.tv_usec / 1000);
	return s1 + s2;
}
