Wikipedia and DBpedia Ontology Parser

This project uses fuzzy matching to find the closest match for each term and loads the ontology if a match is found. Terms with over 85% similarity are saved separately, while terms not found at all are also listed in a separate file.

Features
Term normalization: Converts terms to lowercase and replaces spaces and hyphens with underscores for better matching.
Wikipedia search: Uses the Wikipedia API to search for terms and applies fuzzy matching to find the best match.
DBpedia ontology: Retrieves ontologies for found terms using SPARQL queries to DBpedia.
Reports:
Main ontology file: ontology_results.json.
File for similar terms (85%+ similarity): similar_terms.txt.
File for not found terms: not_found_terms.txt.


Run the parser:
python app.py

After the script finishes, the following files will be created:

ontology_results.json: Ontologies for found terms.
similar_terms.txt: Terms with more than 85% similarity to Wikipedia entries.
not_found_terms.txt: Terms not found in Wikipedia or DBpedia.