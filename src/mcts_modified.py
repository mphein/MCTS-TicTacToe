
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1000
explore_faction = 2.

def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 1 or 2.

    Returns:        A node from which the next stage of the search can proceed.
    
    """        
    while not board.is_ended(state):
        if node.untried_actions:
            # If there are untried actions from this node, return a new child node.
            action = choice(node.untried_actions)
            node.untried_actions.remove(action)
            retNode = expand_leaf(node, board, state, action)
            return  retNode , state
        else:
            # Select the child node with the highest UCT value.
            action, node = select_child(node, board, state, explore_faction, identity)
            state = board.next_state(state, action)
    return node, state

def select_child(node, board, state, explore_factor, identity):
    """Selects a child node based on the UCT (Upper Confidence Bound for Trees) value.

    Args:
        node: The parent node.
        board: The game setup.
        state: The state of the game.
        explore_factor: The exploration factor.

    Returns:
        The action and child node with the highest UCT value.
    """
    best_value = float('-inf')
    best_child = None

    for action, child in node.child_nodes.items():
        if (identity == board.current_player(state)):
            child_value = child.wins / child.visits + explore_factor * sqrt(log(node.visits) / child.visits)
        else: 
            child_value = 1 - (child.wins / child.visits) + explore_factor * sqrt(log(node.visits) / child.visits)
        if child_value > best_value:
            best_value = child_value
            best_child = child
    return best_child.parent_action, best_child

def expand_leaf(node, board, state, action):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """
    new_state = board.next_state(state, action)
    new_actions = board.legal_actions(new_state)

    new_node = MCTSNode(parent=node, parent_action=action, action_list=new_actions)
    node.child_nodes[action] = new_node
    return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    while not board.is_ended(state):
        action =  move_picker(board, state)
        state = board.next_state(state, action)
    return state

def rollout2(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    while not board.is_ended(state):
        action = choice(board.legal_actions(state))
        state = board.next_state(state, action)
    return state
# X _ _
# _ _ _
# _ _ _
# OWNED BOX EX: {(0, 0): 0, (0, 1): 0, (0, 2): 0, (1, 0): 0, (1, 1): 0, (1, 2): 0, (2, 0): 0, (2, 1): 0, (2, 2): 0}
# DICTIONARY OF ((BOX IN GRID: OWNER) ((KEY): VALUE) WHERE OWNER = 1/2/0

def move_picker(board, state):
    #print(board.owned_boxes(state))
    # currPlayer = board.current_player(state)
    # valid_moves = board.legal_actions(state)
    # for move in valid_moves:
    #     copyState = state
    #     copyState = board.next_state(copyState, move)
    #     if (board.owned_boxes(copyState)[(move[0], move[1])] == currPlayer):
    #         print(board.owned_boxes(copyState))
    #         print((move[0], move[1]))
    #         print(board.owned_boxes(copyState)[(move[0], move[1])])
    #         print()
    #         return move
    # return choice(board.legal_actions(state))
    # MOVES IN FORM (R, C, r, c)
    # for each of the valid moves
    # make opponent pick a square where they have least valid moves?
    # pick move with smallest ratio
    # if move results in you get square = 5
    # if move results in you get win = 10
    # if move results in opponent get square = -5
    # if move results in opponent win = -100
    # else move = 1
    currPlayer = board.current_player(state)
    valid_moves = board.legal_actions(state)
    best_move = {}
    for move in valid_moves:
        copyState = state
        copyState = board.next_state(copyState, move)
        oppMoves = board.legal_actions(copyState)
        oppPlayer = board.current_player(copyState)
        for oppMove in oppMoves:
            oppState = board.next_state(copyState, oppMove)
            if (board.owned_boxes(oppState)[(move[0], move[1])] == oppPlayer):
                best_move[move] = -5
            if (board.is_ended(oppState)):
                if board.points_values(oppState)[currPlayer] == 1:
                    best_move[move] = -10   
        if (board.owned_boxes(copyState)[(move[0], move[1])] == currPlayer):
            return move
        if (board.is_ended(copyState)):
                if board.points_values(copyState)[currPlayer] == 1:
                    return move
        if move not in best_move:
            best_move[move] = 1
    #print(best_move)
    return max(best_move, key = lambda move: best_move[move])

def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    while node:
        node.visits += 1
        node.wins += won
        node = node.parent


def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node
        
        node, sampled_game = traverse_nodes(node, board, sampled_game, identity_of_bot)
        
        sampled_game = rollout(board, sampled_game)
        points = board.points_values(sampled_game)
        won = points[identity_of_bot]

        backpropagate(node, won)

    
    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    best_action = max(root_node.child_nodes, key=lambda action: root_node.child_nodes[action].visits)
    return best_action