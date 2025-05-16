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
    template="""
    Transcript: {transcript}
    You are an experienced Digital Marketing professor creating challenging graduate-level exam questions. Your goal is to assess students' deep understanding of concepts, analytical thinking, and practical application skills.

    OBJECTIVE:
    Generate 15 high-quality multiple choice questions that test different cognitive levels (knowledge, comprehension, application, analysis) based on the provided transcript. The questions should evaluate students' ability to:
    - Understand core digital marketing concepts and terminology
    - Apply frameworks to real-world scenarios
    - Analyze marketing strategies and their implications
    - Evaluate effectiveness of different approaches

    QUESTION GUIDELINES:
    1. Vary question types across:
    - Concept understanding
    - Case analysis
    - Practical application
    - Strategy evaluation
    - Metric interpretation
    - Best practice identification

    2. For each question:
    - Write a clear, concise stem
    - Include 4 plausible answer choices
    - Ensure only one definitively correct answer
    - Avoid obvious incorrect options
    - Use consistent formatting and length for options

    3. Distribution of difficulty:
    - 40% Basic understanding of concepts and terminology
    - 30% Intermediate application
    - 30% Advanced analysis

    FORMAT:
    Question #:
    [Question stem]
    A) [Option]
    B) [Option]
    C) [Option]
    D) [Option]

    After all questions, provide:
    1. Answer key with brief explanations
    2. Topic/concept tested for each question
    3. Difficulty level

    Transcript: {transcript}

    Begin Exam:
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
    
    logger.info("Sending request to LLM for exam question generation")
    response = llm.complete(formatted_prompt)
    
    logger.info("Successfully generated exam")
    return response.text
   

def save_exam(exam: str, output_file_path: str):
    logger.info(f"Saving exam to {output_file_path}")
    try:
        with open(output_file_path, "w") as f:
            f.write(exam)
        logger.info("exam saved successfully")
    except Exception as e:
        logger.error(f"Failed to save exam: {str(e)}")
        raise


def main(input_file_path: str):
    try:
        logger.info(f"Starting transcript summarization process for {input_file_path}")
        
        # Create output file path
        output_file_path = input_file_path.rsplit('.', 1)[0]
        # remove space
        output_file_path = output_file_path.replace(' ', '_')
        output_file_path = output_file_path + '_exam_practice.txt'
        
        # Generate exam
        exam = summarize_transcript(input_file_path)
        
        # Save exam
        save_exam(exam, output_file_path)
        
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
        print(f"exam saved to: {output_path}")
    except Exception as e:
        logger.error(f"Failed to process transcript: {str(e)}")
        sys.exit(1)


