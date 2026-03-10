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

Run the service (stdio transport, for use with Claude and other MCP clients):

```sh
python main.py
# or with uv:
uv run main.py
```

For local HTTP testing (e.g. with MCP Inspector), use the FastMCP CLI:

```sh
fastmcp run main.py --transport http --port 8080
```

The server registers the following tools:

- `get_datasets`: Fetch available IMF datasets
- `get_indicators(dataset_id)`: Fetch indicators for a dataset
- `get_countries(dataset_id)`: Fetch countries for a dataset
- `get_timeseries(indicator, countries, start, end)`: Fetch time series data for given indicator and countries over a year range
- `get_ifs_indicators()`: Fetch IFS (International Financial Statistics) indicator codes; use with `get_timeseries`
- `get_ifs_countries()`: Fetch IFS country/region codes; use with `get_timeseries`
- `get_retrieval_guide()`: Return the retrieval guide (markdown); call first when answering IMF data questions

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
- `CLAUDE_IMF_GUIDE.md` — Retrieval guide; exposed as tool `get_retrieval_guide()` and as MCP resource `imf://retrieval-guide`

## Development

To add new tools or extend functionality, edit `main.py` and use the `@mcp.tool()` decorator to register new async functions.

## Using IMF-MCP with Claude

### Using IMF-MCP as a Claude Tool

Claude (Anthropic's AI assistant) can launch IMF-MCP automatically as a tool. You do **not** need to run the server manually.

#### Configuration Example (Local Setup)

1. Open Claude settings and go to **Developer → Edit Config** (or add/edit your MCP config file, e.g. `claude_desktop_config.json` or the config used by your client).
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
	 - Replace `/Users/yourusername/path/to/imf-mcp` with the **absolute path** to your `imf-mcp` directory.
	 - The server runs over **stdio** by default, which is what Claude expects when it launches the process.
	 - This example uses [uv](https://github.com/astral-sh/uv) so dependencies from `pyproject.toml` are used. You can use `python` instead if you run from an environment where `pip install .` was already run:
	   ```json
	   "imf-mcp": {
	     "command": "python",
	     "args": ["/Users/yourusername/path/to/imf-mcp/main.py"]
	   }
	   ```

3. Save the config and restart Claude if necessary.

4. When you ask Claude to use the IMF tool (e.g., "List available IMF datasets"), Claude will launch the tool as needed.

**Retrieval guide:** The server exposes the guide as a **tool**: `get_retrieval_guide()`. When answering IMF data questions, call this first to get the recommended flow (dataset IDs like IFS/WEO, then get_indicators/get_countries for codes, then get_timeseries). The same content is also exposed as MCP resource `imf://retrieval-guide` for clients that support resource reading.

> **Note:**
> - Ensure the Python environment has all dependencies installed (e.g., via `uv pip install .` or `poetry install`).
> - You do not need to start the server yourself; Claude will handle launching and communication.
> - For advanced configuration, refer to your Claude platform documentation for custom tool integration.

#### Example timeseries analysis using Claude and IMF MCP

https://claude.ai/public/artifacts/001c61fa-f349-4c53-962e-2b7a1093d8cd

## License

MIT License. See [LICENSE](LICENSE) for details.
