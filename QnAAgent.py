from langchain_ollama import OllamaLLM
from typing import List, Dict
import requests
import fitz 

qa_model = OllamaLLM(model="llama3.1")

class QnAAgent:
    def __init__(self, papers: List[Dict]):
        self.papers = papers

    def download_and_extract_text(self, url: str) -> str:
        """
        Downloads the PDF from the given URL and extracts text.
        
        Args:
            url (str): The URL of the PDF to download.

        Returns:
            str: The extracted text content of the PDF.
        """
        response = requests.get(url)
        response.raise_for_status()
        
        with open("temp_paper.pdf", "wb") as file:
            file.write(response.content)
        
        with fitz.open("temp_paper.pdf") as pdf_doc:
            text = ""
            for page in pdf_doc:
                text += page.get_text()
        
        return text

    def answer_text_question(self, question: str, paper_index: int) -> str:
        paper = self.papers[paper_index]
        context = f"Title: {paper['title']}\nSummary: {paper['summary']}\n"
        
        if "url" in paper and paper["url"].endswith(".pdf"):
            full_text = self.download_and_extract_text(paper["url"])
            context += f"\nContent:\n{full_text[:2000]}"

        input_prompt = f"{context}\n\nQuestion: {question}\nAnswer:"
        answer = qa_model.invoke(input=input_prompt)
        return answer


    def handle_image_question(self, question: str, paper_index: int) -> str:
        """
        Provides an answer placeholder for image-related questions.

        Args:
            question (str): The question to answer.
            paper_index (int): The index of the paper in the list to reference.

        Returns:
            str: Placeholder answer for visual content questions.
        """
        paper = self.papers[paper_index]
        input_prompt = (
            f"Title: {paper['title']}\nSummary: {paper['summary']}\n\n"
            f"Question: {question}\n"
            "Answer with details if this paper contains images, charts, or figures relevant to the question."
        )

        # need to use the llama3.2 vision model model for an answer related to visual content
        answer = qa_model.invoke(input=input_prompt)
        return answer

    def answer_question(self, question: str, paper_index: int) -> str:
        """
        Determines whether a question is text or image-based and provides an answer.

        Args:
            question (str): The question to answer.
            paper_index (int): The index of the paper in the list to reference.

        Returns:
            str: The answer to the question.
        """
        if any(keyword in question.lower() for keyword in ["image", "chart", "graph", "figure"]):
            return self.handle_image_question(question, paper_index)
        else:
            return self.answer_text_question(question, paper_index)