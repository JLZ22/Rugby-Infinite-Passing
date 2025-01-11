# Insights and Observations

For these insights, the restrictions do not apply to the end lines because oscillations cannot happen between an intermediate line and an end line. See [What are Oscillations?](./README.md/#what-are-oscillations) for the formal definition of an oscillation. 

When referring to the parity of a line, we are referring to the parity of the number of players in that line when a player enters it excluding the entering player. 

## Lemma 1

When a player $p$ enters a line with an even number of players excluding $p$, $p$ will not return to the line they entered from on their next pass (i.e. they will not oscillate). The opposite is true if the line has an odd number of players. This only applies to the non-end lines. 
<details>
<summary>Proof</summary><br/>
For this proof, we will use induction. 

### Proposition

Let $P(x)$ be the proposition that if a player enters a line with $n$ players, they will not return to the line they were originally from given that

$$n = 2x \ \ \forall x \in \mathbb{N}^+.$$

### Base Case

Let $x = 1$ (aka $n=2$), and assume that the ball is being passed to the right. We can make this assumption without loss of generality since direction is symmetric. If a player, $p$, passes to and then enters a line with 2 players, $a$ and $b$, $a$ will then pass it in right, $b$ will pass it left, and $p$ will pass right. Since $p$ passes right twice, they will not return to the line they were originally from.

### Inductive Hypothesis

Assume $P(k)$ is true for some $k \in \mathbb{N}^+$. 

### Inductive Step

We must show $P(k) \implies P(k+1)$ for the induction to hold.

Let $n = 2(k+1) = 2k + 2$. If a player, $p$, enters a line with $2k+2$ players, $a_1, b_1, a_2, b_2, \ldots, a_k, b_k, a_{k+1}, b_{k+1}$, player $a_1$ will pass it right, $b_1$ will pass it left, $a_2$ will pass it right, $b_2$ will pass it left, and so on. Since $b_{k+1}$ will pass it left, $p$ will pass it right. Since $p$ passes right twice, they will not return to the line they were originally from.

Therefore, $P(k) \implies P(k+1)$ for all $k \in \mathbb{N}^+$. By induction, we have shown that if a player enters a line with an even number of players, they will not return to the line they were originally from. However, we have not yet shown the converse. By slightly modifying the proof, we can show that if a player enters a line with an odd number of players, they will return to the line they were originally from. 

### Odd Number of Players

Following the same steps in the proof for even number of players, let's say that $n = 2x + 1 \ \ \forall x \in \mathbb{N}^+$. Then, our base case would be a line with one player $a$ who passes right. Then player $p$ would pass left, thereby returning to the line they were originally from. The inductive step would be similar to the one above, but since there is an odd number of players, the sequence of players would end at $a_{k+1}$ passing left. Therefore, $p$ would pass right and return to the line they were originally from.

### Conclusion

We have shown that if a player enters a line with an even number of players, they will not return to the line they were originally from. We have also shown that the opposite is true: if the line has an odd number of players, the player will return to the line they were originally from.

</details><br/>

## Lemma 2

The parity of all intermediate lines excluding the starting line will never change over the course of the drill. The starting line's parity will change on the first pass of the drill and will remain constant for all subsequent passes.

<details>
<summary>Proof</summary>

### Starting Line 

The starting line will change parity on the first pass of the drill. On the first pass, the starting line will lose a player. This changes the parity of the starting line because the next time a player enters this line, the number of players in the line excluding the entering player will be of a different parity than the number of players in the line before the first pass.

### Other Intermediate Lines

The parity of non-starting intermediate lines will never change because every time one of these lines passes and loses a player, they would have gained a player in the previous pass. Let's say we have lines $a$, $b$, and $c$ from left to right where they all have 2 players to start. Line $a$ is the starting line, so it passes to line $b$, leaving $a$ with 1 player and $b$ with 3. Since lines can't pass to themselves, we can still say that the parity of line $b$ is the same as before the pass. When line $b$ passes to line $c$, line $b$ will have 2 players. Now, if line $b$ receives the ball, it will have the same parity as before the start of the drill. This can be generalized to any number of lines.

</details>

## Lemma 3

Over infinite passes, the drill will never have a player oscillate if and only if the number of players in the starting line are odd (assuming the starting line is not one of the end lines) and the number of players in each intermediate line are even. This will subsequently be referred to as a perfect drill. Conversely, the drill will have a player oscillate if and only if any of the intermediate lines have an odd number of players or the starting line has an even number of players (imperfect drill).

<details>
<summary>Proof</summary><br/>

By [Lemma 2](#lemma-2), we know that the starting line will change parity on the first drill while all other intermediate lines will not. By [Lemma 1](#lemma-1), we know that a player will not oscillate if they enter a line with an even number of players. 

### Parity of the Starting Line

Because the starting line's parity changes on the first pass, the starting line must start with an odd number of players. This would make it even for all subsequent passes.

### Parity of the Intermediate Lines

Because non-starting intermediate lines will not change parity, they must start with an even number of players. By [Lemma 2](#lemma-2), they will remain even for all subsequent passes.

</details>

## Finding a Player's First Oscillation

Given any valid drill run for $n$ passes, we can determine if, when, and between which two lines any player will oscillate. 

First, we must check the parity of the drill's lines against the conditions set in [Lemma 3](#lemma-3).

Once we rule out the possibility of a perfect drill, we can perform some computation to find the player's first oscillation. 

TODO  figure out what math is needed here