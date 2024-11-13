from typing import List, Dict
from langchain_ollama import OllamaLLM

summary_model = OllamaLLM(model="llama3.1")

class SummarizeFindings:
    def __init__(self, papers: List[Dict]):
        """
        Initializes the SummarizeFindingsAgent with a list of papers.

        Args:
            papers (List[Dict]): List of dictionaries containing paper details.
        """
        self.papers = papers

    def summarize_findings(self) -> str:
        """
        Summarizes the findings of all papers in a specific timeframe.

        Returns:
            str: A consolidated summary of the findings.
        """
        combined_summaries = "\n\n".join(paper["summary"] for paper in self.papers)

        prompt = (
            f"Summaries of papers published:\n\n{combined_summaries}\n\n"
            "Provide a high-level summary highlighting the main findings across these papers."
        )

        overall_summary = summary_model.invoke(input=prompt)
        return overall_summary

    def generate_future_works_from_year(self) -> str:
        """
        Generates future work suggestions for the year based on all paper summaries.

        Returns:
            str: Suggested future work directions for all papers in the specified year.
        """
        combined_summaries = "\n\n".join(paper["summary"] for paper in self.papers)

        prompt = (
            f"Summaries of papers published:\n\n{combined_summaries}\n\n"
            "Based on the above summaries, suggest potential improvements, unexplored areas, "
            "and future research directions across these studies."
        )
        
        future_work_suggestions = summary_model.invoke(input=prompt)
        return future_work_suggestions

    def extract_key_points(self) -> List[Dict[str, str]]:
        """
        Extracts key points or highlights from each paper.

        Returns:
            List[Dict[str, str]]: List of dictionaries containing paper title and key points.
        """
        key_points_list = []
        
        for paper in self.papers:
            prompt = (
                f"Title: {paper['title']}\n"
                f"Summary: {paper['summary']}\n\n"
                "Extract the key points or most important highlights from this paper."
            )
            
            key_points = summary_model.invoke(input=prompt)
            key_points_list.append({"title": paper["title"], "key_points": key_points})
        
        return key_points_list
