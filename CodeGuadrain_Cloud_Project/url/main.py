



# HORCRUX/CodeGuadrain_Cloud_Project/url/main.py
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from .hackathon import get_local_file_and_content, get_github_file_and_content
import os
from dotenv import load_dotenv
from on_device_requests import get_response_on_device
from aggregate import aggregate, delete_results
from url.helper import determine_severity
import json
from gemini_request import get_gemini_response




load_dotenv("url/.env")
api_claude = os.getenv('LLM_TOKEN')
api_gemini = os.getenv('GEMINI_API_KEY')



template = """Analyze this code for vulnerabilities:
{code}

Respond in following format only:
a. Executive Summary
•	Overall risk assessment (High/Medium/Low)
•	Key findings summary
b. Vulnerability Details (for each vulnerability)
•	Title: Clear, descriptive title of the vulnerabilities
•	Summary: Brief description of the issue
•	Severity: Using a standard scoring system like CVSS (necessary field)
•	Impact: Potential consequences of the vulnerability
•	Recommendations: Suggested fixes or mitigations (not the code)
•	References: Links to relevant CWEs/CVEs (mention web links), or best practices
"""

import time

def analyze_code_with_claude(file_path, content):
    print(f"Analyzing file: {file_path}")
    prompt = template.format(code=content)
    # print("prompt", prompt)
    start_time = time.time()
    response=""""""
    
    while time.time() - start_time < 6:  # Wait for at least 6 seconds
        response = get_response_on_device(prompt)
        # response = get_gemini_response(prompt,api_gemini)

        
        print("response", response)
        if response:
            print(f"Received response from deployed model for {file_path}")
            break
        else:
            print(f"Waiting for response from the deployed model for {file_path}...")
            time.sleep(1)  # Wait for 1 second before checking again
    
    if response:
            print(f"Response received for {file_path}: {response}")
            # Format response for frontend
            return {
                'file': file_path,
                'content': response.strip(),  # Remove extra whitespace
                'severity': determine_severity(response)  # You'll need to implement this
            }
    else:
            print(f"No response received from the deployed model for {file_path} after 6 seconds.")
            return None
    




def main(input_path, mail_address):
    # delete_results()
    try:
        if input_path.startswith('http'):
            folder_structure, file_content_dict = get_github_file_and_content(input_path)
        else:
            folder_structure, file_content_dict = get_local_file_and_content(input_path)
        
        # print("file_content_dict", file_content_dict)

        individual_reports = []
        for file_path, content in file_content_dict.items():
            # print("Analyzing individual file:", file_path)
            report = analyze_code_with_claude(file_path, content)
            if report:
                individual_reports.append(report)
                yield f"data: {json.dumps({'report': report})}\n\n"
        
        # print("individual_reports", individual_reports)
        if not individual_reports:
            print("No individual reports generated.")
        else:
            from agregate_all_reports import get_final_report
            final_report = get_final_report(individual_reports, folder_structure, mail_address)
            # print("final_report", final_report)
            yield f"data: {json.dumps({'completed': True, 'final_report': final_report})}\n\n"
        
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"
     