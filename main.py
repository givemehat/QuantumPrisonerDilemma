"""
Entry point for the Quantum Prisoner's Dilemma project.
"""

from __future__ import annotations

import argparse
import sys

from analysis import GameAnalysis
from simulation import SimulationConfig, SimulationRunner


def bounded_probability(value: str) -> float:
    """
    Argparse helper for validating probabilities.
    """
    try:
        prob = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "Probability must be a numeric value."
        ) from exc

    if prob < 0 or prob > 1:
        raise argparse.ArgumentTypeError("Probability must be between 0 and 1.")
    return prob


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Quantum Prisoner's Dilemma with SQLite logging and analysis."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a simulation experiment.")
    run_parser.add_argument(
        "--player-a",
        type=bounded_probability,
        required=True,
        help="Player A cooperation probability.",
    )
    run_parser.add_argument(
        "--player-b",
        type=bounded_probability,
        required=True,
        help="Player B cooperation probability.",
    )
    run_parser.add_argument(
        "--iterations",
        type=int,
        default=1000,
        help="Number of runs for the experiment.",
    )

    analyze_parser = subparsers.add_parser("analyze", help="Analyze stored results.")
    analyze_parser.add_argument(
        "--plots", action="store_true", help="Display matplotlib plots."
    )

    return parser


def run_simulation(player_a: float, player_b: float, iterations: int) -> None:
    runner = SimulationRunner()
    config = SimulationConfig(
        player_a_prob=player_a,
        player_b_prob=player_b,
        iterations=iterations,
    )
    runner.run_experiment(config)
    print(
        f"Simulation complete: {iterations} runs stored "
        f"for Player A={player_a:.2f}, Player B={player_b:.2f}"
    )


def run_analysis(show_plots: bool) -> None:
    analysis = GameAnalysis()
    analysis.print_summary()

    if show_plots:
        analysis.plot_outcome_distribution()
        analysis.plot_scores_over_runs()
        analysis.plot_probability_vs_score()


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "run":
            run_simulation(args.player_a, args.player_b, args.iterations)
        elif args.command == "analyze":
            run_analysis(args.plots)
        else:
            parser.print_help()
            return 1
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
