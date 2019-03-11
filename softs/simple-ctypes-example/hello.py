#!/usr/bin/python3

import ctypes

'''
ctypes helps in binding a C library into a Python object with cdll.

Note on arrays : if you want to get an array from a C function, it is better
to create and pass the list from Python, along with the expected size of the
list. This way, memory allocation/deallocation is managed by Python.
'''

if __name__ == "__main__":
    # Load the library. This library must be generated with :
    # gcc -shared -Wl,-soname,helloworld -o helloworld.so -fPIC hello.c
    helloworld = ctypes.cdll.LoadLibrary("./helloworld.so")

    # Set the return types for the functions
    helloworld.helloworld.restype = ctypes.c_char_p             # Pointer on char array
    helloworld.numbers.restype = ctypes.POINTER(ctypes.c_int)   # Pointer on int array
    helloworld.number.restype = ctypes.c_int                    # Just an int

    # Test the helloworld() function
    print(helloworld.helloworld())

    # Test the print() function
    helloworld.print("This is a test".encode('utf-8'))

    # Test the numbers() function
    helloworld.randomSeed()
    numbers = helloworld.numbers()

    # Test the number() function
    print(helloworld.number())