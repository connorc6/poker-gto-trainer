# equity_calculator.py

from treys import Card, Evaluator, Deck
from itertools import combinations
import itertools
import random, pdb

def flatten_cards(cards):
        if not isinstance(cards, list):
            raise TypeError(f"Expected a list of cards, got {type(cards)}: {cards}")

        result = []
        for c in cards:
            if isinstance(c, list):
                result.extend(c)
            elif isinstance(c, int):
                result.append(c)
            else:
                raise TypeError(f"Expected card or list of cards, got {type(c)}: {c}")
        return result

def calculate_equity(hero_hand, villain_range, board, iterations=10000, force_exact=False):
    evaluator = Evaluator()
    hero = list(hero_hand)
    board = list(board)

    if isinstance(villain_range[0], tuple):
        villain_combos = villain_range
    else:
        villain_combos = [tuple(villain_range)]

    board_complete = len(board) >= 3
    use_exact = force_exact or (len(villain_combos) <= 20 and board_complete)

    hero_wins = 0
    villain_wins = 0
    ties = 0

    # If the board is complete, just evaluate directly — no need to simulate
    if len(board) == 5:
        hero_score = evaluator.evaluate(board, hero)
        best_equity = 0
        tie_equity = 0
        for v1, v2 in villain_combos:
            if v1 in hero or v2 in hero or v1 in board or v2 in board:
                continue
            v_score = evaluator.evaluate(board, [v1, v2])
            if hero_score < v_score:
                best_equity += 1
            elif hero_score == v_score:
                tie_equity += 1

        total = len(villain_combos)
        if total == 0:
            return {'hero': 0.0, 'villain': 0.0, 'tie': 0.0}

        hero_equity = best_equity / total + 0.5 * tie_equity / total
        return {
            'hero': round(100 * hero_equity, 2),
            'villain': round(100 * (1 - hero_equity), 2),
            'tie': round(100 * tie_equity / total, 2)
        }

    if use_exact:
        for v1, v2 in villain_combos:
            if v1 in hero or v2 in hero or v1 in board or v2 in board:
                continue

            # Complete the board if needed
            missing = 5 - len(board)
            deck = Deck()
            used = set(hero + [v1, v2] + board)
            deck.cards = [c for c in deck.cards if c not in used]

            # Enumerate all board completions
            if missing == 0:
                sim_boards = [board]
            else:
                sim_boards = list(itertools.combinations(deck.cards, missing))

            for additional in sim_boards:
                full_board = board + list(additional)

                # Ensure exactly 5 unique board cards
                if len(full_board) != 5:
                    continue
                if len(set(full_board)) != 5:
                    continue

                # Avoid duplicated cards in hand + board
                all_cards = full_board + hero + [v1, v2]
                if len(set(all_cards)) != 9:
                    continue

                try:
                    h_score = evaluator.evaluate(full_board, hero)
                    v_score = evaluator.evaluate(full_board, [v1, v2])
                except Exception as e:
                    print(f"[WARN] Evaluator failed: {e}")
                    continue

                if h_score < v_score:
                    hero_wins += 1
                elif h_score > v_score:
                    villain_wins += 1
                else:
                    ties += 1
    else:
        for _ in range(iterations):
            v1, v2 = random.choice(villain_combos)

            # Check for overlap
            if v1 in hero or v2 in hero or v1 in board or v2 in board:
                continue

            used = set(hero + [v1, v2] + board)
            deck = Deck()
            deck.cards = [c for c in deck.cards if c not in used]

            missing = 5 - len(board)
            sim_board = board + deck.draw(missing)

            if len(sim_board) != 5:
                print("[ERROR] Board does not have 5 cards:", sim_board)
                continue

            if len(set(sim_board + hero)) != len(sim_board + hero):
                print("[ERROR] Duplicate card in board + hero:", sim_board, hero)
                continue

            h_score = evaluator.evaluate(sim_board, hero)
            v_score = evaluator.evaluate(sim_board, [v1, v2])

            if h_score < v_score:
                hero_wins += 1
            elif h_score > v_score:
                villain_wins += 1
            else:
                ties += 1

    total = hero_wins + villain_wins + ties
    if total == 0:
        return {'hero': 0.0, 'villain': 0.0, 'tie': 0.0}
    return {
        'hero': round(100 * hero_wins / total, 2),
        'villain': round(100 * villain_wins / total, 2),
        'tie': round(100 * ties / total, 2)
    }

def complete_boards(hero, villain, board):
    """
    Generate all possible board completions given a partial board.
    """
    known_cards = set(hero + villain + board)
    deck = [c for c in Deck().cards if c not in known_cards]
    missing = 5 - len(board)

    if missing == 0:
        sim_boards = [board]
    else:
        sim_boards = itertools.combinations(deck.cards, missing)

    for additional in sim_boards:
        full_board = board + list(additional)
        if len(full_board) != 5:
            continue  # Skip invalid boards
        if len(set(full_board + hero + villain)) != 9:
            continue  # Skip overlaps