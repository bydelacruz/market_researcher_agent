import os

import google.generativeai as genai
from dotenv import load_dotenv
from duckduckgo_search import DDGS

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


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


class Agent:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-flash-latest")
        self.chat = self.model.start_chat(history=[])
        self.is_active = True  # To track if the agent is active

        # THE INSTRUCTIONS
        self.system_prompt = """
        You are an AI Agent with access to tools.
        You do NOT know the current date.
        You do NOT know any real-time information (stock prices, weather, sports scores, etc).
        
        If the user asks for ANY real-time information, you MUST use the 'search_web' tool.

        TOOLS AVAILABLE:
        1. search_web(query): specific web search.
        2. calculate(expression): math calculator (e.g., "12 * 50").

        FORMAT INSTRUCTIONS:
        To use a tool, you MUST respond in this exact format:
        ACTION: tool_name("argument")
        """

        # Send system prompt
        try:
            self.chat.send_message(self.system_prompt)
        except Exception as e:
            print(f"⚠️ Error initializing Agent: {e}")
            self.is_active = False  # Mark as broken

    def ask(self, query):
        # 1. Send user query to Gemini
        print(f"👤 USER: {query}")

        try:
            response = self.chat.send_message(query)
            text = response.text.strip()
        except Exception as e:
            return f"⚠️ System Overload: My brain is tired (API Quota Exceeded). Please wait a minute and try again.\n\n(Error Detail: {e})"

            # 🔄 THE REACT LOOP
        # We allow up to 5 turns. If it takes more, it's probably stuck.
        for _ in range(5):
            # Check if it wants to use a tool
            if "ACTION:" in text:
                print(f"🤖 AGENT WANTS TO ACT: {text}")

                # --- PARSE ---
                try:
                    action_part = text.split("ACTION:")[1].strip()
                    start_quote = action_part.find('"')
                    end_quote = action_part.rfind('"')

                    tool_name = action_part[:start_quote].split("(")[0].strip()
                    argument = action_part[start_quote + 1 : end_quote]
                except Exception:
                    # If parsing fails, tell the AI
                    try:
                        text = self.chat.send_message(
                            'SYSTEM: Error parsing action. Use format: ACTION: tool_name("arg")'
                        ).text
                    except Exception as e:
                        return f"⚠️ System Overload: My brain is tired (API Quota Exceeded). Please wait a minute and try again.\n\n(Error Detail: {e})"
                    continue

                # --- EXECUTE ---
                tool_result = "Error: Tool not found"
                if tool_name == "search_web":
                    print(f"🌍 SEARCHING: {argument}")
                    tool_result = search_web(argument)
                elif tool_name == "calculate":
                    print(f"🧮 CALCULATING: {argument}")
                    tool_result = calculate(argument)

                # Check for empty results
                if not tool_result:
                    tool_result = "No results found."

                # --- OBSERVE (Feed back to AI) ---
                print(f"🕵️ OBSERVATION: {tool_result[:60]}...")

                # IMPORTANT: We overwrite 'text' with the NEW response from the AI
                # This allows the loop to check "Does it want to act AGAIN?"
                try:
                    response = self.chat.send_message(f"OBSERVATION: {tool_result}")
                    text = response.text.strip()
                except Exception as e:
                    return f"⚠️ System Overload: My brain is tired (API Quota Exceeded). Please wait a minute and try again.\n\n(Error Detail: {e})"

            else:
                # No "ACTION:" found? The Agent is done thinking.
                return text

        return "I tried too many steps and gave up."


if __name__ == "__main__":
    agent = Agent()
    # A question that requires 2 tools (search + math)
    print("USER: If i buy 15 shares of Apple, how much will it costs?")
    response = agent.ask("If i buy 15 shares of Apple, how much will it costs?")
    print(f"Agent: {response}")
    print(f"Agent: {response}")
