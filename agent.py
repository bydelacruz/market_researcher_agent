from duckduckgo_search import DDGS


def search_web(query: str) -> str:
    if not query:
        return "Please provide a search query"

    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=3))

        formatted_result = ""

        for result in results:
            formatted = f"""
                Title: {result["title"]}\n
                Link: {result["href"]}\n
                snippet: {result["body"]}\n
            """
            formatted_result += formatted

        return formatted_result


def calculate(expression: str) -> str:
    if not expression:
        return "Please provide an expression"

    stack = []
    current_num = 0
    last_op = "+"

    # We add a dummy operator at the end to force the last number to be processed
    expression = expression.replace(" ", "") + "+"

    ops = set(["+", "-", "*", "/"])

    for i, char in enumerate(expression):
        if char.isdigit():
            # BUILD the number (e.g., if we have 1, and see 2, it becomes 12)
            current_num = (current_num * 10) + int(char)

        if char in ops:
            # The number ended! Now we process it based on the PREVIOUS operator
            if last_op == "+":
                stack.append(current_num)
            elif last_op == "-":
                stack.append(-current_num)
            elif last_op == "*":
                # POP immediately, multiply, push back
                prev = stack.pop()
                stack.append(prev * current_num)
            elif last_op == "/":
                prev = stack.pop()
                if current_num == 0:
                    return "Error: Division by zero"
                # Use int conversion for clean integer division if desired, or float
                stack.append(prev / current_num)

            # Reset for the next number
            last_op = char
            current_num = 0

    return str(sum(stack))
