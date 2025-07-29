import re, pdfplumber, fitz
import os
import logging
from app.utils.openai_interface import generate_commodity_prompt#
from openai import OpenAI

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the OpenAI API key from environment variables
api_key = os.getenv('openai_api_key')

if not api_key:
    logging.error("OpenAI API key is not defined in the environment variables")
    raise ValueError("OpenAI API key is not defined in the environment variables")

logging.info("OpenAI API key successfully loaded from environment variables")
client = OpenAI(api_key=api_key)

def parse_pdf(path: str) -> str:
    logging.info(f"Starting to parse PDF: {path}")

    # 1 extract raw text
    text = ""
    with pdfplumber.open(path) as pdf:
        text = "\n".join(p.extract_text() or "" for p in pdf.pages)
    #logging.info("Extracted text using pdfplumber: %s", text + "...")
    
    response = client.responses.create(
        model="gpt-3.5-turbo",
        input=generate_commodity_prompt(text),
        text={"format": {"type": "json_object"}},
    )

    logging.info("Extracted text using OpenAI API: %s", response.output_text)
    logging.info("Finished parsing PDF.")
    return response.output_text
