# Insights and Observations

For these insights, the restrictions do not apply to the end lines because oscillations cannot happen between an intermediate line and an end line. See [What are Oscillations?](./README.md/#what-are-oscillations) for the formal definition of an oscillation. 

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

Over infinite passes, the drill will never have a player oscillate if and only if the number of players in the starting line must be odd and the number of players in each intermediate line must are even. Conversely, the drill will have a player oscillate if and only if any of the intermediate lines have an odd number of players or the starting line has an even number of players.

<details>
<summary>Proof</summary>

### Parity of the Starting Line

The starting line must have an odd number of players. Assume that the starting line has an even number of players. On the first pass, the starting line will lose a player and become odd. When the ball returns to this line, the player that passed the ball will be entering a line with an odd number of players. By insight 1, this player will not return to the line they were originally from. Therefore, we can say that for the drill to never have a player oscillate, the starting line must have an odd number of players through proof by contradiction.

### Parity of the Intermediate Lines

This follows from [Lemma 1](#lemma-1). 

</details>