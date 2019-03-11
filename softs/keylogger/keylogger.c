#include "keylogger.h"

void intHandler(int dummy) {
    printf("Killed [%d]\n", dummy);
    fflush(stdout);
    saveToFile();
    exit(dummy);
}
// TODO: add filename argument
// TODO: pass data as Sample*
void saveToFile(int sampleCount, sample * loggedSamples) {
    FILE * dump = fopen("./dump.csv", "w");
    for (int i = 0 ; i < sampleCount; i++) {
        sample toReg = loggedSamples[i];
        char * aSample = (char *) malloc(27 * sizeof(char));
        sprintf(
            aSample,
            "%011ld%09ld,%03d,%d\n",
            toReg.seconds,
            toReg.nsec,
            toReg.code,
            toReg.state
        );
        fwrite(aSample, sizeof(char), 27, dump);
    }
    fclose(dump);
}

void printSample(sample theSample) {
    const char * state = theSample.state == 2 ? "REPEATED" : (
        theSample.state ? "PRESSED " : "RELEASED"
    );
    printf("%ld%09ld %03d %s\n", theSample.seconds, theSample.nsec, theSample.code, state);
}

void replaySamples(
    int sampleNb,
    sample * loggedSamples,
    struct timeval * loggedTimes
) {
    int kbdFileHandle = open(
        "/dev/input/by-path/platform-i8042-serio-0-event-kbd", O_WRONLY
    );
    struct timeval startTime;
    gettimeofday(&startTime, NULL);
    int sampleCount = 0;

    while (sampleCount < sampleNb) {
        struct timeval endTime;
        gettimeofday(&endTime, NULL);

        long int concat1 = (endTime.tv_sec * 1000000) + endTime.tv_usec;
        long int concat2 = (startTime.tv_sec * 1000000) + startTime.tv_usec;
        long int concat3 = (loggedTimes[sampleCount].tv_sec * 1000000)
            + loggedTimes[sampleCount].tv_usec;

        if (concat1 - concat2 > concat3) {
            sample keyEvt = loggedSamples[sampleCount];

            struct input_event forcedKey;

            forcedKey.type = EV_MSC;
            forcedKey.value = keyEvt.code;
            forcedKey.code = 16;
            gettimeofday(&forcedKey.time, NULL);
            write(kbdFileHandle, &forcedKey, sizeof(struct input_event));

            forcedKey.type = EV_KEY;
            forcedKey.value = keyEvt.state;
            forcedKey.code = keyEvt.code;
            gettimeofday(&forcedKey.time, NULL);
            write(kbdFileHandle, &forcedKey, sizeof(struct input_event));

            forcedKey.type = EV_SYN;
            forcedKey.value = 0;
            forcedKey.code = 0;
            gettimeofday(&forcedKey.time, NULL);
            write(kbdFileHandle, &forcedKey, sizeof(struct input_event));

            gettimeofday(&startTime, NULL);
            sampleCount++;
        }
    }

    close(kbdFileHandle);

    printf("Replay done\n");
}

void keylogSession() {
    struct input_event ev;
    struct timespec spec;
    struct timeval prevTime = {0, 0};

    _Bool isRecording = false;

    int sampleNb = 0;

    /* Disables keyboard events echo in console */
    struct termios termInfo;
    tcgetattr(0, &termInfo);
    termInfo.c_lflag &= ~ECHO;
    tcsetattr(0, 0, &termInfo);

    // Opening keyboard input file
    int kbdFileHandle = open(
        "/dev/input/by-path/platform-i8042-serio-0-event-kbd", O_RDONLY
    );

    sample * loggedSamples;
    loggedSamples = (sample *) calloc(MAX_KEY_EV_SAMPLES, sizeof(sample));

    struct timeval * loggedTimes;
    loggedTimes = (struct timeval *) calloc(
        MAX_KEY_EV_SAMPLES,
        sizeof(struct timeval)
    );

    while(true) {
        // Reading one event from input file
        read(kbdFileHandle, &ev, sizeof (struct input_event));
        // Saving time of event
        clock_gettime(CLOCK_REALTIME, &spec);

        // TODO: cannot record again. Must free previous memory and restart
        if (ev.type == EV_KEY) {
            if (isRecording && ev.code < KEY_F1) {

                // If the first event is a key release, discard it
                if (sampleNb == 0 && ev.value == EV_KEY_RELEASED) {
                } else {
                    sample newSample = { ev.time.tv_sec, ev.time.tv_usec, ev.code, ev.value };
                    loggedSamples[sampleNb] = newSample;

                    struct timeval timeDiff;
                    if (sampleNb == 0) {
                        timeDiff.tv_sec = 0;
                        timeDiff.tv_usec = 0;
                    } else {
                        timeDiff.tv_sec = ev.time.tv_sec - loggedSamples[sampleNb - 1].seconds;
                        timeDiff.tv_usec = ev.time.tv_usec - loggedSamples[sampleNb - 1].nsec;
                    }
                    loggedTimes[sampleNb] = timeDiff;

                    sampleNb++;
                    // Fixed size array guard
                    if (sampleNb >= MAX_KEY_EV_SAMPLES) {
                        printf("More than max samples, killing it\n");
                        exit(1);
                    }
                }
                gettimeofday(&prevTime, NULL);
            }

            // Control sequences for start / stop / replay
            if (ev.code == KEY_F2 && ev.value == EV_KEY_PRESSED) {
                printf(isRecording ? "Stopping " : "Starting ");
                printf("recording...\n");
                isRecording = isRecording ? false : true;
                if (!isRecording) {
                    printf("Saving samples to file");
                    saveToFile(sampleNb, loggedSamples);
                }
            } else if (ev.code == KEY_F3 && ev.value == EV_KEY_PRESSED) {
                printf("Replaying\n");
                replaySamples(sampleNb, loggedSamples, loggedTimes);
            }
        } // End if ev.type == EV_KEY. All other events are ignored

        fflush(stdout);
    } // End of while loop

    close(kbdFileHandle);
} // End of keylogSession() function

int main() {
    // Registring shutdown hook for C^C shutdown command-line.
    signal(SIGINT, intHandler);

    printf("Keylogger started\n");
    keylogSession();

    return 0;
}