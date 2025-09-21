# kb/fallback_mcp.py
import os
import requests

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError("❌ Missing Tavily API Key. Please set TAVILY_API_KEY environment variable.")

def search_web(query: str, max_results: int = 3):
    """
    Use Tavily API to perform a web search
    """
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "max_results": max_results
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        return []

    data = response.json()
    results = []
    for res in data.get("results", []):
        results.append({
            "title": res.get("title"),
            "content": res.get("content"),
            "url": res.get("url")
        })
    return results

if __name__ == "__main__":
    # quick test
    q = "Integrate sin(x) from 0 to pi/2"
    results = search_web(q)
    for r in results:
        print("-", r["title"], "\n ", r["content"][:150], "...\n", r["url"])
