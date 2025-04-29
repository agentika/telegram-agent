# Telegram Agent

```sh
export BOT_TOKEN=
export OPENAI_API_KEY=

# use redis cache
export CACHE_URL="redis://localhost:6379/0?pool_max_size=1"

# or use memory cache
export CACHE_URL="memory://"

uv run telegramagent
```
