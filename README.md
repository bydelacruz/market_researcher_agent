# 🤖 AI Market Researcher Agent

An autonomous AI Agent capable of performing multi-step reasoning to answer complex questions. Unlike standard LLMs, this agent is equipped with **Tools** (Web Search and Calculator) and uses the **ReAct (Reason + Act)** pattern to determine _when_ and _how_ to use them.

## 🚀 Features

- **Autonomous Reasoning Loop:** Uses a custom-built ReAct loop to "Think, Act, and Observe" before answering.
- **Real-Time Web Access:** Integrated `duckduckgo-search` to fetch current events and market data (bypassing the LLM's knowledge cutoff).
- **Deterministic Math:** Features a custom Stack-based calculator to ensure 100% mathematical accuracy, avoiding LLM hallucinations.
- **Resilient Architecture:** Includes fallback mechanisms for API rate limits and robust error handling for tool parsing.
- **Session-Based Memory:** Built with Streamlit Session State to maintain conversational context across multiple turns.

## 🛠️ Tech Stack

- **Core Logic:** Python 3.10+
- **LLM Engine:** Google Gemini (via `google-generativeai`)
- **Web Tooling:** DuckDuckGo Search (`ddgs`)
- **Frontend:** Streamlit
- **Environment:** `python-dotenv` for secure API key management

## 🧠 How It Works

The Agent follows a strict **Thought-Action-Observation** cycle:

1.  **User Query:** "If I buy 15 shares of Apple, how much will it cost?"
2.  **Reasoning:** The Agent realizes it needs the current price.
3.  **Action 1:** `search_web("Apple stock price")`
4.  **Observation:** Python fetches the price (e.g., "$200") and feeds it back to the LLM.
5.  **Reasoning:** The Agent sees the price and realizes it needs to calculate the total.
6.  **Action 2:** `calculate("200 * 15")`
7.  **Final Answer:** "The total cost is $3,000."

## 📦 Installation

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/bydelacruz/market-researcher-agent.git]
    cd market-researcher-agent
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Environment:**
    Create a `.env` file in the root directory:

    ```ini
    GEMINI_API_KEY=your_api_key_here
    ```

4.  **Run the Application:**
    ```bash
    streamlit run app.py
    ```
