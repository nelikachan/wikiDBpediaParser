import requests
import json
from rapidfuzz import fuzz

WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"
DBPEDIA_SPARQL_URL = "https://dbpedia.org/sparql"

def normalize_term(term):
    return term.lower().replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "")

def terms_are_identical(term1, term2):
    normalized1 = normalize_term(term1)
    normalized2 = normalize_term(term2)
    return normalized1 == normalized2

def search_wikipedia(term):
    params = {
        "action": "query",
        "list": "search",
        "srsearch": term,
        "format": "json"
    }
    response = requests.get(WIKIPEDIA_API_URL, params=params)
    data = response.json()

    if "query" in data and "search" in data["query"]:
        best_match = None
        highest_ratio = 0
        for result in data["query"]["search"]:
            title = result["title"]
            if terms_are_identical(term, title):
                return title, 100  # Exact match
            similarity = fuzz.ratio(term.lower(), title.lower())
            if similarity > highest_ratio:
                highest_ratio = similarity
                best_match = title

        if best_match and highest_ratio >= 85: 
            return best_match, highest_ratio
    return None, 0

def get_dbpedia_ontology(term):
    normalized_term = normalize_term(term)
    sparql_query = f"""
    SELECT ?property ?value
    WHERE {{
        <http://dbpedia.org/resource/{normalized_term}> ?property ?value
    }}
    LIMIT 50
    """
    params = {
        "query": sparql_query,
        "format": "application/json"
    }
    response = requests.get(DBPEDIA_SPARQL_URL, params=params)
    if response.status_code == 200:
        print(f"Ontology loaded for {term}")
        return response.json()
    else:
        print(f"Error loading ontology for {term}")
        return None

def main():
    input_file_path = "terms.txt"  
    output_file_path = "ontology_results.json"  
    not_found_file_path = "not_found_terms.txt" 
    similar_terms_file_path = "similar_terms.txt"  
    

    with open(input_file_path, "r", encoding="utf-8") as file:
        terms = [line.strip() for line in file.readlines()]
    
    total_terms = len(terms)
    print(f"Loaded {total_terms} terms from the file.")

    results = {}
    not_found_terms = []  
    similar_terms = [] 
    found_count = 0  
    
    for term in terms:
        print(f"Searching for term: {term}")
        wiki_title, similarity = search_wikipedia(term)
        
        if wiki_title:
            if similarity == 100: 
                ontology = get_dbpedia_ontology(wiki_title)
                if ontology:
                    results[term] = ontology
                    found_count += 1
            else:  
                similar_terms.append(f"{term} -> {wiki_title} (similarity: {similarity:.2f}%)")
        else:
            not_found_terms.append(term)
    

    with open(output_file_path, "w", encoding="utf-8") as output_file:
        json.dump(results, output_file, ensure_ascii=False, indent=4)
    print(f"Results saved to {output_file_path}")


    if similar_terms:
        with open(similar_terms_file_path, "w", encoding="utf-8") as sim_file:
            sim_file.write("\n".join(similar_terms))
        print(f"List of similar terms saved to {similar_terms_file_path}")


    if not_found_terms:
        with open(not_found_file_path, "w", encoding="utf-8") as nf_file:
            nf_file.write("\n".join(not_found_terms))
        print(f"List of not found terms saved to {not_found_file_path}")
    

    print("\n--- Search Statistics ---")
    print(f"Total terms: {total_terms}")
    print(f"Found terms (exact match): {found_count}")
    print(f"Similar terms (85%+): {len(similar_terms)}")
    print(f"Not found terms: {len(not_found_terms)}")
    print(f"Percentage found: {found_count / total_terms * 100:.2f}%")

if __name__ == "__main__":
    main()
