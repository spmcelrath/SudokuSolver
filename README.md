## Introduction

Sudoku is a popular logic-based puzzle game created in 1979 by Howard Garns, a freelance puzzle constructor. A Sudoku puzzle consists of 81 cells, which are divided into nine columns, rows and regions. Players must place the numbers from 1 to 9 into the empty cells in such a way that in every row, column and 3×3 region each number appears only once.
Takayuki Yato and Takahiro Seta of the University of Tokyo have recently proven that Sudoku puzzles belong to the category of NP-complete problems. Such problems are ones that probably cannot be solved in a realistic time frame. Although any given solution to an NP-complete problem can be verified quickly in polynomial time, there is no known efficient way to locate a solution in the first place.
Here, computational theory is applied to create a program which attempts to solve generalized sudoku puzzles of any size with dimension n2 x m2. This program is then extended to solve Samurai Sudokus, puzzles consisting of five overlapping Sudoku grids.

## Approach

The problem was first simplified by considering each Sudoku puzzle to be a graph. In the Sudoku graph, each cell is considered a vertex and two vertices are connected by an edge if the cells that they correspond to are in the same column, row, or 3 x 3 box. Once represented as graphs, Sudokus
 
can be thought of in the context of the classic graph-coloring problem. This problem involves coloring the vertices of a graph such that no two adjacent vertices share the same color. The simplification of Sudokus as graphs allows the solution to be more easily generalized.

## Algorithm

The solution program employed an optimized depth-first search algorithm. The algorithm starts with the first available unknown vertex and iterates through the set of possible values for that vertex, coming up with a different value for the vertex and generating a new depth-first search at every iteration. When the board contains at least one vertex with no possible values, the search fails and there is no solution. The search is complete when each vertex has exactly one possible value. The solver is made more efficient by restricting the sets of possible values for allvertices to only the values specified by their edges. Another pass through the board vertices is made, recursively removing the values of all known vertices from the possible-value lists of their peer vertices in the same row or column. Finally, the depth-first search is recursively called. A heuristic is also applied that prefers cells with fewer remaining possible values.

## Sample I/O

The solution program takes in a text file as input. See example input for the "World's hardest Sudoku" [here](example_input.txt) The first two lines of the text file represent the dimensions of the sudoku puzzle and the subsequent n rows and n columns represent the puzzle itself. Vertices are separated by commas with known vertices represented by the number that occupies them and unknown vertices represented by question marks.

An example output generated from the above input txt file can be seen [here](example_output.txt)

## Nonomino Extension

The solution program was then extended to support nonomino Sudoku puzzles. Nonomino Sudokuos work exactly the same as the typical Sudoku puzzle, except that subregions of the board can be any shape polygon made up of n^2 equal sized squares. This is accomplished through the nono method.


