2856. Count Uppercase and Lowercase Letters in Word
Easy
Category
Functions
Points
125
Description
You are given a prefilled function that accepts a string as input. Complete the function so that it counts the number of uppercase and lowercase letters separately and prints both counts on separate lines.

Function Details:

Function Name: count_of_lowercase_and_uppercase_letters
Parameter: arg_1 (string to analyze)
Input Format
A single line containing a string
Output Format
First line: count of uppercase letters
Second line: count of lowercase letters
Constraints
Count both uppercase and lowercase separately
Ignore non-alphabetic characters
Print both counts inside function
First uppercase, then lowercase
Sample Input / Output
Input
MasTer
Output
2
4
Explanation
Input string arg_1 is MasTer.
Initialize uppercase_count to 0 and lowercase_count to 0.
Iterate through arg_1: 'M' increments uppercase_count to 1, 'a' increments lowercase_count to 1, 's' increments lowercase_count to 2, 'T' increments uppercase_count to 2, 'e' increments lowercase_count to 3, and 'r' increments lowercase_count to 4.
Print uppercase_count which is 2.
Print lowercase_count which is 4.
Complexity
Time:
O(n)
Space:
O(1)
