from data3_network_agent.lib import Data3AgentUtils

data3 = Data3AgentUtils()
TELEGRAM_TOKEN = data3.fetch_agent_env_variables(docker_service_name="agentic-rag-telegram-bot", field_names=["TELEGRAM_TOKEN"])["TELEGRAM_TOKEN"]

TELEGRAM_TOKEN = "7837158639:AAFlhIe89140GKqlhnd-HG8ivejC__i_WCE"
PROD_BASE_URL = 'http://host.docker.internal:7000'
DEV_BASE_URL = 'http://127.0.0.1:7000'

IS_PROD = False

BASE_URL = PROD_BASE_URL if IS_PROD else DEV_BASE_URL