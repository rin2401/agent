import requests
import json
import sys

def search_anime(query):
    url = f"https://api.jikan.moe/v4/anime?q={query}&limit=5"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Failed to fetch data ({response.status_code})")
        return []
    data = response.json()
    return data.get('data', [])

def extract_info(anime):
    return {
        'title': anime.get('title'),
        'title_japanese': anime.get('title_japanese'),
        'synopsis': anime.get('synopsis'),
        'episodes': anime.get('episodes'),
        'score': anime.get('score'),
        'genres': [g['name'] for g in anime.get('genres', [])],
        'aired': anime.get('aired', {}).get('string'),
        'url': anime.get('url'),
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python anime_crawler.py <anime title>")
        sys.exit(1)
    query = " ".join(sys.argv[1:])
    print(f"Searching for: {query}\n")
    results = search_anime(query)
    if not results:
        print("No results found.")
        return
    infos = [extract_info(a) for a in results]
    print(json.dumps(infos, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
