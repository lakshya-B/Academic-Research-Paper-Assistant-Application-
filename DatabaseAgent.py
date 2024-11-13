from neo4j import GraphDatabase
from typing import List, Dict, Optional
import hashlib

class Neo4jDatabase:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def store_paper(self, paper_info: Dict):
        """
        Stores a single paper in the Neo4j database and assigns a unique paper_id property.
        
        Args:
            paper_info (Dict): Details of the paper to store.
        """
        paper_id = hashlib.md5(paper_info["url"].encode()).hexdigest()

        with self.driver.session() as session:
            session.write_transaction(self._store_paper_tx, paper_info, paper_id)

    @staticmethod
    def _store_paper_tx(tx, paper_info: Dict, paper_id: str):
        tx.run(
            """
            MERGE (p:Paper {paper_id: $paper_id})
            SET p.title = $title,
                p.authors = $authors,
                p.published_date = $published_date,
                p.summary = $summary,
                p.url = $url
            """,
            paper_id=paper_id,
            title=paper_info["title"],
            authors=paper_info["authors"],
            published_date=paper_info["published_date"].isoformat(),
            summary=paper_info["summary"],
            url=paper_info["url"]
        )

    def query_papers_by_year(self, year: int) -> List[Dict]:
        """
        Queries Neo4j for papers published in a specific year.

        Args:
            year (int): The publication year to filter.

        Returns:
            List[Dict]: A list of dictionaries containing matching paper details.
        """
        with self.driver.session() as session:
            result = session.execute_read(self._query_papers_by_year, year)
            print(f"Debug: Retrieved {len(result)} papers for year {year}")  # Debugging line
            return result

    @staticmethod
    def _query_papers_by_year(tx, year: int) -> List[Dict]:
        query = """
        MATCH (p:Paper)
        WHERE p.published_date STARTS WITH $year
        RETURN p.paper_id AS paper_id, p.title AS title, p.authors AS authors, p.published_date AS published_date,
            p.summary AS summary, p.url AS url
        """
        result = tx.run(query, year=str(year))

        papers = []
        for record in result:
            papers.append({
                "paper_id": record["paper_id"],
                "title": record["title"],
                "authors": record["authors"],
                "published_date": record["published_date"],
                "summary": record["summary"],
                "url": record["url"]
            })

        return papers
    
    def get_paper_by_id(self, paper_id: str) -> Optional[Dict]:
        """
        Retrieve a specific paper by its unique paper_id (string).
        
        Args:
            paper_id (str): The unique paper ID.
        
        Returns:
            Optional[Dict]: Paper details if found, otherwise None.
        """
        with self.driver.session() as session:
            result = session.execute_read(self._get_paper_by_id_tx, paper_id)
            return result

    @staticmethod
    def _get_paper_by_id_tx(tx, paper_id: str) -> Optional[Dict]:
        query = """
        MATCH (p:Paper {paper_id: $paper_id})
        RETURN p.title AS title, p.authors AS authors, p.published_date AS published_date,
            p.summary AS summary, p.url AS url
        """
        result = tx.run(query, paper_id=paper_id).single()
        if result:
            return {
                "title": result["title"],
                "authors": result["authors"],
                "published_date": result["published_date"],
                "summary": result["summary"],
                "url": result["url"]
            }
        return None


