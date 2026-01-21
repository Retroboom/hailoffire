import random
from dataclasses import dataclass
from typing import Literal, Optional

@dataclass
class SimConfig:
    # BP roll table
    bp_table: Literal["current", "proposed"]  # current: 1-3=1, 4-5=2, 6=3 | proposed: 1-2=1, 3-5=2, 6=3

    # Attacker objective threshold
    attacker_threshold: Literal["all", "any"]  # "all" = bleeds until 3, "any" = bleeds until 1

    # Rolls per unit destroyed
    rolls_per_unit_destroyed: int  # 2 (current) or 1 (proposed)

    # Defender bleeds when enemy on their side (turn they arrive)
    defender_territory_bleed: int = 0  # 0 = off (current), 2 = turn enemy reaches defender side

    # Whether territory bleed is flat 1 BP or rolled (1-3 BP)
    territory_bleed_flat: bool = False  # False = rolled, True = flat 1 BP


def roll_d6():
    return random.randint(1, 6)


def generate_bp(table: str) -> int:
    """Generate break points based on table type"""
    roll = roll_d6()
    if table == "current":
        if roll <= 3:
            return 1
        elif roll <= 5:
            return 2
        else:
            return 3
    else:  # proposed
        if roll <= 2:
            return 1
        elif roll <= 5:
            return 2
        else:
            return 3


def generate_game_params() -> dict:
    """Generate randomized game parameters per the specified distributions"""

    # Unit counts: 5-8 each side (random)
    attacker_units = random.randint(5, 8)
    defender_units = random.randint(5, 8)

    # Break limits: 10 + (2 × units), then adjusted by -4 to +4 for FPP
    attacker_bl = 10 + (2 * attacker_units) + random.randint(-4, 4)
    defender_bl = 10 + (2 * defender_units) + random.randint(-4, 4)

    # Defender reserves: half of units rounded down
    defender_on_table = defender_units // 2
    defender_in_reserve = defender_units - defender_on_table

    # First objective capture: turn 3-8, weighted toward later turns
    # Using weighted random: later turns more likely
    first_obj_weights = [1, 2, 3, 4, 5, 6]  # turns 3-8
    first_obj_turn = random.choices(range(3, 9), weights=first_obj_weights)[0]

    # Second objective: 2-4 turns after first
    second_obj_turn = first_obj_turn + random.randint(2, 4)

    # Attacker casualty schedule: first casualty turn 3-6, then each subsequent
    # within 1-5 turns of previous
    attacker_casualty_turns = []
    first_casualty = random.randint(3, 6)
    attacker_casualty_turns.append(first_casualty)
    next_window_start = first_casualty + 1
    while next_window_start <= 30:  # safety cap
        casualty_turn = random.randint(next_window_start, next_window_start + 4)
        attacker_casualty_turns.append(casualty_turn)
        next_window_start = casualty_turn + 1
        if len(attacker_casualty_turns) >= 10:  # cap at 10 casualties
            break

    # Defender casualty schedule: same formula
    defender_casualty_turns = []
    first_casualty = random.randint(3, 6)
    defender_casualty_turns.append(first_casualty)
    next_window_start = first_casualty + 1
    while next_window_start <= 30:
        casualty_turn = random.randint(next_window_start, next_window_start + 4)
        defender_casualty_turns.append(casualty_turn)
        next_window_start = casualty_turn + 1
        if len(defender_casualty_turns) >= 10:
            break

    # Objective recapture: defender retakes within 10 turns of losing,
    # then attacker retakes within 10 turns of that
    defender_retakes_turn = None
    attacker_retakes_turn = None
    if first_obj_turn:
        defender_retakes_turn = first_obj_turn + random.randint(1, 10)
        attacker_retakes_turn = defender_retakes_turn + random.randint(1, 10)

    return {
        "attacker_bl": attacker_bl,
        "defender_bl": defender_bl,
        "attacker_units": attacker_units,
        "defender_units": defender_units,
        "defender_on_table": defender_on_table,
        "defender_in_reserve": defender_in_reserve,
        "first_obj_turn": first_obj_turn,
        "second_obj_turn": second_obj_turn,
        "attacker_casualty_turns": attacker_casualty_turns,
        "defender_casualty_turns": defender_casualty_turns,
        "defender_retakes_turn": defender_retakes_turn,
        "attacker_retakes_turn": attacker_retakes_turn,
    }


def simulate_game(config: SimConfig, verbose: bool = False) -> dict:
    """Simulate a single game and return results"""

    # Generate randomized game parameters
    params = generate_game_params()

    attacker_bl = params["attacker_bl"]
    defender_bl = params["defender_bl"]
    attacker_units_remaining = params["attacker_units"]
    defender_units_remaining = params["defender_units"]
    defender_on_table = params["defender_on_table"]
    defender_in_reserve = params["defender_in_reserve"]

    attacker_casualty_turns = params["attacker_casualty_turns"].copy()
    defender_casualty_turns = params["defender_casualty_turns"].copy()

    first_obj_turn = params["first_obj_turn"]
    second_obj_turn = params["second_obj_turn"]
    defender_retakes_turn = params["defender_retakes_turn"]
    attacker_retakes_turn = params["attacker_retakes_turn"]

    # Track state
    attacker_bp = 0
    defender_bp = 0

    attacker_objectives = 0
    defender_objectives = 3  # Defender controls all at start

    turn = 0
    winner = None

    break_trigger_event = None

    def check_break(side: str, trigger: str) -> bool:
        """Check if a side breaks at trigger event"""
        nonlocal winner, break_trigger_event
        if side == "attacker":
            if attacker_bp >= attacker_bl:
                if verbose:
                    print(f"  ATTACKER BREAKS! ({trigger}) - {attacker_bp}/{attacker_bl} BP")
                winner = "Defender"
                break_trigger_event = f"attacker_{trigger.replace(' ', '_')}"
                return True
        else:
            if defender_bp >= defender_bl:
                if verbose:
                    print(f"  DEFENDER BREAKS! ({trigger}) - {defender_bp}/{defender_bl} BP")
                winner = "Attacker"
                break_trigger_event = f"defender_{trigger.replace(' ', '_')}"
                return True
        return False

    while winner is None:
        turn += 1

        if verbose:
            print(f"\n=== TURN {turn} ===")
            print(f"Attacker: {attacker_bp}/{attacker_bl} BP, {attacker_units_remaining} units, {attacker_objectives} obj")
            print(f"Defender: {defender_bp}/{defender_bl} BP, {defender_units_remaining} units ({defender_on_table} on table, {defender_in_reserve} reserve), {defender_objectives} obj")

        # Defender reserves: 50% on turn 3, 25% each turn after
        if defender_in_reserve > 0:
            if turn == 3:
                if random.random() < 0.50:
                    defender_in_reserve -= 1
                    defender_on_table += 1
                    if verbose:
                        print(f"  Defender reserves arrive! (50% chance)")
            elif turn > 3:
                if random.random() < 0.25:
                    defender_in_reserve -= 1
                    defender_on_table += 1
                    if verbose:
                        print(f"  Defender reserves arrive! (25% chance)")

        # Objective changes - TRIGGER EVENTS

        # Attacker captures first objective
        if turn == first_obj_turn and attacker_objectives == 0:
            attacker_objectives = 1
            defender_objectives = 2
            if verbose:
                print(f"  Attacker captures first objective!")
            if check_break("defender", "lost objective"):
                break

        # Attacker captures second objective
        if turn == second_obj_turn and attacker_objectives == 1:
            attacker_objectives = 2
            defender_objectives = 1
            if verbose:
                print(f"  Attacker captures second objective!")
            if check_break("defender", "lost objective"):
                break

        # Defender retakes an objective
        if defender_retakes_turn and turn == defender_retakes_turn and attacker_objectives > 0:
            attacker_objectives -= 1
            defender_objectives += 1
            if verbose:
                print(f"  Defender retakes an objective!")
            if check_break("attacker", "lost objective"):
                break

        # Attacker retakes after defender retook
        if attacker_retakes_turn and turn == attacker_retakes_turn and defender_retakes_turn and turn > defender_retakes_turn:
            attacker_objectives += 1
            defender_objectives -= 1
            if verbose:
                print(f"  Attacker retakes the objective!")
            if check_break("defender", "lost objective"):
                break

        if winner:
            break

        # Casualties - TRIGGER EVENTS

        # Attacker casualties
        if attacker_casualty_turns and turn == attacker_casualty_turns[0]:
            attacker_casualty_turns.pop(0)
            if attacker_units_remaining > 0:
                attacker_units_remaining -= 1
                if verbose:
                    print(f"  Attacker loses a unit!")
                for _ in range(config.rolls_per_unit_destroyed):
                    attacker_bp += generate_bp(config.bp_table)
                if check_break("attacker", "unit destroyed"):
                    break

        if winner:
            break

        # Defender casualties (only from units on table)
        if defender_casualty_turns and turn == defender_casualty_turns[0]:
            defender_casualty_turns.pop(0)
            if defender_on_table > 0:
                defender_on_table -= 1
                defender_units_remaining -= 1
                if verbose:
                    print(f"  Defender loses a unit!")
                for _ in range(config.rolls_per_unit_destroyed):
                    defender_bp += generate_bp(config.bp_table)
                if check_break("defender", "unit destroyed"):
                    break

        if winner:
            break

        # End of turn BP from objectives (NOT trigger events)

        # Attacker objective bleeding
        if config.attacker_threshold == "all":
            if attacker_objectives < 3:
                attacker_bp += generate_bp(config.bp_table)
                if verbose:
                    print(f"  Attacker generates BP (doesn't control all objectives)")
        else:  # "any"
            if attacker_objectives < 1:
                attacker_bp += generate_bp(config.bp_table)
                if verbose:
                    print(f"  Attacker generates BP (doesn't control any objectives)")

        # Defender territory bleeding (enemy on their side of table)
        if config.defender_territory_bleed > 0 and turn >= config.defender_territory_bleed:
            if config.territory_bleed_flat:
                defender_bp += 1  # Flat 1 BP
            else:
                defender_bp += generate_bp(config.bp_table)  # Rolled 1-3 BP
            if verbose:
                print(f"  Defender generates BP (enemy on their territory)")

        # Defender objective bleeding (only for objectives they don't control)
        uncontrolled = 3 - defender_objectives
        for _ in range(uncontrolled):
            defender_bp += generate_bp(config.bp_table)
        if verbose and uncontrolled > 0:
            print(f"  Defender generates BP for {uncontrolled} uncontrolled objective(s)")

        if verbose:
            print(f"  End of turn - Attacker: {attacker_bp}/{attacker_bl} BP, Defender: {defender_bp}/{defender_bl} BP")

        # Check for elimination
        if attacker_units_remaining <= 0:
            winner = "Defender"
            if verbose:
                print(f"  Attacker eliminated!")
        elif defender_units_remaining <= 0:
            winner = "Attacker"
            if verbose:
                print(f"  Defender eliminated!")
        elif turn >= 30:  # Safety cap
            winner = "Draw (turn limit)"

    # Determine end trigger
    end_trigger = "unknown"
    if winner == "Defender" and attacker_bp >= attacker_bl:
        end_trigger = "attacker_broke"
    elif winner == "Attacker" and defender_bp >= defender_bl:
        end_trigger = "defender_broke"
    elif winner == "Defender" and attacker_units_remaining <= 0:
        end_trigger = "attacker_eliminated"
    elif winner == "Attacker" and defender_units_remaining <= 0:
        end_trigger = "defender_eliminated"
    elif "Draw" in str(winner):
        end_trigger = "turn_limit"

    return {
        "winner": winner,
        "turns": turn,
        "attacker_bp": attacker_bp,
        "attacker_bl": attacker_bl,
        "defender_bp": defender_bp,
        "defender_bl": defender_bl,
        "attacker_units_start": params["attacker_units"],
        "defender_units_start": params["defender_units"],
        "attacker_units_lost": params["attacker_units"] - attacker_units_remaining,
        "defender_units_lost": params["defender_units"] - defender_units_remaining,
        "first_obj_turn": first_obj_turn,
        "end_trigger": end_trigger,
        "attacker_objectives": attacker_objectives,
        "break_trigger_event": break_trigger_event,
    }


def run_comparison(num_games_per_config: int = 1000):
    """Run comparison across different rule configurations"""

    configs = [
        # (name, bp_table, threshold, rolls, defender_territory_bleed, territory_flat)
        ("BASELINE (old BL, no territory)", "current", "all", 2, 0, False),
        ("new BL only (no territory)", "current", "all", 2, 0, False),  # need to modify BL separately
        ("new BL + territory (CURRENT BP table)", "current", "all", 2, 2, False),
        ("new BL + territory (NEW BP table)", "proposed", "all", 2, 2, False),
    ]

    print("\n" + "="*70)
    print("  HAIL OF FIRE - BREAK POINT SIMULATION v2")
    print(f"  Running {num_games_per_config} games per configuration")
    print("="*70)

    all_results = []

    for name, bp_table, threshold, rolls, territory_bleed, territory_flat in configs:
        config = SimConfig(
            bp_table=bp_table,
            attacker_threshold=threshold,
            rolls_per_unit_destroyed=rolls,
            defender_territory_bleed=territory_bleed,
            territory_bleed_flat=territory_flat,
        )

        results = {
            "attacker_wins": 0,
            "defender_wins": 0,
            "draws": 0,
            "total_turns": 0,
            "attacker_bp_totals": [],
            "defender_bp_totals": [],
            "end_triggers": {},
            "end_turns": [],
            "attacker_obj_at_end": [],
            "break_events": {},
        }

        for _ in range(num_games_per_config):
            game = simulate_game(config)

            if game["winner"] == "Attacker":
                results["attacker_wins"] += 1
            elif game["winner"] == "Defender":
                results["defender_wins"] += 1
            else:
                results["draws"] += 1

            results["total_turns"] += game["turns"]
            results["attacker_bp_totals"].append(game["attacker_bp"])
            results["defender_bp_totals"].append(game["defender_bp"])

            # Track end triggers
            trigger = game["end_trigger"]
            results["end_triggers"][trigger] = results["end_triggers"].get(trigger, 0) + 1
            results["end_turns"].append(game["turns"])
            results["attacker_obj_at_end"].append(game["attacker_objectives"])

            # Track specific break events
            if game["break_trigger_event"]:
                evt = game["break_trigger_event"]
                results["break_events"][evt] = results["break_events"].get(evt, 0) + 1

        results["avg_turns"] = results["total_turns"] / num_games_per_config
        results["avg_attacker_bp"] = sum(results["attacker_bp_totals"]) / num_games_per_config
        results["avg_defender_bp"] = sum(results["defender_bp_totals"]) / num_games_per_config
        results["attacker_win_rate"] = results["attacker_wins"] / num_games_per_config * 100
        results["defender_win_rate"] = results["defender_wins"] / num_games_per_config * 100
        results["draw_rate"] = results["draws"] / num_games_per_config * 100

        print(f"\n{'='*70}")
        print(f"  {name}")
        print(f"{'='*70}")
        print(f"  Attacker Win Rate: {results['attacker_win_rate']:.1f}%")
        print(f"  Defender Win Rate: {results['defender_win_rate']:.1f}%")
        print(f"  Draw Rate: {results['draw_rate']:.1f}%")
        print(f"  Average Game Length: {results['avg_turns']:.1f} turns")
        print(f"  Average Attacker BP at game end: {results['avg_attacker_bp']:.1f}")
        print(f"  Average Defender BP at game end: {results['avg_defender_bp']:.1f}")
        print(f"  Break Trigger Events (what caused the break check):")
        for evt, count in sorted(results['break_events'].items(), key=lambda x: -x[1]):
            pct = count / num_games_per_config * 100
            print(f"    {evt}: {pct:.1f}%")

        all_results.append((name, results))

    # Summary table
    print("\n" + "="*70)
    print("  SUMMARY TABLE")
    print("="*70)
    print(f"{'Configuration':<40} {'Atk%':>7} {'Def%':>7} {'Draw%':>7} {'Turns':>6}")
    print("-"*70)
    for name, results in all_results:
        print(f"{name:<40} {results['attacker_win_rate']:>6.1f}% {results['defender_win_rate']:>6.1f}% {results['draw_rate']:>6.1f}% {results['avg_turns']:>6.1f}")


if __name__ == "__main__":
    # Run the comparison
    run_comparison(num_games_per_config=1000)

    # Run a verbose example game
    print("\n" + "="*70)
    print("  EXAMPLE GAME (Current Rules, Verbose)")
    print("="*70)

    example_config = SimConfig(
        bp_table="current",
        attacker_threshold="all",
        rolls_per_unit_destroyed=2,
    )

    result = simulate_game(example_config, verbose=True)
    print(f"\nGame ended on turn {result['turns']}: {result['winner']} wins!")
    print(f"First objective captured on turn: {result['first_obj_turn']}")
