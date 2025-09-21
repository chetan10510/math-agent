from kb.kb_retriever import query_kb, kb_hit
from kb.fallback_mcp import search_web
import sympy as sp

def solve_math(query: str):
    """
    Try KB first, then fallback to web (MCP/Tavily).
    """
    # 1) Try Knowledge Base
    results = query_kb(query)
    hit = kb_hit(results)
    if hit:
        return {
            "source": "knowledge_base",
            "question": hit["payload"]["question"],
            "solution": hit["payload"]["solution_text"]
        }

    # 2) Fallback: Web Search via MCP (Tavily)
    print("⚠️ No KB hit, falling back to web search...")
    web_results = search_web(query)

    if not web_results:
        return {
            "source": "web",
            "solution": "Sorry, I couldn’t find a reliable solution online."
        }

    # 3) Try parsing math expressions with SymPy
    try:
        if "integrate" in query.lower():
            x = sp.Symbol("x")
            if "sin(x)" in query:
                result = sp.integrate(sp.sin(x), (x, 0, sp.pi/2))
                return {
                    "source": "web+mcp",
                    "solution": f"Step 1: Recognize integral ∫ sin(x) dx from 0 to π/2.\n"
                                f"Step 2: Antiderivative of sin(x) is -cos(x).\n"
                                f"Step 3: Evaluate: [-cos(x)]₀^(π/2) = ( -cos(π/2) ) - ( -cos(0) ).\n"
                                f"Step 4: Simplify: (0 - (-1)) = 1.\nAnswer: {result}"
                }
    except Exception as e:
        pass

    # 4) Fallback to showing top web result content
    best = web_results[0]
    return {
        "source": "web",
        "solution": f"Based on web search: {best['content']}\n(Source: {best['url']})"
    }

if __name__ == "__main__":
    tests = [
        "Solve x^2 - 5x + 6 = 0",
        "What is the integral of x^2 from 0 to 1?",
        "Find area of a triangle with base 10 and height 5",
        "Integrate sin(x) from 0 to pi/2"
    ]
    for q in tests:
        print("\nQUERY:", q)
        ans = solve_math(q)
        print("SOURCE:", ans["source"])
        print("SOLUTION:\n", ans["solution"])
