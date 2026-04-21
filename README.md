# ESG Report Generation Agent Based on Huazheng ESG Annual Rating Data

## Project Overview
This project develops a Track 3 Coze/Dify data analysis agent supported by a substantive Python workflow. The agent allows users to enter a **stock code** and generate a **full English ESG analysis report** for the corresponding company based on the **Huazheng Index ESG Annual Rating Database (2009–2024)**.

The project is designed to transform raw ESG rating data into a structured, user-friendly, and business-relevant report for investors, business students, researchers, and corporate analysts.

## Project Goal
Many users may know a company's stock code but cannot easily interpret raw ESG tables or compare performance across years. This project addresses that problem by using Python to clean, analyze, benchmark, and summarize ESG data, and then using an agent interface to present the result as a readable company-level ESG report.

## Track
**Track 3 – Coze/Dify Data Analysis Agent**

Track 3 requires:
- Coze/Dify link
- Python notebook
- workflow evidence
- 1–3 minute demo video
- reflection report

A key requirement is that the product must be supported by a **substantive Python workflow**, rather than relying only on generic model responses.

## Target Users
This project is intended for:
- ESG-conscious investors
- business students
- sustainability researchers
- corporate analysts
- users interested in responsible investment and company benchmarking

## Data Source
- **Dataset Name:** Huazheng Index ESG Annual Rating Database
- **Coverage Period:** 2009–2024
- **Data Scope:** Chinese A-share listed companies
- **Provider:** Huazheng Index
- **Access Date:** [Please fill in your actual access date]

## Key Variables
The main variables used in this project include:
- company name
- stock code
- year
- ESG rating

Additional variables used in the final analysis also include:
- ESG total score
- Environmental (E) score
- Social (S) score
- Governance (G) score
- industry classification
- industry percentile / industry benchmark information

## User Input and Output
### User Input
The agent takes **stock code** as the main user input.

Users can:
- input a stock code to retrieve a company ESG report
- request company-level ESG analysis
- compare the same company across different years
- view benchmark comparison against industry peers

### Final Output
After receiving the stock code, the agent generates a **full English ESG analysis report** for the selected company. The report is designed to include:
1. **Data Source & Cleaning Report**
2. **Target Company Confirmation**
3. **Full English ESG Analysis Report**
4. **Visualizations**
5. **Conclusion and recommendations**

This means the product does not only return a short answer. Instead, it produces a structured analytical report grounded in actual ESG data processing.

---

## Final Report Structure

### 1. Data Source & Cleaning Report
This section reports the data source and data quality information used in the workflow.

Example output:
- Total rows of raw data: 52,453
- Total columns of raw data: 15
- Data source: Huazheng Index ESG Annual Rating Database (2009–2024)
- Total valid rows after full cleaning: 52,452
- Number of invalid rows removed: 1
- Number of covered listed companies: 5,461
- Number of covered industries: 338

This part demonstrates that the workflow includes real preprocessing rather than directly relying on unprocessed raw data.

### 2. Target Company Confirmation
After the user enters a stock code, the system identifies the matched company and confirms the analysis target.

Example output:
- Company Name: 蓝色光标
- Stock Code: 300058
- Industry: 营销代理
- Peer Companies: 省广集团, 易点天下, 三人行

This section ensures that the user can verify whether the selected company has been matched correctly before reading the detailed report.

### 3. Full English ESG Analysis Report
The final report is generated in English and includes a structured interpretation of the selected company’s ESG performance.

The full report may contain the following sections:
- **Abstract**
- **Company and Industry Overview**
- **Data Source and Methodology**
- **Long-term ESG Performance Trend Analysis**
- **E/S/G Three-Dimensional Deep Dive**
- **Industry Benchmarking and Peer Comparison**
- **ESG Risk and Opportunity Assessment**
- **Conclusion and Targeted Recommendations**

This allows the agent to move beyond simple lookup and provide a richer, more interpretable analytical product.

---

## Demonstration Case from Final Program Output

### Data Source & Cleaning Report
- **Total rows of raw data:** 52,453
- **Total columns of raw data:** 15
- **Data Source:** Huazheng Index ESG Annual Rating Database (2009–2024)
- **Total valid rows after full cleaning:** 52,452
- **Number of invalid rows removed:** 1
- **Number of covered listed companies:** 5,461
- **Number of covered industries:** 338

### Target Company Confirmation
- **Company Name:** 蓝色光标
- **Stock Code:** 300058
- **Industry:** 营销代理
- **Peer Companies:** 省广集团, 易点天下, 三人行

### Key Findings from the Final ESG Report
Based on the final Python output for 蓝色光标 (Stock Code: 300058):

- As of 2024, the company achieved an **overall ESG score of 82.01**
- It ranked in the **top 8.0 percentile** of the 营销代理 industry
- Its ESG score increased from **66.86 (2009)** to **82.01 (2024)**
- The cumulative ESG score growth was **22.66%**
- The **Social (S)** dimension was identified as the company’s core strength
- The **Environmental (E)** dimension was identified as the key weakness and improvement area

### 2024 Peer Benchmark Snapshot
| Company | ESG Total Score | E Score | S Score | G Score |
|---|---:|---:|---:|---:|
| 蓝色光标 | 82.01 | 74.00 | 81.23 | 80.92 |
| 省广集团 | 81.44 | 64.67 | 83.91 | 79.47 |
| 易点天下 | 82.46 | 63.43 | 82.53 | 83.50 |
| 三人行 | 82.45 | 64.67 | 81.78 | 82.15 |

---

## Visualizations

### Figure 1. ESG Trend and Industry Benchmark
![ESG Trend and Industry Benchmark](figures/esg_trend_industry_benchmark.png)

### Figure 2. E/S/G Three-Dimension Trend
![E/S/G Three-Dimension Trend](figures/esg_3dimension_trend.png)

### Figure 3. Peer Company Benchmark
![Peer Company Benchmark](figures/esg_peer_benchmark.png)

### Figure 4. ESG Radar Chart
![ESG Radar Chart](figures/esg_radar_chart.png)

---

## Python Workflow
This project is supported by a substantive Python workflow. The workflow includes:

1. loading ESG data
2. cleaning invalid, duplicated, or unusable records
3. selecting the target company based on stock code
4. confirming industry classification and peer companies
5. calculating multi-year ESG trends
6. comparing the company with industry benchmarks
7. analyzing E/S/G dimension performance
8. generating tables, charts, and structured report content
9. producing a full English ESG analysis report

This workflow follows a coherent analytical chain from **data input → cleaning → analysis → output**, which is expected in the notebook and code submission.

## Relationship Between the Agent and the Python Workflow
The relationship between the agent and the Python code is central to this project.

### Python is the analytical engine
Python performs the actual data analysis work, including:
- reading the Huazheng ESG dataset
- cleaning and validating the data
- filtering by stock code
- identifying the target company and peer firms
- conducting year-by-year trend analysis
- benchmarking the company against the industry
- generating charts and analytical report components

Without the Python workflow, the final report would not have reliable data grounding.

### The agent is the interaction and delivery layer
The agent is responsible for:
- receiving the user’s stock code input
- triggering or following the Python-supported analysis logic
- presenting the result in a user-friendly way
- converting structured outputs into an interpretable ESG report

### Why this matters for Track 3
This project is designed for Track 3, where the product must **not rely only on model responses**. The Python analysis must be substantive, and this project follows that requirement by making Python the core source of evidence, logic, and report content.

In short:
- **Python produces the analysis**
- **the agent delivers the analysis**
- **the final report is grounded in actual data processing rather than generic text generation**

## Why This Project Is Business-Related
This project is business-related because ESG information is increasingly used in:
- investment decisions
- company evaluation
- sustainability benchmarking
- industry comparison
- strategic management and disclosure improvement

The output is valuable to real users because it turns raw data into decision-support information.

## Repository Contents
This repository may include:
- `README.md` – project description
- Python code file(s) – main analysis program
- notebook file – analytical workflow and outputs
- dataset file or data documentation
- workflow evidence – screenshots or exported workflow files
- demo video – 1–3 minute demonstration of the product

## Limitations
- The analysis depends on the quality and coverage of the source dataset.
- ESG ratings and scores reflect the methodology of the original data provider.
- Some company names or industry names may follow the original Chinese dataset labels.
- The project provides data-supported analysis rather than professional investment advice.

## Future Improvements
Possible future improvements include:
- adding more flexible user queries
- allowing comparison across multiple companies simultaneously
- generating downloadable report files
- adding more visualizations and interactive dashboards
- integrating more detailed ESG sub-dimensions if data is available

## Links
- **Coze/Dify Agent Link:** [Insert link here]
- **Workflow Evidence:** [Insert screenshots or workflow export link here]

## Submission Notes
- All assessed materials should be in English.
- The notebook should show a coherent workflow from data loading to final output.
- The reflection report must include AI disclosure at the end, including tool name, model/version, access date, and purpose of use.
