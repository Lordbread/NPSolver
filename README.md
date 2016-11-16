# NPSolver
## Introduction
This program is used to solve some NP-hard problem that comes with a map.  
For example, finding an optimal point on the map that is far away from all the hostipal on the map  
User should provide a map definition file ( .map) that contains all symbols in this map with each symbol in a line. And then implements `SoftConstrain` and `HardConstrain` class provided by NPSolve engine.

## Procedure
* The system read all map symboles into a map object with coordinates:x,y
* Divides the map into a tile system and place symbol into grid
* Then the system will find the solution space (All possible soltion) that satistify the `HardConstrain`
* After we find the solution space, we use some NP algorithm to find the optimal solution with `SoftConstrain`

## Better Procedure (Not Implemented yet)
* Divides the map into a large grid (4*4 or 3*3)
* Find solution using `HardConstrain` and `SoftConstrain`
* Find the optimal gird
* divides this grid into sub tiles (4*4 or 3*3) and back to step 2
* Loop untail we meet our accuracy requirement 

