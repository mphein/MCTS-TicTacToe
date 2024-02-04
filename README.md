MCTS 3x3 TicTacToe

Implement a python bot which plays Ultimate Tic-Tac-Toe. 

Ultimate Tic-Tac-Toe is a turn-based two-player game where players have to play a grid of 9 tic-tac-toe games simultaneously in order to complete one giant row, column, or diagonal. The catch is that each on each player’s turn, they can only place a cross or circle in one square of one board; and whichever square they pick, their opponent must play on the corresponding (possibly different) board.

Implemented a game tree constructed of MCTS(Monte Carlo Tree Search) nodes.
-	 traverse_nodes → a.k.a. ‘selection’; navigates the tree node
-	 expand_leaf → adding a new MCTSNode to the tree
-	 rollout → simulating the remainder of the game

Random MCTS bot will run until it reaches X nodes per tree and choose a move based on a random rollout. It will then backpropogate modifying each node's win and visit count.
Heuristic MCTS: takes into account board state, and adds scoring to certain move choices such as: winning a tic tac toe square (+), allowing your opponent's next move to be in a square they will win (-).

game.txt contains the mcts_bot vs a purely random bot -> mcts wins

game2.txt features the output of mcts_bot vs mcts_modified showing that taking into account moves instead of random rollouts might be more costly in terms of runtime, but creates a smarter more informed bot.

Challenges: Coming up with a heuristic for the heuristic MCTS bot to make better than random choices when rolling out from a node.

Learned: The four stages of MCTS. How to implement MCTS for a bot in a turn based game. Also learned about the confusing game of Ultimate Tic-Tac-Toe.
