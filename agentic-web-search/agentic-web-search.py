from tavily import TavilyClient

# Step 1. Instantiating your TavilyClient
tavily_client = TavilyClient(api_key="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")

# Step 2. Executing a simple search query
answer = tavily_client.qna_search(query="Who is Leo Messi?")

# Step 3. That's it! You've done a Tavily Search!
print(answer)