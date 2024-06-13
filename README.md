# Rugby Simulation

## Packages

```

```

## Context

In rugby, a common drill to warm up is "infinite passing". This is a drill where players will line up in `n` lines (typically no more than 5 or 6) and pass the ball according to the following algoirthm. 

The ball starts on the leftmost line. 

1. the player with the ball passes to the adjacent right line
2. the player who just passed the ball goes to the end of the adjacent right line
3. repeat steps 1 and 2 until the ball reaches the rightmost line
4. the player with the ball passes to the adjacent left line 
5. the player who just passed the ball goes to the end of the adjacent left line
6. repeat steps 1-6

Below is a diagram of the drill running where the ball is passed 4 times (`-n->` indicates the n-th iteration). Each column is a line of players where each number is a unique player. A number with `b` immediately after it represents the player with the ball. For example, `1b` means player 1 has the ball. In the example below, the ball starts with player one who is the first player in the leftmost column. Player 4 is the second player in the leftmost column. Player 2 is the first player in the middle column.  
```
1b 2 3        4 2b 3        4 5 3b       4 5b 6        4b 8 6
4  5 6  -1->  7 5  6  -2->  7 8 6  -3->  7 8  9  -4->  7  1 9
7  8 9          8  9          1 9          1  2        5  3 2
                1               2          3
```

## Problem

A common occurence in this drill is that one or more players will be stuck oscillating between two lines. This happens to a player (let's name him Jeff) if he passes the ball and goes to the end of a line with an odd number of players. If we were to have 5 lines of 3 where Jeff is the first player in the first line, he would not travel all the way down the 5 lines before revisiting the first line because the line he is entering (line 2) has 3 people. As such, he would return to line 1 on his next turn. 


## Approach

1. gaTo gain intuition on the problem and potentially observe patterns, I am starting with a brute force approach where I am keeping track of which players oscillate. 
