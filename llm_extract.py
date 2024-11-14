
import os
from openai import OpenAI


def get_llm_client():
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def extract_invoice(client, base64_image):
    system_prompt = f"""
You are an OCR-like data extraction tool that extracts data from PDFs.
1. Please extract the data according to theme/sub groups, and then output into JSON.
2. Please keep the keys and values of the JSON in the original language. 
3. If there are blank data fields in the file, please include them as "null" values in the JSON object.
4. If there are tables in the file, capture all of the rows and columns in the JSON object. 
    Even if a column is blank, include it as a key in the JSON object with a null value.
5. If a row is blank denote missing fields with "null" values. 
6. Don't interpolate or make up data.
7. Please maintain the table structure of the charges, i.e. capture all of the rows and columns in the JSON object."""
    
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={ "type": "json_object" },
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "extract the data in this file and output into JSON "},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}", "detail": "high"}}
                ]
            }
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content



def extract_normal_doc(client, base64_image):
    system_prompt =  f"""
    Extract the main body text from {page_range} of the provided PDF file. Exclude cover pages, title pages, 
    table of contents, appendices, indexes, headers, footers, bookmarks, annotations, images, tables, footnotes, 
    and any other non-body text elements, include titles and subtitles if exist.
    Format the extracted text as Markdown, following these guidelines:
    1. Use appropriate heading levels (#, ##, ###, etc.) to represent the document's structure.
    2. Maintain paragraph separations from the original text.
    3. Use Markdown list formatting (ordered or unordered) for any lists encountered.
    4. Preserve important emphasis such as bold or italics (if present in the original).
    5. Use Markdown quote formatting for any quotations.
    If you've finished extracting all the requested text, end your response with the phrase 'Gemini Work Done' 
    on a new line. If you haven't finished, simply stop at a natural breakpoint, and I will prompt you to continue.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={ "type": "json_object" },
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "extract the data in this hotel invoice and output into JSON "},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}", "detail": "high"}}
                ]
            }
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content