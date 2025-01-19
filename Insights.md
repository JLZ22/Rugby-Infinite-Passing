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
</details>

---

## Lemma 2

The parity of the starting line will change on the first pass of the drill. It will remain constant for all subsequent passes. 

<details>
<summary>Proof</summary><br/>

On the first pass, the starting line will lose a player. This changes the parity of the starting line because the next time a player enters this line, the number of players in the line excluding the entering player will be of a different parity than the number of players in the line before the first pass. For all following passes, the starting line will receive a player before losing one, so the parity will remain constant.

</details>

---

## Lemma 3

The parity of all intermediate lines excluding the starting line will remain the same over the course of the drill. 

<details>
<summary>Proof</summary><br/>

The parity of non-starting intermediate lines will never change because every time one of these lines passes and loses a player, they would have gained a player in the previous pass. Let's say we have lines $a$, $b$, and $c$ from left to right where they all have 2 players to start. Line $a$ is the starting line, so it passes to line $b$, leaving $a$ with 1 player and $b$ with 3. Since lines can't pass to themselves, we can still say that the parity of line $b$ is the same as before the pass. When line $b$ passes to line $c$, line $b$ will have 2 players. Now, if line $b$ receives the ball, it will have the same parity as before the start of the drill. This can be generalized to any number of lines.
</details>

---

## Lemma 4

Over infinite passes, the drill will never have a player oscillate if and only if the number of players in the starting line are odd (assuming the starting line is not one of the end lines) and the number of players in each intermediate line are even. This will subsequently be referred to as a perfect drill. Conversely, the drill will have a player oscillate if and only if any of the intermediate lines have an odd number of players or the starting line has an even number of players (imperfect drill).

<details>
<summary>Proof</summary>

### Parity of the Starting Line

Because the starting line's parity changes on the first pass ([Lemma 2](#lemma-2)), the starting line must start with an odd number of players since we need an even number of players in the line to guarantee 0 oscillations ([Lemma-1](#lemma-1)). 

### Parity of the Intermediate Lines

Because non-starting intermediate lines will not change parity ([Lemma 3](#lemma-3)), they must start with an even number of players to guarantee 0 oscillations ([Lemma-1](#lemma-1)).

</details>

---

## Finding a Player's First Oscillation

Given any valid drill run for $n$ passes, we can determine if, when, and between which two lines any player $p$ will oscillate. 

### Perfect Drill

First, we must check the parity of the drill's lines against the conditions set in [Lemma 4](#lemma-4). If all of the conditions are met, we know that the player will never oscillate. 

### Imperfect Drill

Once we rule out the possibility of a perfect drill, we must figure out if the player's first oscillation is within $n$ passes. To do this, we will find the number of passes it takes for the player to reach the beginning line they will oscillate between and add one to account for the pass where they oscillate.

Let's call the line that $p$ is in $l$.

1. Find number of passes it takes to get from the starting line to the line with the $p$ in it. Add that 
to the total pass count.
2. Find the number of passes it takes to get $p$ to the start of the line they are currently in. Add that to the total pass count.
<details>
<Summary>Finding the value</Summary><br/>
 
Each player ahead of $p$ in $l$ must pass the ball in a direction. For each of those players, we will calculate how many passes it takes for the ball to return to $l$ given their passing direction. Then, sum these values to get the total number of passes it takes for the ball to return to $l$ with $p$ at the beginning of the line and in possession of the ball.

To find the number of passes it takes for the ball to return to $l$ after one pass, we simply count how many lines are in the direction of the pass excluding $l$ and multiply by two. For example, if you have a drill with four lines and $l$ is in the second line, the ball will take four passes to return to $l$ after passing right and two passes to return to $l$ after passing left.
</details>

3. Find the closest intermediate line to $l$ that has an odd number of players in the direction that $p$ will first pass. This will be the line that $p$ oscillates between. In the case that there is no intermediate line with an odd number of players in that direction, it must either be $l$ or somewhere in the other direction. In this case, you must search at the other direction inclusive of the $l$ for the first line with an odd number of players starting with $l$. 

4. Run the following loop:

```
function find_first_oscillation(p):
    l <- the line that p starts in 
    passes <- number of passes total # this includes the calculations from steps 1 and 2
    end_line <- the line found in step 3

    # over the current number of passes, p is now at the beginning of l and has the ball

    # now p will pass the ball in the direction of the pass
    passes += 1 
    l = next line in the direction of the pass

    while l != end_line:
        passes <- add the number of passes for p to get to the beginning of l
        passes += 1 # account for p's pass to the next line 
        l = next line in the direction of the pass
    passes += 1 # account for the pass where p oscillates

    return passes
```

5. Now that we have the number of passes it takes for $p$ to oscillate, we can determine if it is within $n$ passes. If it is, we can determine between which two lines $p$ oscillates by checking end_line and the line before it. 