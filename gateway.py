# gateway.py
import re
from math_agent import solve_math

def input_guardrail(query: str) -> bool:
    """
    Input guardrail: only allow math-related queries.
    Returns True if query is valid, False if blocked.
    """
    math_keywords = [
        r"\bintegral\b", r"\bderivative\b", r"\bsolve\b", r"\bequation\b",
        r"\blog\b", r"\btriangle\b", r"\barea\b", r"\bvolume\b",
        r"\bmatrix\b", r"\bdeterminant\b", r"\blimit\b", r"\bsum\b",
        r"x", r"y", r"\d+"  # variables or numbers
    ]
    combined = re.compile("|".join(math_keywords), re.IGNORECASE)
    return bool(combined.search(query))

def output_guardrail(response: str) -> str:
    """
    Output guardrail: ensure only math/educational responses.
    If response is irrelevant or empty, return safe fallback.
    """
    if not response or len(response.strip()) == 0:
        return "Sorry, I could not generate a valid math solution."

    # allow responses that contain numbers, math symbols, or steps
    if re.search(r"[0-9=+\-*/^()]", response):
        return response

    # fallback safe response
    return "Sorry, I can only provide math-related answers."

def ai_gateway(query: str):
    """
    AI Gateway wrapper with input/output guardrails.
    """
    # Input guardrail
    if not input_guardrail(query):
        return {
            "source": "gateway",
            "solution": "Sorry, I can only answer educational mathematics questions."
        }

    # Run the math agent
    ans = solve_math(query)
    raw_solution = ans.get("solution", "")

    # Output guardrail
    safe_solution = output_guardrail(raw_solution)

    return {
        "source": ans.get("source", "unknown"),
        "solution": safe_solution
    }

if __name__ == "__main__":
    tests = [
        "Who is the president of USA?",
        "Solve x^2 - 5x + 6 = 0",
        "Tell me a joke",
        "Integrate sin(x) from 0 to pi/2"
    ]
    for q in tests:
        print("\nQUERY:", q)
        ans = ai_gateway(q)
        print("SOURCE:", ans["source"])
        print("SOLUTION:\n", ans["solution"])
