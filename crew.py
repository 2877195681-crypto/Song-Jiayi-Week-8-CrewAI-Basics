import os
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO

from crewai import Agent, Crew, LLM, Process, Task  # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv


def create_crew() -> Crew:
    load_dotenv()

    llm = LLM(
        model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        base_url=os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com"),
        api_key=os.getenv("DEEPSEEK_API_KEY"),
    )

    market_research_specialist = Agent(
        role="Hong Kong Tourism Market Research Specialist",
        goal=(
            "Within one run, identify at least 5 current Hong Kong tourism trends "
            "and compare at least 3 direct competitors using evidence-based notes."
        ),
        backstory=(
            "You spent 8 years as a destination intelligence consultant for tourism "
            "boards in Asia. You are trained to separate short-term hype from real "
            "market shifts by checking demand signals, visitor behavior, and "
            "competitor actions. You are careful with claims, and you organize "
            "findings in a way business teams can act on quickly."
        ),
        llm=llm,
        verbose=True,
    )

    business_data_analyst = Agent(
        role="Tourism Business Data Analyst",
        goal=(
            "Convert research findings into a decision brief that includes at least "
            "4 high-impact opportunities, 4 key risks, and 3 practical mitigation actions."
        ),
        backstory=(
            "You previously worked in strategy and analytics for a regional travel "
            "group managing hotels, tours, and attraction partnerships. You focus "
            "on measurable outcomes such as demand, pricing pressure, margin impact, "
            "and operational feasibility. You challenge weak assumptions and rank "
            "recommendations by business value and implementation risk."
        ),
        llm=llm,
        verbose=True,
    )

    business_report_writer = Agent(
        role="Executive Business Report Writer",
        goal=(
            "Produce one professional executive report with clear sections "
            "(market trends, competitor landscape, opportunities, risks, and recommendations) "
            "plus a concise one-page style executive summary."
        ),
        backstory=(
            "You are a former management consulting writer known for turning complex "
            "analysis into board-ready narratives. You write with a formal and clear "
            "tone, highlight what matters most for decision makers, and keep every "
            "section action-oriented. You ensure the final report is structured, "
            "credible, and easy for executives to review."
        ),
        llm=llm,
        verbose=True,
    )

    task1 = Task(
        description=(
            "Research the tourism market in Hong Kong and produce evidence-based market intelligence. "
            "Identify at least 5 current tourism trends and compare at least 3 direct competitors "
            "in terms of positioning, target segments, offerings, and strengths/weaknesses."
        ),
        expected_output=(
            "A structured market research brief in markdown with these sections: "
            "1) Hong Kong tourism trends (minimum 5), "
            "2) competitor comparison table (minimum 3 competitors), "
            "3) key market insights and implications."
        ),
        agent=market_research_specialist,
    )

    task2 = Task(
        description=(
            "Analyze Task 1 findings on the tourism market in Hong Kong to identify business opportunities "
            "and risks. Prioritize issues based on expected impact and feasibility, and define practical "
            "mitigation actions for key risks."
        ),
        expected_output=(
            "A decision brief in markdown containing: "
            "1) at least 4 high-impact opportunities, "
            "2) at least 4 key risks, "
            "3) at least 3 mitigation actions, "
            "4) a simple priority ranking (high/medium/low) with short rationale."
        ),
        agent=business_data_analyst,
        context=[task1],
    )

    task3 = Task(
        description=(
            "Write a professional executive report about the tourism market in Hong Kong by combining "
            "the research and analysis from Task 1 and Task 2. The report should be concise, credible, "
            "and action-oriented for senior decision makers."
        ),
        expected_output=(
            "A polished executive report in markdown with: "
            "1) executive summary, "
            "2) market trends section, "
            "3) competitor landscape section, "
            "4) opportunities section, "
            "5) risks and mitigation section, "
            "6) final strategic recommendations."
        ),
        agent=business_report_writer,
        context=[task1, task2],
    )

    return Crew(
        agents=[
            market_research_specialist,
            business_data_analyst,
            business_report_writer,
        ],
        tasks=[task1, task2, task3],
        process=Process.sequential,
        verbose=True,
    )


def _is_clean_char(ch: str) -> bool:
    code = ord(ch)
    return ch in "\n\r\t" or 32 <= code <= 126


def _clean_line(line: str) -> str:
    return "".join(ch for ch in line if _is_clean_char(ch))


def _is_decorative_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if "Traceback" in stripped:
        return False
    if "Final Answer:" in stripped:
        return False
    if "Task Started" in stripped or "Task Completed" in stripped:
        return False
    if "Crew Execution Started" in stripped or "Crew Execution Completed" in stripped:
        return False
    if "Agent:" in stripped or "Task:" in stripped or "Name:" in stripped or "ID:" in stripped:
        return False
    return not any(ch.isalnum() for ch in stripped)


if __name__ == "__main__":
    crew = create_crew()
    buffer = StringIO()
    with redirect_stdout(buffer), redirect_stderr(buffer):
        result = crew.kickoff(inputs={"topic": "tourism market in Hong Kong"})

    raw_output = buffer.getvalue()
    cleaned_lines = []
    for line in raw_output.splitlines():
        clean_line = _clean_line(line)
        if _is_decorative_line(clean_line):
            continue
        cleaned_lines.append(clean_line)

    cleaned_text = "\n".join(cleaned_lines).strip()
    final_text = (
        f"{cleaned_text}\n\n=== FINAL RESULT ===\n\n{result}"
        if cleaned_text
        else f"=== FINAL RESULT ===\n\n{result}"
    )

    with open("output_clean.txt", "w", encoding="utf-8") as file:
        file.write(final_text)

    print(result)
