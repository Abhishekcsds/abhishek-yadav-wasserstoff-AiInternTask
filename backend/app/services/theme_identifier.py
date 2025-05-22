


# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
# from langchain_groq.chat_models import ChatGroq
# from app.core.config import settings
# from typing import List
# import re
# # other existing imports...


# # Initialize Groq LLM with API key
# llm = ChatGroq(
#     api_key=settings.GROQ_API_KEY,
#     model="llama3-8b-8192",
#     temperature=0  # for deterministic output
# )

# # Prompt for theme extraction
# prompt = PromptTemplate(
#     input_variables=["text"],
#     template="""
# You are a helpful assistant skilled at reading and analyzing academic and technical texts. 
# Given the following input, extract **5 to 10** key themes or topics discussed. Then, provide a concise summary in 2-3 lines.

# Text:
# {text}

# Respond in the following format:

# Themes: Theme1, Theme2, Theme3, ..., Theme10  
# Summary: <brief summary here>
# """
# )

# # Chain setup
# theme_chain = LLMChain(llm=llm, prompt=prompt)




# def identify_themes(text: str = None) -> dict:
#     if not text:
#         return {
#             "themes": [],
#             "synthesizedAnswer": "No input provided.",
#             "error": None
#         }

#     try:
#         chunks = chunk_text(text, max_chars=5000)[:2]  # Limit to first 1–2 chunks

#         all_themes = []
#         summaries = []

#         for chunk in chunks:
#             result = theme_chain.run(chunk)

#             themes_match = re.search(r"(?i)themes:\s*(.+?)\n", result)
#             summary_match = re.search(r"(?i)summary:\s*(.+)", result)

#             if themes_match:
#                 themes = [t.strip() for t in themes_match.group(1).split(",") if t.strip()]
#                 all_themes.extend(themes)

#             if summary_match:
#                 summaries.append(summary_match.group(1).strip())

#         final_themes = list(dict.fromkeys(all_themes))[:10]
#         final_summary = " ".join(summaries)[:400] or "No summary found."

#         return {
#             "themes": final_themes,
#             "synthesizedAnswer": final_summary,
#             "error": None
#         }

#     except Exception as e:
#         return {
#             "themes": [],
#             "synthesizedAnswer": "",
#             "error": str(e)
#         }

#     except Exception as e:
#         print(f"[ERROR] Theme Identification Failed: {e}")
#         return {
#             "themes": [],
#             "synthesizedAnswer": "",
#             "error": str(e)
#         }



# from typing import List

# def chunk_text(text: str, max_chars: int = 3000) -> List[str]:
#     """
#     Splits large text into chunks of max_chars size.
#     Keeps chunks roughly by paragraph or sentence if possible.
#     """
#     import re
    
#     paragraphs = re.split(r'\n{2,}', text)
#     chunks = []
#     current_chunk = ""

#     for para in paragraphs:
#         if len(current_chunk) + len(para) + 2 <= max_chars:
#             current_chunk += para + "\n\n"
#         else:
#             if current_chunk:
#                 chunks.append(current_chunk.strip())
#             if len(para) > max_chars:
#                 # Split very long paragraphs further by sentences
#                 sentences = re.split(r'(?<=[.!?]) +', para)
#                 temp_chunk = ""
#                 for sent in sentences:
#                     if len(temp_chunk) + len(sent) + 1 <= max_chars:
#                         temp_chunk += sent + " "
#                     else:
#                         chunks.append(temp_chunk.strip())
#                         temp_chunk = sent + " "
#                 if temp_chunk:
#                     chunks.append(temp_chunk.strip())
#                 current_chunk = ""
#             else:
#                 current_chunk = para + "\n\n"

#     if current_chunk:
#         chunks.append(current_chunk.strip())

#     return chunks




from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq.chat_models import ChatGroq
from app.core.config import settings
from typing import List
import re

# Initialize the Groq LLM client with the API key from config
llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model="llama3-8b-8192",
    temperature=0  # fixed output for consistency
)

# Define the prompt template used to extract themes and provide a summary
prompt = PromptTemplate(
    input_variables=["text"],
    template="""
You are an expert assistant specialized in analyzing scholarly and technical documents.
Given the following text, identify **between 5 and 10** key themes or topics that are covered.
Then, summarize the content briefly in 2-3 sentences.

Text:
{text}

Please respond in this exact format:

Themes: Theme1, Theme2, Theme3, ..., Theme10  
Summary: <short summary here>
"""
)

# Set up the LLM chain combining the prompt and the model
theme_chain = LLMChain(llm=llm, prompt=prompt)

def identify_themes(text: str = None) -> dict:
    """
    Analyze the given text to extract key themes and a synthesized summary.
    Processes up to first 2 chunks of 5000 characters each for performance.

    Args:
        text (str): The input text to analyze.

    Returns:
        dict: Contains 'themes' (list of extracted themes),
              'synthesizedAnswer' (summary string),
              and 'error' (if any occurred).
    """
    if not text:
        return {
            "themes": [],
            "synthesizedAnswer": "No input provided.",
            "error": None
        }

    try:
        # Break text into chunks limited to 5000 characters (max 2 chunks)
        chunks = chunk_text(text, max_chars=5000)[:2]

        collected_themes = []
        collected_summaries = []

        # Process each chunk with the LLM chain
        for chunk in chunks:
            response = theme_chain.run(chunk)

            # Extract themes line from LLM output using regex
            themes_match = re.search(r"(?i)themes:\s*(.+?)\n", response)
            # Extract summary line similarly
            summary_match = re.search(r"(?i)summary:\s*(.+)", response)

            if themes_match:
                themes_list = [t.strip() for t in themes_match.group(1).split(",") if t.strip()]
                collected_themes.extend(themes_list)

            if summary_match:
                collected_summaries.append(summary_match.group(1).strip())

        # Remove duplicates, limit to 10 themes max
        unique_themes = list(dict.fromkeys(collected_themes))[:10]
        combined_summary = " ".join(collected_summaries)[:400] or "No summary found."

        return {
            "themes": unique_themes,
            "synthesizedAnswer": combined_summary,
            "error": None
        }

    except Exception as exc:
        return {
            "themes": [],
            "synthesizedAnswer": "",
            "error": str(exc)
        }


def chunk_text(text: str, max_chars: int = 3000) -> List[str]:
    """
    Split large input text into smaller chunks of approximately max_chars length.
    Attempts to split by paragraphs and then sentences to keep chunks coherent.

    Args:
        text (str): The large text to be split.
        max_chars (int): Maximum characters per chunk.

    Returns:
        List[str]: List of text chunks.
    """
    import re

    # Split by paragraphs separated by two or more newlines
    paragraphs = re.split(r'\n{2,}', text)
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        # Check if paragraph fits into current chunk within max_chars
        if len(current_chunk) + len(para) + 2 <= max_chars:
            current_chunk += para + "\n\n"
        else:
            # Save existing chunk if not empty
            if current_chunk:
                chunks.append(current_chunk.strip())

            # If paragraph is longer than max_chars, split further by sentences
            if len(para) > max_chars:
                sentences = re.split(r'(?<=[.!?]) +', para)
                temp_chunk = ""
                for sent in sentences:
                    if len(temp_chunk) + len(sent) + 1 <= max_chars:
                        temp_chunk += sent + " "
                    else:
                        chunks.append(temp_chunk.strip())
                        temp_chunk = sent + " "
                if temp_chunk:
                    chunks.append(temp_chunk.strip())
                current_chunk = ""
            else:
                # Paragraph fits alone in a chunk
                current_chunk = para + "\n\n"

    # Append the final chunk if exists
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
