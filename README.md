# Digital Marketing AI Notes Generator

An AI-powered study assistant for Digital Marketing MGT6311 OMSCS that automatically generates comprehensive lecture notes and practice exam questions from course transcripts.

## Features

- **Transcript Summarization**: Converts lecture transcripts into well-structured markdown notes
- **Exam Question Generation**: Creates practice exam questions with multiple-choice answers
- **Markdown Output**: Generates clean, formatted markdown files for easy reading
- **Practice Questions**: Produces exam-style questions with answer keys and explanations

## Project Structure

```
digital-marketing-ai-notes/
├── ai-notes/
│   ├── summarize-transcript.py    # Generates markdown notes from transcripts
│   └── exam-question-generation.py # Creates practice exam questions
├── video-transcript/             # Contains input transcript files
│   ├── *.docx                    # Original transcript files
│   ├── *.md                      # Generated markdown notes
│   └── *_exam_practice.txt       # Generated practice questions
└── requirements.txt              # Python dependencies
```

## Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the `ai-notes` directory with your Azure OpenAI credentials:
   ```
   AZURE_OPENAI_KEY=your_api_key
   OPENAI_API_VERSION=your_api_version
   AZURE_OPENAI_ENDPOINT=your_endpoint
   ```

## Usage

### Generate Lecture Notes
```bash
python ai-notes/summarize-transcript.py "path/to/transcript.docx"
```

### Generate Practice Questions
```bash
python ai-notes/exam-question-generation.py "path/to/transcript.docx"
```

## Output Files

- **Markdown Notes**: `[transcript_name].md`
  - Structured lecture notes with sections, key concepts, and takeaways
  - Formatted in markdown for easy reading and navigation

- **Practice Questions**: `[transcript_name]_exam_practice.txt`
  - 15 multiple-choice questions per transcript
  - Includes answer key and explanations
  - Covers various difficulty levels and topics

## Requirements

- Python 3.10+
- Azure OpenAI API access
- Required Python packages (see requirements.txt)

## Note

This tool is specifically designed for the Digital Marketing MGT6311 OMSCS course and generates content based on the course's curriculum and teaching style.
