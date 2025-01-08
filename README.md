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

When I was first introduced to this drill, I noticed that some players would be stuck passing between two lines while others would visit multiple lines. This project is interested in understanding the conditions that lead to a player oscillating between two lines. While oscillation is not necessarily a bad thing (since you end up getting to pass in both directions anyways), it is interesting to see how the number of players and lines affect whether a player oscillates.

A demonstration of an oscillating player and a non-oscillating player can be seen in the [Usage](#usage) section.

<ins>Note:</ins> If a player enters one of the end lines, they will always return to the line they were originally from. Therefore, we are only interested in the players that enter the lines in between the first and last lines when counting oscillations.


## Usage

### Dependencies 

Install the required packages with 

```bash
pip install -r requirements.txt
```

### Running the Code

These scripts both have command line arguments that can be used to modify the parameters of the drill. Use the `-h` flag to see the available options.

#### Pygame Demonstration

Note: The different colors just help to differentiate the players. They have no other significance. 

```bash
python3 simulation.py
```

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

#### Brute Force Approach

```bash
python3 brute_force_drills.py
```

## Notable Constraints

1. The starting line must have at least two players. Since the starting line is the only line that loses a player without gaining one, it must have at least two players to ensure that it is not empty when the ball returns to it. this will never happen to any other line since they will always gain a player before losing one.

## Insights

My observations and insights can be found in [Insights.md](./Insights.md).