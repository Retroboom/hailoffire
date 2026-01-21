import random
from dataclasses import dataclass
from typing import Literal

@dataclass
class SimConfig:
    # BP roll table
    bp_table: Literal["current", "proposed"]  # current: 1-3=1, 4-5=2, 6=3 | proposed: 1-2=1, 3-5=2, 6=3

    # Attacker objective threshold
    attacker_threshold: Literal["all", "any"]  # "all" = bleeds until 3, "any" = bleeds until 1

    # Rolls per unit destroyed
    rolls_per_unit_destroyed: int  # 2 (current) or 1 (proposed)

    # Force sizes
    attacker_units: int
    defender_units: int

    # Turn attacker captures first objective
    first_objective_turn: int

    # Casualty rates (probability per turn of losing a unit)
    attacker_casualty_rate: float  # e.g., 0.25 = 1 unit per 4 turns on average
    defender_casualty_rate: float

    # Turn casualties start
    attacker_casualties_start_turn: int
    defender_casualties_start_turn: int

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

def simulate_game(config: SimConfig, verbose: bool = False) -> dict:
    """Simulate a single game and return results"""

    # Calculate break limits
    attacker_bl = 5 + (2 * config.attacker_units)
    defender_bl = 5 + (2 * config.defender_units)

    # Track state
    attacker_bp = 0
    defender_bp = 0
    attacker_units_remaining = config.attacker_units
    defender_units_remaining = config.defender_units
    defender_units_on_table = config.defender_units // 2  # Half start in reserve
    defender_reserves = config.defender_units - defender_units_on_table
    reserves_arrived = 0

    attacker_objectives = 0
    defender_objectives = 3  # Defender controls all at start (hidden teams)

    turn = 0
    winner = None

    def check_break(side: str, trigger: str) -> bool:
        """
        Check if a side breaks. Per rules: breaking only happens when
        you lose an objective or unit AND your BP >= BL at that moment.
        """
        nonlocal winner
        if side == "attacker":
            if attacker_bp >= attacker_bl:
                if verbose:
                    print(f"  ATTACKER BREAKS! ({trigger}) - {attacker_bp}/{attacker_bl} BP")
                winner = "Defender"
                return True
        else:  # defender
            if defender_bp >= defender_bl:
                if verbose:
                    print(f"  DEFENDER BREAKS! ({trigger}) - {defender_bp}/{defender_bl} BP")
                winner = "Attacker"
                return True
        return False

    while winner is None:
        turn += 1

        if verbose:
            print(f"\n=== TURN {turn} ===")
            print(f"Attacker: {attacker_bp}/{attacker_bl} BP, {attacker_units_remaining} units")
            print(f"Defender: {defender_bp}/{defender_bl} BP, {defender_units_remaining} units ({defender_units_on_table} on table, {defender_reserves} in reserve)")

        # Defender reserves (turn 3+)
        if turn >= 3 and defender_reserves > 0:
            target = 4 + reserves_arrived
            if target <= 6:
                if roll_d6() >= target:
                    defender_reserves -= 1
                    defender_units_on_table += 1
                    reserves_arrived += 1
                    if verbose:
                        print(f"  Defender reserves arrive! (target was {target}+)")

        # Attacker captures first objective - this is a TRIGGER EVENT for defender
        if turn == config.first_objective_turn and attacker_objectives == 0:
            attacker_objectives = 1
            defender_objectives = 2
            if verbose:
                print(f"  Attacker captures first objective!")
            # Defender loses an objective - check if defender breaks
            if check_break("defender", "lost objective"):
                break

        # Casualties - each is a TRIGGER EVENT
        if turn >= config.attacker_casualties_start_turn and attacker_units_remaining > 0:
            if random.random() < config.attacker_casualty_rate:
                attacker_units_remaining -= 1
                if verbose:
                    print(f"  Attacker loses a unit!")
                # Generate BP from this casualty
                for _ in range(config.rolls_per_unit_destroyed):
                    attacker_bp += generate_bp(config.bp_table)
                # Check if attacker breaks (unit destroyed is trigger)
                if check_break("attacker", "unit destroyed"):
                    break

        if winner:
            break

        if turn >= config.defender_casualties_start_turn and defender_units_on_table > 0:
            if random.random() < config.defender_casualty_rate:
                defender_units_on_table -= 1
                defender_units_remaining -= 1
                if verbose:
                    print(f"  Defender loses a unit!")
                # Generate BP from this casualty
                for _ in range(config.rolls_per_unit_destroyed):
                    defender_bp += generate_bp(config.bp_table)
                # Check if defender breaks (unit destroyed is trigger)
                if check_break("defender", "unit destroyed"):
                    break

        if winner:
            break

        # Generate BP from objectives (end of turn) - these are NOT trigger events
        # They accumulate BP but don't cause breaking by themselves
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

        # Defender objective BP
        if attacker_objectives >= 1:
            uncontrolled = 3 - defender_objectives
            for _ in range(uncontrolled):
                defender_bp += generate_bp(config.bp_table)
            if verbose and uncontrolled > 0:
                print(f"  Defender generates BP for {uncontrolled} uncontrolled objectives")

        if verbose:
            print(f"  End of turn - Attacker: {attacker_bp}/{attacker_bl} BP, Defender: {defender_bp}/{defender_bl} BP")

        # Check for elimination (no units left)
        if attacker_units_remaining <= 0:
            winner = "Defender"
            if verbose:
                print(f"  Attacker eliminated!")
        elif defender_units_remaining <= 0:
            winner = "Attacker"
            if verbose:
                print(f"  Defender eliminated!")
        elif turn >= 20:  # Safety cap
            winner = "Draw (turn limit)"

    return {
        "winner": winner,
        "turns": turn,
        "attacker_bp": attacker_bp,
        "attacker_bl": attacker_bl,
        "defender_bp": defender_bp,
        "defender_bl": defender_bl,
        "attacker_units_lost": config.attacker_units - attacker_units_remaining,
        "defender_units_lost": config.defender_units - defender_units_remaining,
    }

def run_simulations(config: SimConfig, num_games: int = 1000) -> dict:
    """Run multiple simulations and aggregate results"""
    results = {
        "attacker_wins": 0,
        "defender_wins": 0,
        "draws": 0,
        "total_turns": 0,
        "attacker_bp_totals": [],
        "defender_bp_totals": [],
        "game_lengths": [],
    }

    for _ in range(num_games):
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
        results["game_lengths"].append(game["turns"])

    results["avg_turns"] = results["total_turns"] / num_games
    results["avg_attacker_bp"] = sum(results["attacker_bp_totals"]) / num_games
    results["avg_defender_bp"] = sum(results["defender_bp_totals"]) / num_games
    results["attacker_win_rate"] = results["attacker_wins"] / num_games * 100
    results["defender_win_rate"] = results["defender_wins"] / num_games * 100

    return results

def print_results(name: str, results: dict):
    """Pretty print simulation results"""
    print(f"\n{'='*60}")
    print(f"  {name}")
    print(f"{'='*60}")
    print(f"  Attacker Win Rate: {results['attacker_win_rate']:.1f}%")
    print(f"  Defender Win Rate: {results['defender_win_rate']:.1f}%")
    print(f"  Average Game Length: {results['avg_turns']:.1f} turns")
    print(f"  Average Attacker BP at game end: {results['avg_attacker_bp']:.1f}")
    print(f"  Average Defender BP at game end: {results['avg_defender_bp']:.1f}")

def generate_random_config(
    bp_table: str,
    attacker_threshold: str,
    rolls_per_unit: int
) -> SimConfig:
    """Generate a random but realistic game configuration"""

    # Force sizes: 80% are 5-7, rest are 4 or 8-10
    def pick_force_size():
        if random.random() < 0.8:
            return random.randint(5, 7)
        else:
            return random.choice([4, 8, 9, 10])

    attacker_units = pick_force_size()
    defender_units = random.randint(5, 7)  # Defender typically 5-7

    # First objective captured turn 5-7
    first_obj_turn = random.randint(5, 7)

    return SimConfig(
        bp_table=bp_table,
        attacker_threshold=attacker_threshold,
        rolls_per_unit_destroyed=rolls_per_unit,
        attacker_units=attacker_units,
        defender_units=defender_units,
        first_objective_turn=first_obj_turn,
        attacker_casualty_rate=0.25,  # 1 per 4 turns
        defender_casualty_rate=0.25,  # 1 per 4 turns
        attacker_casualties_start_turn=5,  # No casualties first 4 turns
        defender_casualties_start_turn=5,
    )

def run_comparison(num_games_per_config: int = 1000):
    """Run comparison across different rule configurations"""

    configs = [
        ("CURRENT RULES", "current", "all", 2),
        ("Proposed: 'any' objective only", "current", "any", 2),
        ("Proposed: new BP table only", "proposed", "all", 2),
        ("Proposed: 1 roll per unit only", "current", "all", 1),
        ("Proposed: 'any' + new BP table", "proposed", "any", 2),
        ("Proposed: 'any' + 1 roll per unit", "current", "any", 1),
        ("Proposed: new BP table + 1 roll", "proposed", "all", 1),
        ("Proposed: ALL THREE CHANGES", "proposed", "any", 1),
    ]

    print("\n" + "="*60)
    print("  HAIL OF FIRE - BREAK POINT SIMULATION")
    print(f"  Running {num_games_per_config} games per configuration")
    print("="*60)

    all_results = []

    for name, bp_table, threshold, rolls in configs:
        # Run many games with randomized force sizes
        combined_results = {
            "attacker_wins": 0,
            "defender_wins": 0,
            "draws": 0,
            "total_turns": 0,
            "attacker_bp_totals": [],
            "defender_bp_totals": [],
            "game_lengths": [],
        }

        for _ in range(num_games_per_config):
            config = generate_random_config(bp_table, threshold, rolls)
            game = simulate_game(config)

            if game["winner"] == "Attacker":
                combined_results["attacker_wins"] += 1
            elif game["winner"] == "Defender":
                combined_results["defender_wins"] += 1
            else:
                combined_results["draws"] += 1

            combined_results["total_turns"] += game["turns"]
            combined_results["attacker_bp_totals"].append(game["attacker_bp"])
            combined_results["defender_bp_totals"].append(game["defender_bp"])
            combined_results["game_lengths"].append(game["turns"])

        combined_results["avg_turns"] = combined_results["total_turns"] / num_games_per_config
        combined_results["avg_attacker_bp"] = sum(combined_results["attacker_bp_totals"]) / num_games_per_config
        combined_results["avg_defender_bp"] = sum(combined_results["defender_bp_totals"]) / num_games_per_config
        combined_results["attacker_win_rate"] = combined_results["attacker_wins"] / num_games_per_config * 100
        combined_results["defender_win_rate"] = combined_results["defender_wins"] / num_games_per_config * 100

        print_results(name, combined_results)
        all_results.append((name, combined_results))

    # Summary table
    print("\n" + "="*60)
    print("  SUMMARY TABLE")
    print("="*60)
    print(f"{'Configuration':<40} {'Atk%':>6} {'Def%':>6} {'Turns':>6}")
    print("-"*60)
    for name, results in all_results:
        print(f"{name:<40} {results['attacker_win_rate']:>5.1f}% {results['defender_win_rate']:>5.1f}% {results['avg_turns']:>6.1f}")

if __name__ == "__main__":
    # Run the comparison
    run_comparison(num_games_per_config=10000)

    # Also run a single verbose game to see the mechanics
    print("\n" + "="*60)
    print("  EXAMPLE GAME (Current Rules, Verbose)")
    print("="*60)

    example_config = SimConfig(
        bp_table="current",
        attacker_threshold="all",
        rolls_per_unit_destroyed=2,
        attacker_units=6,
        defender_units=6,
        first_objective_turn=5,
        attacker_casualty_rate=0.25,
        defender_casualty_rate=0.25,
        attacker_casualties_start_turn=5,
        defender_casualties_start_turn=5,
    )

    result = simulate_game(example_config, verbose=True)
    print(f"\nGame ended on turn {result['turns']}: {result['winner']} wins!")
