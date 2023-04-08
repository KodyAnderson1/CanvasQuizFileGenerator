# Homework 3 Results for Anthony Welter

- Number of questions: 5
- Number of [Multiple Answer Questions](#multiple-answer-questions): 1
- Number of [Multiple Short Answer Questions](#multiple-short-answer-questions): 3 **This section is still being tested. Please report any bugs.**



---


## Multiple Answer Questions
Consider the grid as shown below.
A robot starts in cell S at location (9,5) and needs to go to cell G at location (12,10).
The robot cannot pass through the dark blue cells that represent walls.
The robot uses the A* algorithm and the Manhattan distance between a cell and the cell of the goal.
The cost to move between two neighboring cells is 4 if the direction of the move is horizontal and 3 if the direction of the move is vertical.
Manhattan distance h(cell,goal) = abs(cell.x - goal.x) + abs(cell.y - goal.y).
The priority queue is initially set to [S/f=8].
After the first node is popped from the queue, the priority queue changes to [T/f=10, P/f=11, U/f=12] Which of the following cells labeled A, B, K, L, R, Q does the robot not explore, i.e., not insert in its priority queue/frontier?

1. A
2. B
3. K
4. L
5. R
6. Q
7. none; the robot explores all cells listed above

#### _Answer(s):_
- none; the robot explores all cells listed above

---

## Multiple Short Answer Questions
Apply the Uniform Cost Search algorithm as discussed in class to search for a low-cost path from S to G in the graph depicted below.
How many nodes are in the frontier/priority queue after B is added to the queue?
__________ (enter a number only) What is the cost value g, when node G is popped from the frontier/priority queue?
__________ (enter a number only)


#### _Answer(s):_ 3, 5

---

Apply the Greedy Best First Search (GBFS) algorithm as discussed in class to compute the shortest path from city T to city B.
Use the provided straight-line distance as your heuristic function h.
Note the map is slightly different from the map presented in class.
Node T for Timisoara is the first node the algorithm pops from the priority queue/frontier and explores.
Enter the label (e.g., A, O, R, ...) of the city associated with the node in each of the following questions.
What is the city label of the fourth node that the algorithm pops from the priority queue/frontier to explore?
__________ What is the city label of the fifth node that the algorithm pops from the priority queue/frontier to explore?
__________


#### _Answer(s):_ P, B

---

Apply the A* algorithm as discussed in class to compute the shortest path from city T to city B.
Use the provided straight-line distance as your heuristic function h and the provided cost of the graph for your cost function g.
Note the map is slightly different from the map presented in class.
Node T associated with city Timisoara is the first node the algorithm explores.
What is the city label of the fourth node that the algorithm pops from the priority queue/frontier to explore?
Enter the city label (e.g.
A, O, R, ...) of the city associated with the fourth node.
fourth node city label: __________ What is the value of function f associated with the fourth node?
f = __________ (enter a numeric value only)


#### _Answer(s):_ P, 398

---

