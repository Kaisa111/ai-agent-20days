
from typing import Literal

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field


# 1. 加载环境变量
load_dotenv()

client = OpenAI()


# 2. 定义结构化任务计划
class ResearchPlan(BaseModel):

    route: Literal["crypto", "rwa", "both", "other"] = Field(
        description="Which research agents should handle the question."
    )

    crypto_question: str = Field(
        description="Subtask for the Crypto Agent. Empty if not needed."
    )

    rwa_question: str = Field(
        description="Subtask for the RWA Agent. Empty if not needed."
    )

    requires_live_data: bool = Field(
        description="Whether answering requires current external information."
    )


# 3. 定义 Planner 函数
def create_research_plan(question: str) -> ResearchPlan:

    response = client.responses.parse(
        model="gpt-4.1-mini",

        instructions=(
            "You are a research task planner. "
            "Your job is to analyze the user's question "
            "and create a structured research plan. "

            "Choose route='crypto' for cryptocurrency-only questions. "
            "Choose route='rwa' for real-world asset tokenization questions. "
            "Choose route='both' when both domains are required. "
            "Choose route='other' when neither domain is relevant. "

            "Generate focused, independent subtasks for each required agent. "
            "Preserve the user's actual research objectives. "
            "Strictly isolate agent responsibilities. "
            "The Crypto Agent must research only cryptocurrency-related facts, "
            "risks, metrics, and mechanisms. "
            "The RWA Agent must research only tokenized real-world asset facts, "
            "risks, metrics, and mechanisms. "
            "Do not ask either agent to compare its domain with the other domain. "
            "For cross-domain comparison requests, create independent subtasks "
            "that examine the same requested dimensions. "
            "The final comparison will be performed by a separate synthesizer. "
            "Use an empty string for any unused subtask. "

            "Set requires_live_data=True when the question needs "
            "current prices, yields, news, or other time-sensitive data. "

            "Do not answer the user's question. "
            "Only produce the research plan."
        ),

        input=[
            {
                "role": "user",
                "content": question,
            }
        ],

        text_format=ResearchPlan,
    )

    plan = response.output_parsed

    if plan is None:
        raise RuntimeError("Planner did not return a valid research plan.")

    return plan


# 4. 本地测试
if __name__ == "__main__":

    test_cases = [
        {
            "question": "What is the current BTC price?",
            "expected_route": "crypto",
            "expected_live_data": True,
        },
        {
            "question": "What are the legal ownership risks of RWA tokenization?",
            "expected_route": "rwa",
            "expected_live_data": False,
        },
        {
            "question": (
                "Compare Bitcoin and tokenized Treasury bonds "
                "in terms of liquidity and custody risks."
            ),
            "expected_route": "both",
            "expected_live_data": False,
        },
        {
            "question": "How do I cook fried rice?",
            "expected_route": "other",
            "expected_live_data": False,
        },
        {
            "question": "Compare the latest Bitcoin price with current tokenized Treasury yields.",
            "expected_route": "both",
            "expected_live_data": True,
        },
    ]

    passed = 0

    for index, case in enumerate(test_cases, start=1):

        print(f"\n{'=' * 60}")
        print(f"Test {index}")
        print("Question:", case["question"])

        plan = create_research_plan(case["question"])

        print(plan.model_dump_json(indent=2))

        route_ok = plan.route == case["expected_route"]
        live_ok = (
            plan.requires_live_data
            == case["expected_live_data"]
        )

        # 检查未使用的子任务是否为空
        unused_ok = (
            (plan.route in ("crypto", "both") or plan.crypto_question == "")
            and
            (plan.route in ("rwa", "both") or plan.rwa_question == "")
        )

        # 检查需要的子任务是否存在
        required_ok = (
            (plan.route not in ("crypto", "both") or bool(plan.crypto_question.strip()))
            and
            (plan.route not in ("rwa", "both") or bool(plan.rwa_question.strip()))
        )

        success = route_ok and live_ok and unused_ok and required_ok

        print("Route check:", route_ok)
        print("Live data check:", live_ok)
        print("Subtask check:", unused_ok and required_ok)
        print("Result:", "PASS" if success else "FAIL")

        if success:
            passed += 1

    print(f"\nFinal Score: {passed}/{len(test_cases)}")
