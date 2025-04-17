import requests
import json
import sys

def search_anilist(query):
    url = "https://graphql.anilist.co"
    graphql_query = '''
    query ($search: String) {
      Page(perPage: 5) {
        media(search: $search, type: ANIME) {
          title {
            romaji
            english
            native
          }
          description(asHtml: false)
          episodes
          averageScore
          genres
          startDate { year month day }
          endDate { year month day }
          siteUrl
        }
      }
    }
    '''
    variables = {"search": query}
    response = requests.post(url, json={"query": graphql_query, "variables": variables})
    if response.status_code != 200:
        print(f"Error: Failed to fetch data from AniList ({response.status_code})")
        return []
    data = response.json()
    return data.get('data', {}).get('Page', {}).get('media', [])

def extract_info(anime):
    return {
        'title_romaji': anime['title'].get('romaji'),
        'title_english': anime['title'].get('english'),
        'title_native': anime['title'].get('native'),
        'description': anime.get('description'),
        'episodes': anime.get('episodes'),
        'average_score': anime.get('averageScore'),
        'genres': anime.get('genres'),
        'start_date': anime.get('startDate'),
        'end_date': anime.get('endDate'),
        'url': anime.get('siteUrl'),
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python anime_crawler.py <anime title>")
        sys.exit(1)
    query = " ".join(sys.argv[1:])
    print(f"Searching AniList for: {query}\n")
    results = search_anilist(query)
    if not results:
        print("No results found.")
        return
    infos = [extract_info(a) for a in results]
    print(json.dumps(infos, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
