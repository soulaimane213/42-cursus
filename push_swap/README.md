*This project has been created as part of the 42 curriculum by sofadl.*

# Push_Swap Project

## Description
The Push_Swap project is a programming challenge aimed at sorting data on a stack using a limited set of operations. The goal is to sort a list of integers with the minimum number of operations possible, while complying with constraints on time and memory efficiency. This project helps develop algorithmic thinking, understanding of data structures (stacks), and low-level programming skills in C.

## Instructions
1. Clone the repository:
```bash
git clone <repository_url>
Compile the project:

gcc *.c -o push_swap
Run the program:

./push_swap <list_of_numbers>
Optional: Use checker_linux to verify the correctness of your operations:

./push_swap <list_of_numbers> | ./checker_linux <list_of_numbers>

Example:
./push_swap 3 2 1

Resources

C Standard Library Documentation

Valgrind Memory Checker

Tutorials and articles on stack-based sorting algorithms and radix sort.

AI Usage: AI was used to assist in code formatting, generating test cases, and optimizing error handling for memory leaks and edge cases in user input parsing.

Additional Information
Ensure input integers are within the 32-bit signed integer range.

Duplicate numbers or invalid input will trigger an error.

The project follows the 42 Norm coding standard, including line length and indentation rules.
