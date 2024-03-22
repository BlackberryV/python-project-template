from app.entities.agent_data import AgentData
from app.entities.processed_agent_data import ProcessedAgentData


def process_agent_data(
    agent_data: AgentData,
) -> ProcessedAgentData:
    print(agent_data)
    return ProcessedAgentData(road_state="bad road" if 0 > agent_data.accelerometer.y else "good road", agent_data=agent_data)
