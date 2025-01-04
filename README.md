# Rugby Infinite Passing

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



### Proof that Even Implies No Oscillation

Let $P(n)$ be the proposition that a player will not oscillate if they enter a line with $n$ players where $n$ is even (and conversely will oscillate if $n$ is odd). The example above is our base case.

Assume $P(n)$ is true for some $n \in \mathbb{N}^+$. 

1. if $n$ is even, then $n+1$ is odd which means that the player will oscillate by our inductive hypothesis.
2. if $n$ is odd, then $n+1$ is even which means that our player will not oscillate by our inductive hypothesis.

Since $n$ is either even or odd, we have shown that $P(n) \implies P(n+1)$ for all $n \in \mathbb{N}^+$.

## Usage

Run a single instance of a drill where every iteration is printed:
```bash
python3 Drill.py
```

To run a brute force over range of player and line counts for a number of iterations:

```bash
python3 brute_force_drills.py
```

Further details on modifying the parameters for both scripts can be found in the respective files.

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

2. 

$$\lim_{i \rightarrow \infty} |X_2| = 18$$ 

$$\lim_{i \rightarrow \infty} |X_j| = 14, \ \ \forall j > 2$$


#### Going beyond constraints:

3. $\forall j > 1 \ \ \forall p \in [j+1, \infty)$, it seems that

$$\lim_{i \rightarrow \infty} |X_j| \rightarrow \infty.$$ 

This makes sense because we know that if every line contains an even number of players, then no player will oscillate. With infinite players or lines, there are an infinite number of ways to achieve an even number of players in each line.

4. If $p$ is restricted to $p \le c \cdot j$ for some constant $c \mod 10 = 0$, then

$$\lim_{i \rightarrow \infty} |X_2| = 2c - 2$$

$$\lim_{i \rightarrow \infty} |X_j| = \frac{3c}{2} - 1, \ \ \forall j \in [3, 20]$$

. This was observed for $c \in [10, 20, 30, 40, 50]$. However, this trend breaks down if either $c$ or $j$ are not constrained.

### Next Steps

1. Propose an algorithm that will yield all possible values of $p$ that result in a 0 oscillation drill for a given number of lines $j$ and a given maximum number of players $p_{\text{max}}$. 
    - One version should be able to handle $i \rightarrow \infty$
    - The second version should be able to handle any positive value of $i$.

Learn Coq: https://cel.hal.science/inria-00001173v6/document
