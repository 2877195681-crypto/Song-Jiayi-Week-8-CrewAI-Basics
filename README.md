# Hong Kong Tourism Crew - Documentation and Reflection

## 1) Business Problem Addressed

This crew addresses a strategic business problem in the Hong Kong tourism market: how to stay competitive in a fast-changing regional environment where traveler behavior, digital channels, and competitor positioning are shifting quickly. Tourism stakeholders need a practical way to move from raw market information to clear business decisions and then to executive-ready recommendations. The crew solves this by turning one topic ("tourism market in Hong Kong") into a structured workflow that produces trend intelligence, risk-opportunity analysis, and a final strategic report for decision makers.

## 2) How the 3 Agents Work Together

The three agents operate in sequence with clear handoff logic. First, the **Market Research Specialist** gathers and organizes tourism trends and competitor insights, creating the evidence base. Second, the **Business Data Analyst** uses the first output as context, evaluates implications, and identifies prioritized opportunities, risks, and mitigation actions. Third, the **Business Report Writer** takes both earlier outputs as context and converts them into a professional executive report with clear sections and action-oriented recommendations. This design ensures each agent has a focused responsibility while still building on prior work for consistency and depth.

## 3) Challenges Encountered and How They Were Solved

One major challenge was environment compatibility. Early runs failed because the default Python setup had dependency issues (version mismatch and package import errors). I resolved this by creating a dedicated Conda environment (`crew311`) with a compatible Python version and reinstalling required dependencies there, which made execution stable. Another challenge was log readability on Windows, where decorative Unicode output from CrewAI was garbled when redirected. To solve this, I updated `crew.py` to automatically capture stdout/stderr, clean out decorative characters, and save a readable `output_clean.txt` (later used as the main `output.txt`).

## 4) One Thing I Would Change with More Time

If I had more time, I would add a small evaluation layer to score output quality automatically (for example: coverage of required sections, clarity of recommendations, and evidence consistency). This would make the workflow not only generate reports, but also self-check whether each run meets a defined quality standard before delivery.

