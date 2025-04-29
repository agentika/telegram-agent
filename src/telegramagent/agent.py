from __future__ import annotations

from agents import Agent
from agents import Runner
from agents.mcp import MCPServerStdio

from .cache import get_cache_from_env
from .config import Config
from .model import get_openai_model
from .model import get_openai_model_settings


class OpenAIAgent:
    def __init__(self, agent: Agent, max_input_items: int | None = None) -> None:
        self.agent = agent
        self.max_input_items = max_input_items
        self.cache = get_cache_from_env()

    @classmethod
    def from_config(cls, config: Config) -> OpenAIAgent:
        agent = Agent(
            name=config.name,
            instructions=config.instructions,
            model=get_openai_model(),
            model_settings=get_openai_model_settings(),
            mcp_servers=[
                MCPServerStdio(params=params.model_dump(), name=name) for name, params in config.mcp_servers.items()
            ],
        )
        return cls(agent)

    async def connect(self) -> None:
        for mcp_server in self.agent.mcp_servers:
            await mcp_server.connect()

    async def cleanup(self) -> None:
        for mcp_server in self.agent.mcp_servers:
            await mcp_server.cleanup()

    async def run(self, text, cache_key: str) -> str:
        input_items = await self.cache.get(cache_key)
        if input_items is None:
            input_items = []

        input_items.append(
            {
                "role": "user",
                "content": text,
            }
        )

        result = await Runner.run(
            starting_agent=self.agent,
            input=input_items,
        )

        input_items = result.to_input_list()
        if self.max_input_items is not None:
            input_items = input_items[-self.max_input_items :]
        await self.cache.set(cache_key, input_items)

        return result.final_output
