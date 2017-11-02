import hug
import json
from hug.middleware import CORSMiddleware

# Probably should never do this but lol.
api = hug.API(__name__)
api.http.add_middleware(CORSMiddleware(api))

def do_move(pos, mov):
    return pos - mov


def gen_moves(pos):
    if pos == 1:
        return [1]
    elif pos == 0:
        return []
    else:
        return [1, 2]


@hug.get('/')
def next_best_move(pos: hug.types.number):
    moves = gen_moves(pos)
    with open('fto1.json') as raw_data:
        data = json.loads(raw_data.read())
        best = moves[0]
        best_stats = [data[str(do_move(pos, moves[0]))]['value'],
                      data[str(do_move(pos, moves[0]))]['remoteness']]
        for move in moves:
            if best_stats[0] == "LOSS" and data[str(do_move(pos, move))]['value'] == "LOSS":
                best_stats = (data[str(do_move(pos, move))]['value'], data[str(do_move(pos, move))]['remoteness'])
                best = move
            elif best_stats[0] == "LOSS" and data[str(do_move(pos, move))]['value'] == "WIN":
                if best_stats[1] < data[str(do_move(pos, move))]['remoteness']:
                    best_stats[1] = data[str(do_move(pos, move))]['remoteness']
                    best = move
            elif best_stats[0] == "WIN" and data[str(do_move(pos, move))]['value'] == "LOSS":
                if best_stats[1] > data[str(do_move(pos, move))]['remoteness']:
                    best_stats[1] = data[str(do_move(pos, move))]['remoteness']
                    best = move
        return best

