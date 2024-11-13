from typing import List, Dict
from langchain_ollama import OllamaLLM

# Initialize the LLM with the Ollama model "llama3.1"
future_model = OllamaLLM(model="llama3.1")

class FutureWorksAgent:
    def __init__(self, papers: List[Dict]):
        """
        Initializes the FutureWorksAgent with a list of papers.

        Args:
            papers (List[Dict]): List of dictionaries containing paper details.
        """
        self.papers = papers

    def generate_future_work(self, paper_index: int) -> str:
        """
        Generates future work suggestions for a given paper using a fixed prompt.

        Args:
            paper_index (int): Index of the paper in the list to use for future work generation.

        Returns:
            str: Suggested future work directions.
        """
        paper = self.papers[paper_index]
        prompt = (
            f"Title: {paper['title']}\n"
            f"Summary: {paper['summary']}\n\n"
            "Based on the above summary, suggest potential improvements, unexplored areas, "
            "and future research directions."
        )

        # Get future research suggestions from the llama3.1 model
        future_work_suggestions = future_model.invoke(input=prompt)
        return future_work_suggestions

    def create_review_paper(self) -> str:
        """
        Compiles a review paper based on the stored summaries and future work suggestions.

        Returns:
            str: Generated review paper content.
        """
        review_content = "Review Paper: Future Directions in Research\n\n"

        for i, paper in enumerate(self.papers):
            review_content += (
                f"### {i + 1}. {paper['title']}\n"
                f"**Authors**: {paper['authors']}\n"
                f"**Published Date**: {paper['published_date']}\n"
                f"**Summary**: {paper['summary']}\n\n"
            )

            future_directions = self.generate_future_work(i)
            review_content += f"**Future Work Suggestions**:\n{future_directions}\n\n"

        return review_content
