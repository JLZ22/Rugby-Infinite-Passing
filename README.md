# Rugby Simulation

This is a personal interest project that aims to gain a better understanding of a common Rugby warmup drill called "infinite passing". 

## What is "Infinite Passing"?

Players will line up in lines (typically no more than 5 or 6) and pass the ball according to the following steps. 

The ball starts on the leftmost line. 

1. the player with the ball passes to the adjacent right line
2. the player who just passed the ball goes to the end of the adjacent right line
3. repeat steps 1 and 2 until the ball reaches the rightmost line
4. the player with the ball passes to the adjacent left line 
5. the player who just passed the ball goes to the end of the adjacent left line
6. repeat steps 1-6

Below is a diagram of the drill running where the ball is passed 4 times. Each column is a line of players where each number is a unique player. A number with `b` immediately after it represents the player with the ball. For example, `1b` means player 1 has the ball.

The example below was generated by the code in main.
```
Initial State:
Line 1:    Line 2:    Line 3:    
1b         2          3          
4          5          6          
7          8          9          

Iteration 1:
Line 1:    Line 2:    Line 3:    
4          2b         3          
7          5          6          
           8          9          
           1                     

Iteration 2:
Line 1:    Line 2:    Line 3:    
4          5          3b         
7          8          6          
           1          9          
                      2          

Iteration 3:
Line 1:    Line 2:    Line 3:    
4          5b         6          
7          8          9          
           1          2          
           3                     

Iteration 4:
Line 1:    Line 2:    Line 3:    
4b         8          6          
7          1          9          
5          3          2          
```

## Player Oscillations

A common occurence in this drill is that one or more players will oscillate between two lines. This is happens when a player goes to the line they were just in without going all the way down to the last line. For example, if a player, Jeff, is in a drill with 3 lines and is the first person in line 1, Jeff would have oscillated one time if he were to pass to (and subsequently join) line 2 and then pass back to (and join) line 1 again without having visited line 3. 

A key characteristic that determines whether a player will oscillate or not is whether the line they are entering has an odd or even number of players excluding the one entering. If Jeff passes the ball and goes to the end of a line with an even number of players (excluding himself), his next turn would not result in an oscillation. Conversly, if Jeff were to enter a line with an odd number of players (excluding himself), his next turn would not result in an oscillation. The only exception is if the ball reaches the end and switches direction. Since that is a necessary part of the drill, we will not be counting changes in direction on the ends of the drill as an oscillation. Below is a brief example where Jeff is player 1. 

**Jeff enters an odd line** (example generated by the code in main)

```
Initial State:
Line 1:    Line 2:    Line 3:    
1b         2          3          
4                                

Iteration 1:
Line 1:    Line 2:    Line 3:    
4          2b         3          
           1                     

Iteration 2:
Line 1:    Line 2:    Line 3:    
4          1          3b         
                      2          

Iteration 3:
Line 1:    Line 2:    Line 3:    
4          1b         2          
           3                     

Iteration 4:
Line 1:    Line 2:    Line 3:    
4b         3          2          
1                                

Player 1 oscillated 1 times.
Player 2 did not oscillate.
Player 3 did not oscillate.
Player 4 did not oscillate.
```

**Jeff enters an even line** (example generated by the code in main)

```
Initial State:
Line 1:    Line 2:    Line 3:    
1b         2          3          
4          5                     

Iteration 1:
Line 1:    Line 2:    Line 3:    
4          2b         3          
           5                     
           1                     

Iteration 2:
Line 1:    Line 2:    Line 3:    
4          5          3b         
           1          2          

Iteration 3:
Line 1:    Line 2:    Line 3:    
4          5b         2          
           1                     
           3                     

Iteration 4:
Line 1:    Line 2:    Line 3:    
4b         1          2          
5          3                     

Iteration 5:
Line 1:    Line 2:    Line 3:    
5          1b         2          
           3                     
           4                     

Iteration 6:
Line 1:    Line 2:    Line 3:    
5          3          2b         
           4          1          

Player 1 did not oscillate.
Player 2 did not oscillate.
Player 3 did not oscillate.
Player 4 did not oscillate.
Player 5 did not oscillate.
```

As you can see from the visualization above, Jeff (player 1) passes the ball a total of two times in each instance. When there was an even number of players in line 2, he did not oscillate. However, when there was an odd number of players in line 2, he did oscillate. 

## Brute Force Approach

To gain intuition on the problem and potentially observe patterns, I am starting with a brute force approach where I am keeping track of what combination of lines and players result in no oscillations for a given number of run iterations to look for any patterns that may exist.

### Symbols:

$j$ is the number of lines for any given drill.

$p$ is the number of players for any given drill.

$i$ is the number of times the ball is passed in a single run of the drill. This is also known as the number of iterations.

$X_{j}$ the set of values of $p$ that result in a 0 oscillation drill for a given number of lines $j$.

### Constraints 

$$j,p,i \in \mathbb{N}$$
$$2 \le  j \le 100$$
$$j + 1 \le p \le 10j$$
$$i \ge 1000$$

Note: Given the above constriants on $j$ and $p$, running the drill for $i = 1000$ is sufficient to determine whether a certain player count causes a 0 oscillation drill or not because the results are consistent when compared against 10,000 and 100,000 iterations. 

### Algorithm:

For each drill with $j$ lines, run the drill using all possible values of $p$ where $p \in [j + 1, 10j]$ where each run sees the ball passed $i$ times. If the player oscillates 0 times, add $p$ to $X_{j}$.

### Observations

#### Given the above constraints: 

1. Let $m = \min{X_j}$, 

$$m, m + 1, m + 2 \in X_i$$

2. If we allow $i$ to approach infinity while maintaining our other constraints (namely $p \le 10n$), then 
$$\lim_{i \rightarrow \infty} |X_j| = 14$$

. However, $\forall p \in [j+1, \infty)$,

$$\lim_{i \rightarrow \infty} |X_j| \rightarrow \infty$$

### Conjectures 

1. $\forall j \in [2, 100)$ and $i \rightarrow \infty$ the values of $X_j$ are functions of $j$.

    - Reasoning: 
        - Observation 1 suggests that the values of $X_j$ are not random (or at least not entirely).
        - Observation 2 suggests that $|X_j|$ is a function of $j$ and $i$, but for a large enough $i$, it is constant. 

2. Expanding the constraints of conjecture 1 to include $\forall j \in [2, \infty)$.
    - TODO
3. Expanding the constraints of conjecture 2 to $\forall p \in [j+1, \infty)$.
    - TODO