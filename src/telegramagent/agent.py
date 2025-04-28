from __future__ import annotations

from agents import Agent
from agents import Runner
from agents import TResponseInputItem
from agents.mcp import MCPServerStdio

from .config import Config


class OpenAIAgent:
    def __init__(self, agent: Agent, max_input_items: int | None = None) -> None:
        self.agent = agent
        self.max_input_items = max_input_items
        self.input_items: list[TResponseInputItem] = []

    @classmethod
    def from_config(cls, config: Config) -> OpenAIAgent:
        agent = Agent(
            name=config.name,
            instructions=config.instructions,
            mcp_servers=[MCPServerStdio(params=params, name=name) for name, params in config.mcp_servers.items()],
        )
        return cls(agent)

    async def connect(self) -> None:
        for mcp_server in self.agent.mcp_servers:
            await mcp_server.connect()

    async def cleanup(self) -> None:
        for mcp_server in self.agent.mcp_servers:
            await mcp_server.cleanup()

    async def run(self, text) -> str:
        self.input_items.append(
            {
                "role": "user",
                "content": text,
            }
        )

        result = await Runner.run(
            starting_agent=self.agent,
            input=self.input_items,
        )

        self.input_items = result.to_input_list()

        if self.max_input_items is not None:
            self.input_items = self.input_items[-self.max_input_items :]

        return result.final_output
