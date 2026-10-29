
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from day19.evaluation_schemas import (
    AgentRunRecord,
    EvaluationSummary,
)
from day19.result_store import save_benchmark_result


def main():
    # 使用现有 Pydantic 模型生成模拟测试数据
    record = AgentRunRecord.model_construct(
        run_id="test_run_001",
        question="Analyze RWA protocols",
        started_at_utc="2026-10-29T12:00:00+00:00",
        success=True,
        latency_seconds=7.06,
        evidence_coverage=1.0,
        claim_completeness=1.0,
        input_tokens=None,
        output_tokens=None,
        estimated_cost_usd=None,
        error_message=None,
    )

    summary = EvaluationSummary.model_construct(
        total_runs=1,
        successful_runs=1,
        failed_runs=0,
        success_rate=1.0,
        average_latency_seconds=7.06,
        p95_latency_seconds=7.06,
        average_evidence_coverage=1.0,
        average_claim_completeness=1.0,
        total_estimated_cost_usd=None,
    )

    # 临时目录：测试结束后自动清理
    with TemporaryDirectory() as temp_dir:
        saved_path = save_benchmark_result(
            records=[record],
            summary=summary,
            output_dir=temp_dir,
        )

        path = Path(saved_path)

        # 1. 验证文件确实存在
        assert path.exists()

        # 2. 验证文件能够解析为 JSON
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        # 3. 验证保存的数据正确
        assert len(data["records"]) == 1
        assert data["records"][0]["run_id"] == "test_run_001"
        assert data["records"][0]["success"] is True

        assert data["summary"]["total_runs"] == 1
        assert data["summary"]["success_rate"] == 1.0

        assert "generated_at_utc" in data

        print("File creation test passed!")
        print("JSON readback test passed!")
        print("Record consistency test passed!")
        print("Benchmark result store tests passed!")


if __name__ == "__main__":
    main()
