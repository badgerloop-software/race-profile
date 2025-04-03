#!/usr/bin/env python
"""
Sample script that uses the add module created using
MATLAB Compiler SDK.

Refer to the MATLAB Compiler SDK documentation for more information.
"""

import add
import time
# Import the matlab module only after you have imported
# MATLAB Compiler SDK generated Python modules.
import matlab

start_time = time.perf_counter()

my_add = add.initialize()

num1In = matlab.double([25.0], size=(1, 1))
num2In = matlab.double([45.0], size=(1, 1))
resultOut = my_add.add(num1In, num2In)
print(resultOut, sep='\n')

my_add.terminate()

elapsed_time = time.perf_counter() - start_time
print(f"Function execution time: {elapsed_time:.6f} seconds")
