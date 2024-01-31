
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 50
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
        action = choice(board.legal_actions(state))
        state = board.next_state(state, action)
    return state



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

