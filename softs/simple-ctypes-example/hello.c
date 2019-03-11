#include <stdio.h>
#include <stdlib.h>
#include <time.h>

char * helloworld() {
    char * hello = (char *)malloc(100 * sizeof(char));
    hello = "Hello world !";
    return hello;
}

void print(char * model) {
    printf("%s", model);
}

void randomSeed() {
    srand(time(NULL));
}

int * numbers() {
    int * numbers = (int *)malloc(100 * sizeof(int));
    for (int index = 0; index < 100; index++) {
        *(numbers + index) = rand();
    }
    return numbers;
}

int number() {
    int number = rand();
    printf("\nRandom number: %d\n", number);
    return number;
}