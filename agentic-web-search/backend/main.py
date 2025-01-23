from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tavily import TavilyClient
from data3_network_agent.lib import Data3AgentUtils

# Initialize the FastAPI app
app = FastAPI()

# Define the request model
class QueryRequest(BaseModel):
    query: str

# Define the response model
class QueryResponse(BaseModel):
    answer: str

@app.post("/search", response_model=QueryResponse)
async def search(query_request: QueryRequest):
    try:
        data3 = Data3AgentUtils()
        api_key = data3.fetch_agent_env_variables(docker_service_name="agentic-web-search", field_names=["TAVILY_API_KEY"])
        tavily_client = TavilyClient(api_key=api_key["TAVILY_API_KEY"])
        # Execute the Tavily search query
        answer = tavily_client.qna_search(query=query_request.query)
        return QueryResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during search: {str(e)}")

# Example route to check server status
@app.get("/status")
async def status():
    return {"status": "Server is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)