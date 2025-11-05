# IMF-MCP

IMF-MCP is a Python service that provides programmatic access to the International Monetary Fund (IMF) DataMapper API using the FastMCP framework. It exposes tools for fetching datasets, indicators, countries, and time series data from the IMF.

## Features

- Fetch available IMF datasets
- Retrieve indicators for a dataset
- List countries for a dataset
- Query time series data for specific indicators and countries
- Asynchronous HTTP requests for efficient data access

## Requirements

- Python 3.10+
- [httpx](https://www.python-httpx.org/)
- [FastMCP](https://github.com/cutover/fastmcp) (or your local MCP server package)

## Installation

1. Clone this repository:
	```sh
	git clone https://github.com/your-org/imf-mcp.git
	cd imf-mcp
	```
2. Install dependencies using `pyproject.toml`:
	```sh
	pip install .
	# or, if you use poetry:
	poetry install
	```

## Usage

Run the service:

```sh
python main.py
```

This will start the FastMCP server and register the following tools:

- `get_datasets`: Fetch available IMF datasets
- `get_indicators(dataset_id)`: Fetch indicators for a dataset
- `get_countries(dataset_id)`: Fetch countries for a dataset
- `get_timeseries(indicator, countries, start, end)`: Fetch time series data for given indicator and countries over a year range

### Example: Fetching Datasets

You can use the registered tools via the MCP interface or by extending the project. Example code to fetch datasets:

```python
from main import get_datasets
import asyncio

async def main():
	 datasets = await get_datasets()
	 print(datasets)

asyncio.run(main())
```

## Project Structure

- `main.py` — Main application file, defines all tools and starts the server
- `README.md` — Project documentation

## Development

To add new tools or extend functionality, edit `main.py` and use the `@mcp.tool()` decorator to register new async functions.

## Using IMF-MCP with Claude

### Using IMF-MCP as a Claude Tool

Claude (Anthropic's AI assistant) can launch IMF-MCP automatically as a tool. You do **not** need to run the server manually.

#### Configuration Example (Local Setup)

1. Open Claude settings and go to **Developer → Edit Config**.
2. Add an entry to the `mcpServers` section like this:

	 ```json
	 "imf-mcp": {
		 "command": "uv",
		 "args": [
			 "--directory",
			 "/Users/yourusername/path/to/imf-mcp",
			 "run",
			 "main.py"
		 ]
	 }
	 ```
	 - Replace `/Users/yourusername/path/to/imf-mcp` with the actual path to your `imf-mcp` directory.
	 - This example uses [uv](https://github.com/astral-sh/uv) to run the project in the correct environment. You can also use `python` or another environment manager if preferred.

3. Save the config and restart Claude if necessary.

4. When you ask Claude to use the IMF tool (e.g., "List available IMF datasets"), Claude will launch the tool as needed.

> **Note:**
> - Ensure the Python environment has all dependencies installed (e.g., via `uv pip install .` or `poetry install`).
> - You do not need to start the server yourself; Claude will handle launching and communication.
> - For advanced configuration, refer to your Claude platform documentation for custom tool integration.

## License

MIT License. See [LICENSE](LICENSE) for details.
