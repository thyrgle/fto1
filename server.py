import hug
import json
from hug.middleware import CORSMiddleware

# Probably should never do this but lol.
api = hug.API(__name__)
api.http.add_middleware(CORSMiddleware(api))

def do_move(pos, mov):
    """
    Given a particular position perform a move in four to one.
    Note: Assumes validity of move.
    """
    return pos - mov


def gen_moves(pos):
    """
    Generate every possible move given a position in the game four to one.
    """
    if pos == 1:
        return [1]
    elif pos == 0:
        return []
    else:
        return [1, 2]

# -------------------------------------------------------------------
# Collection of functions to update state of the best position found.
# old is the previous best state data, new is the challenger.
# -------------------------------------------------------------------

def loss_loss(old, new):
    return new

def loss_win(old, new):
    return old[0], max(old[1], new[1])

def win_loss(old, new):
    return old[0], min(old[1], new[1])

def no_op(old, new):
    return old

#--------------------------------------------------------------------
#--------------------------------------------------------------------
#--------------------------------------------------------------------

STATES = {
    "LOSS" : { "LOSS" : loss_loss, "WIN" : loss_win },
    "WIN"  : { "LOSS" : win_loss,  "WIN" : no_op },
}

@hug.get('/')
def next_best_move(pos: hug.types.number):
    """
    Given a position, returns the next best move that someone should play
    Arguments:
    pos -- The current position of the board.
    """
    moves = gen_moves(pos)
    with open('fto1.json') as raw_data:
        data = json.loads(raw_data.read())
        best = moves[0]
        best_stats = [data[str(do_move(pos, moves[0]))]['value'],
                      data[str(do_move(pos, moves[0]))]['remoteness']]
        for move in moves:
            move_stats = (data[str(do_move(pos, move))]['value'],
                          data[str(do_move(pos, move))]['remoteness'])
            old_best_stats = best_stats
            best_stats = STATES[best_stats[0]][move_stats[0]](best_stats, move_stats)
            if best_stats != old_best_stats:
                best = move
        return best
