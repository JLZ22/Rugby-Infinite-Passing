# Rugby Infinite Passing

This is a personal interest project that aims to gain a better understanding of how and when [oscillations](#what-are-oscillations) occur in a common Rugby warmup drill called [infinite passing](#what-is-infinite-passing). The key features here are a Pygame demonstration of the drill and a brute force script which runs different combinations of lines and players for a number of iterations each and records the results. 

## Table of Contents

- [What is infinite passing?](#what-is-infinite-passing)
- [What are oscillations?](#what-are-oscillations)
- [Usage](#usage)
  * [Dependencies](#dependencies)
  * [Running the Code](#running-the-code)
    + [Pygame Demonstration](#pygame-demonstration)
    + [Brute Force Approach](#brute-force-approach)
- [Insights](./Insights.md)

## What is infinite passing?

Players will line up in lines (typically no more than 5 or 6) and pass the ball according to the following steps. 

The ball can start in any line. 

1. the player with the ball passes to the adjacent line in the current direction (typically starts with right)
2. the player who just passed the ball goes to the end of the line they just passed to
3. repeat steps 1 and 2 until the ball reaches the last line in that direction
4. switch directions
6. repeat steps 1-4

This goes on indefinitely until the coach stops the drill (or you get bored of watching the demo). To see the demo, see the [Usage](#usage) section.

## What are oscillations?

### Context

When I was first introduced to this drill, I noticed that some players would be stuck passing between two lines while others would visit multiple lines. This project is interested in understanding the conditions that lead to a player oscillating between two lines. While oscillation is not necessarily a bad thing (since you end up getting to pass in both directions anyways), it is interesting to see how the number of players and lines affect whether a player oscillates.

### Definition

Formally, a player $p$ oscillates between lines $l_1$ and $l_2$ if $p$ enters $l_2$ from $l_1$ and then returns to $l_1$ from $l_2$ on the next pass without having reached one of the end lines. Note that this means if $l_2$ is one of the end lines, no oscillations occur. 

### Demonstration

A demonstration of an oscillating player and a non-oscillating player can be seen in the [Usage](#usage) section.

## Usage

Notes:
1. the indices of lines goes from 0 to $n-1$ from left to right where $n$ is the number of lines.
2. the indices of the players goes from left to right and then top to bottom.

```
line 1   line 2   line 3   line 4
0        1        2        3
4        5        6        7
8        9        10       11
```

## Dependencies 

Install the required packages with 

```bash
pip install -r requirements.txt
```

## Running the Code

These scripts both have command line arguments that can be used to modify the parameters of the drill. Use the `-h` flag to see the available options.

### Pygame Demonstration

Note: The different colors just help to differentiate the players. They have no other significance. 

```bash
python3 simulation.py
```

For full documentation on command line arguments, use the `-h` flag.

<details>
<summary>Example of a player oscillating (follow the player in red)</summary>

```bash
python3 simulation.py --example1
```

The player in red goes from the second line to the third line and back to the second line without having reached the rightmost line. This is an example of a player oscillating between two lines.
</details>
<details>
<summary>Example of a player not oscillating (follow the player in green)</summary>

```bash
python3 simulation.py --example2
```

The player in green goes from the second line to the third line. This is an example of a player not oscillating between two lines.
</details>

### Determining if a Player Oscillates 

Given a valid drill run for $n$ passes, we can determine if, when, and between which two lines any player $p$ will oscillate. To test this, we verify the projection by running the drill in hidden mode and comparing the results. 

To run the projection, use the following command:

```bash
python3 will_oscillate.py
```

For full documentation on command line arguments, use the `-h` flag.

### Brute Force Approach

```bash
python3 brute_force_drills.py
```

## Notable Constraints

1. The starting line must have at least two players. Since the starting line is the only line that loses a player without gaining one, it must have at least two players to ensure that it is not empty when the ball returns to it. this will never happen to any other line since they will always gain a player before losing one.

## Insights

My observations and insights can be found in [Insights.md](./Insights.md).