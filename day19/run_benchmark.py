
import argparse

from day19.evaluation_runner import evaluate_agent
from day19.benchmark import summarize_runs

from day19.result_store import save_benchmark_result


def run_benchmark(
    question: str,
    runs: int = 3,
    limit: int = 3,
):
    if runs < 1:
        raise ValueError("runs must be at least 1")
    if limit < 1:
        raise ValueError("limit must be at least 1")

    records = []

    for index in range(1, runs + 1):
        print(f"\n[{index}/{runs}] Running Agent...")

        record = evaluate_agent(
            question=question,
            limit=limit,
        )

        records.append(record)

        print(
            f"Success: {record.success} | "
            f"Latency: {record.latency_seconds:.2f}s | "
            f"Coverage: {record.evidence_coverage:.1%}"
        )

        if record.error_message:
            print(f"Error: {record.error_message}")

    summary = summarize_runs(records)

    saved_path = save_benchmark_result(
    records=records,
    summary=summary,
)

    print(f"\nBenchmark JSON saved to: {saved_path}")

    return records, summary


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark the RWA Research Agent"
    )

    parser.add_argument(
        "--runs",
        type=int,
        default=3,
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=3,
    )

    parser.add_argument(
        "--question",
        type=str,
        default="What are the TVLs of the leading RWA protocols?",
    )

    args = parser.parse_args()

    records, summary = run_benchmark(
        question=args.question,
        runs=args.runs,
        limit=args.limit,
    )

    print("\n=== BENCHMARK SUMMARY ===")
    print(summary.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
