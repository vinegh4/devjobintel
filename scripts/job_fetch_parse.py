#!/opt/homebrew/bin/python3
import requests
from openai import OpenAI
import os
from dotenv import load_dotenv

def parse_job_posting(url):
    try:
        # Fetch HTML content from the provided URL
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch URL: {url}")

        html_content = response.text

        prompt = """
        I want you to help me parse job openings for into structured data. 
        I am going to provide you with the text for a job posting, I want you to return a json formatted response with the following format. If any of the described fields cannot be populated, simply leave them empty. Do not try to infer information that is not present. Do not hallucinate. Do not reply with any material other than the structured json data. In the below formatting description, text starting with "//" is a comment to improve you understand of how the format works. Read and understand these comments, but do not replicate them in the output. 

        Job Title: 
        Company:
        Job URL:
        Country:
        Location: //City, State, Country or analogous format. provide to the level of specificity possible. If the job lists the word "remote" in the location details, truncate this"
        In office/hybrid/remote: //If job specifies fully in office or does not mention hybrid or remote work possible, specify "in-office". If job mentions partial time in office, or is remote but requires employees to be within commute distance of office, specify "hybrid". If job mentions remote, without caveats (other than country of residence, specify "remote".
        Industry: //don't try to infer this from the job description, solely base this off of the company
        Minimum years of experience: //this is a minimum and should only be sourced from a requirements portion of a job add
        Maximum salary: 
        Hard skills: //these are skills with specific tools, programming languages, products, frameworks, libraries, etc. eg. Python, Java, AWS, PostgreSQL. May be sourced from requirements and desired skills
        Subject Matter Areas: //these are broad areas of expertise, but not specific tools or technologies. Eg. back end development, machine learning, large language models, distributed systems, embedded systems, may be sourced from requirements and desired skills
        Education requirements: //ignore subject areas, just specify bachelor's, master's, or phd if any are required. Only use what is required, not desired. 
        Individual contributor or manager: //if management of teams isn't specifically discussed as part of the role, mark "individual contributor"
        """

        load_dotenv()

        # Replace with your GPT-3.5 API credentials or endpoint
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY")
        )
        completion = client.chat.completions.create(
            model = "gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content":html_content}
            ]
        )
        print(completion.choices[0].message)

        return 0

    except Exception as e:
        return {"error": str(e)}

# Example usage:
url = "https://jobs.netflix.com/jobs/333869973"
parsed_data = parse_job_posting(url)
print(parsed_data)


