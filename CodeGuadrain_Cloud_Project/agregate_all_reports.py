# from langchain_anthropic import ChatAnthropic
# from langchain_core.prompts import ChatPromptTemplate
# from typing import List
# from dotenv import load_dotenv
# import os


# from send_email import send_email
# from gemini_request import get_gemini_response






# gemini_api_key = "AIzaSyBDXBP5jTIUChRxX-urREJ2e1pKBzc7Fn8"



# load_dotenv("url/.env")
# api_claude = os.getenv('LLM_TOKEN')
# api_gemini = os.getenv('GEMINI_API_KEY')

# # print(api_claude)

# def init_claude():
#     return ChatAnthropic(
#         model_name="claude-3-haiku-20240307",
#         temperature=0,
#         api_key=str(api_claude)
#     )

# def get_final_report(directory_structure: str = "", email: str = "") -> str:
#     """
#     Generate a comprehensive security report from individual vulnerability reports.
    
#     Args:
#         directory_structure (str): String representation of the repository structure
    
#     Returns:
#         str: The generated security report in markdown format
#     """
#     Claude_haiku_model = init_claude()
    
#     # Read the individual reports
#     try:
#         with open('document.md', 'r', encoding='utf-8') as file:
#             small_reports = file.read()
#     except FileNotFoundError:
#         raise FileNotFoundError("document.md not found. Please ensure the file exists.")

#     final_report_template = """You're a cybersecurity expert synthesizing multiple code vulnerability reports into a comprehensive summary. Given individual reports for each file from a GitHub repo {small_reports} and the repo's directory structure {directory_structure}, create a concise yet thorough aggregated report highlighting critical issues and providing an overall security assessment.

# Include:
# 1. Executive Summary:
#    - Overall risk assessment (High/medium/low)
#    - Most critical vulnerabilities summary
#    - Patterns or recurring issues

# 2. Key Findings:
#    - Top 5 most severe vulnerabilities across all files
#    - For each: title, affected file(s), severity, brief impact

# 3. Vulnerability Statistics:
#    - Total vulnerabilities
#    - Breakdown by severity

# 4. Detailed Vulnerability Analysis:
#    - For each unique vulnerability type:
#      - Description, affected files, potential impact

# 5. Recommendations:
#    - Prioritized actions for critical issues
#    - Overall security improvements

# 6. Remediations:
#    - Required fixes for vulnerabilities

# Use markdown for formatting. Analyze reports, identify patterns, and create a cohesive narrative about the codebase's security state. Provide actionable insights and clear priorities."""

#     prompt = final_report_template.format(
#         directory_structure=directory_structure,
#         small_reports=small_reports
#     )
    
#     try:
#         # response = Claude_haiku_model.invoke(prompt)
#         response = get_gemini_response(prompt, api_gemini)
#         report_content = response

#         # Save the report to a file
#         with open('final_report.md', 'w', encoding='utf-8') as file:
#             file.write(report_content)
#         send_email(email)

#         return report_content
#     except Exception as e:
#         raise Exception(f"Error generating report: {str(e)}")

# def test_report_generation():
#     """
#     Test function to demonstrate the usage of the report generator
#     """
#     # Sample directory structure
#     sample_directory = """
#     /project
#     ├── src/
#     │   ├── main.py
#     │   └── utils.py
#     ├── tests/
#     │   └── test_main.py
#     └── README.md
#     """
    
#     # Create a sample document.md file
#     sample_report = """
#     # Security Analysis for main.py
#     - **Severity**: High
#     - **Issue**: Hardcoded credentials found
#     - **Location**: Line 45
#     - **Description**: API keys stored in plaintext
    
#     # Security Analysis for utils.py
#     - **Severity**: Medium
#     - **Issue**: Insufficient input validation
#     - **Location**: Line 23
#     - **Description**: Potential SQL injection vulnerability
#     """
    
#     with open('document.md', 'w', encoding='utf-8') as file:
#         file.write(sample_report)
    
#     try:
#         # Generate the report
#         final_report = get_final_report(sample_directory)
#         print("Report generated successfully!")
#         print("\nReport preview:")
#         print(final_report[:500] + "...")  # Print first 500 characters
#     except Exception as e:
#         print(f"Error: {str(e)}")
#     finally:
#         # Clean up test file
#         if os.path.exists('document.md'):
#             os.remove('document.md')

# # if __name__ == "__main__":
# #     test_report_generation()


# HORCRUX/CodeGuadrain_Cloud_Project/agregate_all_reports.py
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from typing import List
from dotenv import load_dotenv
import os

from send_email import send_email
from gemini_request import get_gemini_response



load_dotenv("url/.env")
api_claude = os.getenv('LLM_TOKEN')
api_gemini = os.getenv('GEMINI_API_KEY')

def init_claude():
    return ChatAnthropic(
        model_name="claude-3-haiku-20240307",
        temperature=0,
        api_key=str(api_claude)
    )

def get_final_report(individual_reports: List[dict], directory_structure: str = "", email: str = "") -> str:
    """
    Generate a comprehensive security report from individual vulnerability reports.
    
    Args:
        individual_reports (List[dict]): List of dictionaries containing individual vulnerability reports
        directory_structure (str): String representation of the repository structure
    
    Returns:
        str: The generated security report in markdown format
    """
    Claude_haiku_model = init_claude()
    
    # Concatenate individual reports
    small_reports = "\n".join([report["content"] for report in individual_reports])

    final_report_template = """You're a cybersecurity expert synthesizing multiple code vulnerability reports into a comprehensive summary. Given individual reports for each file from a GitHub repo {small_reports} and the repo's directory structure {directory_structure}, create a concise yet thorough aggregated report highlighting critical issues and providing an overall security assessment.
Include:
1. Executive Summary:
   - Overall risk assessment (High/medium/low)
   - Most critical vulnerabilities summary
   - Patterns or recurring issues

2. Key Findings: ( just give in text format and not a table) 
   - Top 5 most severe vulnerabilities across all files
   - For each: title, affected file(s), severity, brief impact

3. Vulnerability Statistics:
   - Total vulnerabilities
   - Breakdown by severity

4. Detailed Vulnerability Analysis:
   - For each unique vulnerability type:
     - Description, affected files, potential impact

5. Recommendations:
   - Prioritized actions for critical issues
   - Overall security improvements

6. Remediations: (Required)
   - Required fixes for vulnerabilities

Use markdown for formatting. Analyze reports, identify patterns, and create a cohesive narrative about the codebase's security state. Provide actionable insights and clear priorities. Dont give any tables in response. """

    prompt = final_report_template.format(
        directory_structure=directory_structure,
        small_reports=small_reports
    )
    
    try:
        response = get_gemini_response(prompt, api_gemini)
        report_content = response

        send_email(report_content, email)

        return report_content
    except Exception as e:
        raise Exception(f"Error generating report: {str(e)}")
