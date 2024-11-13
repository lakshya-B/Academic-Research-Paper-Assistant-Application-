from DatabaseAgent import Neo4jDatabase
from SearchAgent import search_papers, store_papers_in_database

neo4j_uri = "neo4j://localhost:7687" 
neo4j_user = "neo4j"  
neo4j_password = "password"  

topic = "Long-Context Large Language Models (LLMs)"
max_results = 10000 

db = Neo4jDatabase(neo4j_uri, neo4j_user, neo4j_password)

try:
    papers, paper_ids = search_papers(topic, max_results)
    store_papers_in_database(papers, db)
    print(f"Successfully stored {len(papers)} papers on the topic '{topic}' in the database.")
finally:

    db.close()
