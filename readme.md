# Block Game

My partner and I like to play phone games and you could say we get a little competitive. Our current obsession is with a game on the android store called Block Puzzle. It's a tetris like casual game where you place tetrominos on a 10x10 grid attempting to clear rows/columns. 

As it stands, my high score is 176,450. My partner is sitting at 421,200. It's become quite clear to both of us that I will never reach those heights... through conventional means. But, what I do have is a very particular set of skills. Skills I have honed over a long university career. Skills that make me a nightmare for casual phone gaming before bed time. 

The plan is to create a machine playable version of the game and train an AI to play for me. Some people will call this cheating, and it is. But my partner doesn't have github.

## The Game 

Making our own version of our Block Puzzle game is quite straightforward. The game is played on a 10x10 grid, which we can represent as a 2D array. This game has 28 different pieces, each composed of smaller blocks that occupy individual squares on the grid. These pieces include a few basic shapes and their rotated versions. The smallest piece consists of a single block, the largest is a 3x3 block, and the longest stretches 5 blocks in length.

To represent these pieces, we use a 5x5 array. In this array, a block is denoted by an integer value, while a zero represents an empty square. For example, our 3x3 square piece is represented as follows:

```
    0 0 0 0 0
    0 1 1 1 0
    0 1 1 1 0
    0 1 1 1 0
    0 0 0 0 0
```

Positioning the pieces around the central point of the 5x5 grid simplifies the process of placing them on the 10x10 board. We use x, y coordinates to align the center of our 5x5 piece grid over the corresponding area on the 10x10 board grid. A piece cannot be placed if any of its set blocks fall outside the playable area or overlap with already placed blocks. If all subblocks of a piece fit validly, they are 'stamped' onto the board.

In the original phone game, some pieces are different colours, which, this doesn't affect gameplay but to make it look more interesting, I've also assigned different colours to some pieces, represented by varying integer values for the subblocks.

Players have a choice of three pieces to place at any given time. The phone game seems to employ a non-random sequence for piece availability, with certain pieces appearing only after reaching specific scores, and larger pieces offered as the available space decreases. Without insight into the game's exact algorithm, I've opted for a completely random selection: players start with three randomly chosen pieces, and as they place one, it's replaced with another random piece.

Scoring in the game is straightforward. Each subblock placed on the grid is worth 10 points. However, the significant scores come from clearing rows and columns. Clearing any single row or column earns 100 points. Clearing multiple rows or columns simultaneously yields higher scores, as observed:

```
1 row/column = 100 points
2 rows/columns = 300 points
3 rows/columns = 600 points
4 rows/columns = 1000 points
5 rows/columns = 1500 points
6 rows/columns = 2100 points
```

It's worth noting that players can't clear more than 6 lines at once. This scoring system is based on the sum of the first 'n' natural numbers, multiplied by 100.

Putting all of that together we end up with a playable version of the game:

![random_agent3](https://github.com/matthew-tyler/block_game/assets/101033922/e44910e4-9879-4816-ab43-7de22d773faf)

But as you can see from the GIF, just making random moves is not a good stratergy. For that we'll need some machine learning. 

## The AI
