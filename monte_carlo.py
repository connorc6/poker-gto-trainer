import random
from treys import Card, Deck, Evaluator
import itertools

def flatten_cards(cards):
    flat = []
    for c in cards:
        if isinstance(c, list):
            flat.extend(c)
        else:
            flat.append(c)
    return flat

def check_overlap(hands):
    """
    Ensure no cards overlap across multiple hands.
    """
    seen = set()
    for hand in hands:
        for card in hand:
            if card in seen:
                return True
            seen.add(card)
    return False

def monte_carlo_equity(hero_hand, villain_ranges, board=[], iterations=10000):
    """
    hero_hand: List of two cards (ints)
    villain_ranges: List of lists of villain combos, e.g. [[(c1, c2), ...], [(c3, c4), ...]]
    board: List of board cards
    iterations: How many simulations to run
    """
    evaluator = Evaluator()
    board = list(board)
    hero_hand = list(hero_hand)
    n_villains = len(villain_ranges)

    wins = [0] * (n_villains + 1)
    ties = 0

    for _ in range(iterations):
        deck = Deck()
        used = set(hero_hand + board)
        for card in used:
            if card in deck.cards:
                deck.cards.remove(card)

        # Select one valid combo per villain
        villain_hands = []
        for combos in villain_ranges:
            random.shuffle(combos)
            for c1, c2 in combos:
                if c1 in used or c2 in used:
                    continue
                villain_hands.append([c1, c2])
                used.update([c1, c2])
                deck.cards = [c for c in deck.cards if c != c1 and c != c2]
                break
            else:
                break  # Failed to find a valid combo for this villain
        if len(villain_hands) != n_villains:
            continue

        if check_overlap([hero_hand] + villain_hands + [board]):
            continue

        # Complete the board
        missing = 5 - len(board)
        sim_board = board + deck.draw(missing)

        hero_score = evaluator.evaluate(sim_board, hero_hand)
        villain_scores = [evaluator.evaluate(sim_board, v_hand) for v_hand in villain_hands]
        all_scores = [hero_score] + villain_scores

        min_score = min(all_scores)
        winners = [i for i, s in enumerate(all_scores) if s == min_score]

        if len(winners) == 1:
            wins[winners[0]] += 1
        else:
            ties += 1

    total = sum(wins) + ties
    if total == 0:
        return None  # Not enough valid iterations

    result = {'hero': round(100 * wins[0] / total, 2)}
    for i in range(1, len(wins)):
        result[f'villain_{i-1}'] = round(100 * wins[i] / total, 2)
    result['tie'] = round(100 * ties / total, 2)
    return result
