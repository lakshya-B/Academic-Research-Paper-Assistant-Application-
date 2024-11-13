import arxiv
from datetime import datetime, timedelta
from typing import List, Dict
from DatabaseAgent import Neo4jDatabase

def search_papers(topic: str, max_results: int = 500) -> List[Dict]:
    """
    Searches for research papers on Arxiv related to a given topic, subdividing by year if necessary.

    Args:
        topic (str): The research topic to search for.
        max_results (int): Maximum number of papers to fetch.

    Returns:
        List[Dict]: A list of dictionaries containing paper details.
    """
    # Define the years to search across
    start_year = 2019
    end_year = datetime.now().year
    client = arxiv.Client()
    papers = []
    paper_ids = set()  

    for year in range(start_year, end_year + 1):
        search_query = f"{topic} AND submittedDate:[{year}0101 TO {year}1231]"
        batch_size = 100  

        print(f"Searching for papers in the year {year}...")

        while len(papers) < max_results:
            try:
                search = arxiv.Search(
                    query=search_query,
                    max_results=batch_size,
                    sort_by=arxiv.SortCriterion.SubmittedDate
                )

                results = list(client.results(search))
                if not results:
                    print(f"No more results available from Arxiv for the year {year}.")
                    break  

                new_papers_found = False

                for result in results:
                    if result.entry_id in paper_ids:
                        continue

                    paper_info = {
                        "title": result.title,
                        "authors": [author.name for author in result.authors],
                        "published_date": result.published,
                        "summary": result.summary,
                        "url": result.entry_id,
                        "links": [link.href for link in result.links if link.href != result.entry_id]
                    }
                    papers.append(paper_info)
                    paper_ids.add(paper_info["url"])  
                    new_papers_found = True

                    if len(papers) >= max_results:
                        break

                if not new_papers_found:
                    print(f"No new unique papers found in the last batch for the year {year}.")
                    break  

            except Exception as e:
                print(f"Error fetching results: {e}")
                break

    print(f"Fetched {len(papers)} unique papers on topic '{topic}'.")
    return papers, list(paper_ids)

def store_papers_in_database(papers: List[Dict], db: Neo4jDatabase):
    """
    Stores all retrieved papers in the Neo4j database.

    Args:
        papers (List[Dict]): List of paper details.
        db (Neo4jDatabase): Neo4j database instance.
    """
    for paper in papers:
        db.store_paper(paper)
    print(f"Stored {len(papers)} papers in the database.")