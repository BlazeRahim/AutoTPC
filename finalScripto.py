import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from openai import OpenAI
import re

load_dotenv()
client = OpenAI()

def getPdfText(pdfs):
    text = ""
    for i in pdfs:
        pdf_reader = PdfReader(i)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def bold_subheadings(content):
    # List of subheadings to bold
    subheadings = ['NOTICE FOR XYZ PLACEMENT DRIVE FOR BATCH XXXX', 'Eligibility:','Branches:', 'Job Role:',
                   'Job Location:', 'CTC:', 'Bond:', 'Job Responsibilities:', 'Required Skills:', 'Selection Process:',
                   'Registration Link:', 'Confirmation Link:', 'Note:', 'Company Link:']
    content = re.sub(re.escape('NOTICE FOR XYZ PLACEMENT DRIVE FOR BATCH XXXX'),
                     '*NOTICE FOR XYZ PLACEMENT DRIVE FOR BATCH*', content)

    for subheading in subheadings:
        content = content.replace(subheading, f'*{subheading}*')

    return content


def main():
    st.set_page_config(page_title="AutoTPC", page_icon=":books:")

    st.header("Input your pdfs")

    st.subheader("Your pdfs")
    pdfs = st.file_uploader("Upload Your Raw(s) and click on Generate", accept_multiple_files=True)
    if st.button("Generate"):
        with st.spinner("Processing"):
            raw = getPdfText(pdfs)
            if raw:
                completion = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": f"""My raw:
                {raw}

                My Template:
                NOTICE FOR XYZ PLACEMENT DRIVE FOR BATCH XXXX 

                This message is to inform students regarding XYZ placement drive.
                (Company Info). 

                Company link: 

                Branches: (If nothing is given: All) 

                Eligibility:
                • 10th & 12th/Diploma: 
                • BE CGPA: 

                Job Role: 

                Job Location: 

                CTC: 

                Bond: 

                Job Responsibilities: 

                Required Skills: 

                Selection Process: 

                Registration Link: 

                Confirmation Link:

                Note:
                • Deadline for registration is 11th October, 2021 i.e today by 5:00 pm.
                • (If confirmation link is present)
                It is mandatory to fill both the links.

                Regards,
                TPC-RAIT

                Generate a notice for a placement drive based on the given company placement information (raw data) 
                for the specified batch. Ensure that the notice includes key details such as eligibility criteria, 
                job role, location, CTC, selection process, and registration link. Keep the notice concise and 
                structured according to the provided template. Avoid using unnecessary salutations (e.g., 
                "dear students"). For branches, use abbreviations like CS, IT, Extc separated by ',' and if branches 
                are not given, use "All." Do not use dashes in the notice. For eligibility, use base numbers (e.g., 
                6 instead of 6.00/10.00). If specific details are not provided in the raw data (e.g., bond, 
                job responsibilities, required skills), remove the respective subheadings. CTC must be in the format 
                of a number followed by LPA. If CS is given in branches, add CSBS automatically. Use the format for 
                the first line from the template. The BE CGPA must be a whole number between 5 and 10. Print Batch 
                2024 rather than 2024 Batch.

                Additional Instructions:

                Specify that the registration and confirmation links should follow a specific format, e.g., 
                enclosed in angle brackets (< >). Emphasize the importance of strictly adhering to the provided 
                template and structure. Clarify that deviations from the specified format will not be accepted. 
                Reiterate consistent naming conventions, such as using "CTC" for Compensation to Company. Confirm 
                that if branch information is not provided, the notice should use "All" for branches. If batch 
                information is provided then keep display it seperated by commas Specify whether CSBS should be 
                included automatically if CS is given. XYZ must be replaced by the company name given in the raw. For 
                job location just keep the Location given in the raw, and if there are multiple job locations 
                separate it by ','. Remove not specified things, except Registration Link:  and Confirmation Link:. 
                Strictly follow the template."""}
                    ]
                )
                if completion.choices and len(completion.choices) > 0:
                    st.subheader("Generated Notice:")
                    # Bold out subheadings before displaying
                    generated_notice = bold_subheadings(completion.choices[0].message.content)
                    # Use st.text_area to make the text copyable
                    st.text_area(label="", value=generated_notice, height=300)
                else:
                    st.warning("No response from the model.")
            else:
                st.warning("No text extracted from PDFs.")

if __name__ == "__main__":
    main()
