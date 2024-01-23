from langchain.agents import create_sql_agent 
from langchain.agents.agent_toolkits import SQLDatabaseToolkit 
from langchain.sql_database import SQLDatabase 
from langchain.llms.openai import OpenAI 
from langchain.agents.agent_types import AgentType

class DatabaseConnection:

    postgres_connection_string =f"postgresql+psycopg2://flightrw:2OmbZ&QZf66@psql.impressicocrm.com:5432/flight_delays"
    db = SQLDatabase.from_uri(postgres_connection_string,sample_rows_in_table_info=0,)
    openai_api_key = "openai_key"

    openai_llm = OpenAI(api_key=openai_api_key, temperature=0, model_name='gpt-3.5-turbo')
    toolkit = SQLDatabaseToolkit(db=db, llm=openai_llm)
    agent_executor = create_sql_agent(
        llm=openai_llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True
        )
    
    
