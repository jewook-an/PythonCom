from langchain_community.document_loaders import ArxivLoader

# Arxiv IDs
ids = ["2403.05313", "2403.04121", "2402.15809"]

# Load papers
docs = []
for paper_id in ids:
    doc = ArxivLoader(query=paper_id, load_max_docs=1).load()
    docs.extend(doc)