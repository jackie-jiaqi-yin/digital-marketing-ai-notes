import os
from dotenv import load_dotenv
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.core import PromptTemplate
import logging
import docx  # Add this import for handling .docx files

# Configure logging to output only to console with a specific format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # This ensures output only to console
    ]
)
logger = logging.getLogger(__name__)



SYSTEM_PROMPT = PromptTemplate(
    template="""You are an expert teaching assistant tasked with creating comprehensive lecture notes from course transcripts. It is graduate level course of "Digital Marketing".

OBJECTIVE:
Create detailed, well-structured lecture notes from the provided transcript that will help students understand and review the material effectively.

INSTRUCTIONS:
1. Content Organization:
   - Identify and separate major topics and subtopics
   - Maintain the logical flow of ideas
   - Use clear hierarchical structure

2. For Each Section:
   - Extract key concepts and definitions
   - Highlight important theories and frameworks
   - Note real-world examples and case studies if applicable
   - Identify any formulas, methods, or step-by-step processes
   - Capture essential quotes or statements from the professor

3. Format Requirements:
   - Use markdown formatting for clear hierarchy
   - Use bullet points for key points
   - Use numbered lists for sequential steps or processes
   - Include section headings and subheadings
   - Bold important terms and concepts
   - Use tables where appropriate for comparing concepts

4. Additional Elements:
   - Add a brief summary at the start of each major section
   - Include any mentioned references or resources
   - Note any assignments or important deadlines mentioned
   - Highlight key takeaways at the end of each section

OUTPUT FORMAT:
# [Lecture Title]

## Overview
[Brief summary of the entire lecture]

## [Section 1 Title]
### Key Concepts
- [Concept 1]
- [Concept 2]

### Detailed Notes
[Detailed content in structured format]

### Key Takeaways
- [Main point 1]
- [Main point 2]

[Continue for each section...]

Transcript: {transcript}

Summary: 
"""
)

load_dotenv('ai-notes/.env')
llm = AzureOpenAI(
        model='gpt-4o',
        engine='gpt-4o',
        api_key=os.getenv('AZURE_OPENAI_KEY'),
        api_version=os.getenv('OPENAI_API_VERSION'),
        azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
        temperature=0.7,
        retry=2,
        timeout=60
    )


def read_transcript_doc(file_path: str) -> str:
    """
    Read docx file and return the text
    """
    doc = docx.Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])


def summarize_transcript(transcript_file_path: str,
                         prompt: PromptTemplate = SYSTEM_PROMPT):
    logger.info(f"Reading transcript from {transcript_file_path}")
    transcript = read_transcript_doc(transcript_file_path)
    
    logger.info("Formatting prompt with transcript")
    formatted_prompt = prompt.format(transcript=transcript)
    
    logger.info("Sending request to LLM for summarization")
    response = llm.complete(formatted_prompt)
    
    logger.info("Successfully generated summary")
    return response.text
   

def save_summary(summary: str, output_file_path: str):
    logger.info(f"Saving summary to {output_file_path}")
    try:
        with open(output_file_path, "w") as f:
            f.write(summary)
        logger.info("Summary saved successfully")
    except Exception as e:
        logger.error(f"Failed to save summary: {str(e)}")
        raise


def main(input_file_path: str):
    try:
        logger.info(f"Starting transcript summarization process for {input_file_path}")
        
        # Create output file path
        output_file_path = input_file_path.rsplit('.', 1)[0]
        # remove space
        output_file_path = output_file_path.replace(' ', '_')
        output_file_path = output_file_path + '.md'
        
        # Generate summary
        summary = summarize_transcript(input_file_path)
        
        # Save summary
        save_summary(summary, output_file_path)
        
        logger.info(f"Successfully completed summarization. Output saved to {output_file_path}")
        return output_file_path
        
    except Exception as e:
        logger.error(f"An error occurred during summarization: {str(e)}")
        raise


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        logger.error("Please provide the path to the transcript file as an argument")
        sys.exit(1)
        
    try:
        output_path = main(sys.argv[1])
        print(f"Summary saved to: {output_path}")
    except Exception as e:
        logger.error(f"Failed to process transcript: {str(e)}")
        sys.exit(1)


