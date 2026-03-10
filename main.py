from pathlib import Path
from typing import Any
import httpx
from fastmcp import FastMCP

mcp = FastMCP("ImfDataServer")
_DIR = Path(__file__).resolve().parent
IMF_API_BASE = "https://www.imf.org/external/datamapper/api/v1"

async def make_imf_request(endpoint: str, params: dict = None) -> dict[str, Any] | None:
    url = f"{IMF_API_BASE}/{endpoint}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            return data
        except Exception:
            return None

@mcp.tool()
async def get_datasets() -> dict:
    """Fetch available IMF datasets."""
    result = await make_imf_request("datasets")
    return result

@mcp.tool()
async def get_indicators(dataset_id: str) -> dict:
    """Fetch indicators for a dataset."""
    result = await make_imf_request("indicators", {"datasets": dataset_id})
    return result

@mcp.tool()
async def get_countries(dataset_id: str) -> dict:
    """Fetch countries for a dataset."""
    result = await make_imf_request("countries", {"datasets": dataset_id})
    return result

@mcp.tool()
async def get_timeseries(indicator: str, countries: str, start: int, end: int) -> dict:
    """Fetch time series data from IMF using indicator and country codes in the URL path, and periods as a query parameter."""
    periods = ",".join(str(y) for y in range(start, end + 1))
    path = f"timeseries/{indicator}/{countries}"
    params = {"periods": periods}
    result = await make_imf_request(path, params)
    return result


@mcp.tool()
async def get_ifs_indicators() -> dict:
    """Fetch indicator codes for International Financial Statistics (IFS). IFS is a large dataset (thousands of indicators); use these codes with get_timeseries. Codes may include SDMX-style suffixes (e.g. .A annual, .Q quarterly)."""
    return await make_imf_request("indicators", {"datasets": "IFS"})


@mcp.tool()
async def get_ifs_countries() -> dict:
    """Fetch country/region codes for International Financial Statistics (IFS). Use these codes with get_timeseries (e.g. US, CN)."""
    return await make_imf_request("countries", {"datasets": "IFS"})


def _read_retrieval_guide() -> str:
    path = _DIR / "CLAUDE_IMF_GUIDE.md"
    return path.read_text(encoding="utf-8") if path.exists() else ""


@mcp.tool()
async def get_retrieval_guide() -> str:
    """Return the IMF-MCP retrieval guide (markdown). Call this first when the user asks for IMF data: it explains how the API works (get_datasets returns only metadata; use get_indicators(dataset_id) and get_countries(dataset_id) for codes), recommended flow, and common dataset IDs (e.g. IFS, WEO). Use the guide to avoid trial-and-error when calling get_indicators, get_countries, and get_timeseries."""
    return _read_retrieval_guide()


@mcp.resource("imf://retrieval-guide")
def get_retrieval_guide_resource() -> str:
    """Return the IMF-MCP retrieval guide: how the API works, recommended flow, and common dataset IDs. Read this first when using IMF tools to avoid trial-and-error."""
    return _read_retrieval_guide()


def main():
    # Stdio is the default; required for Claude Desktop and other MCP clients that launch via subprocess.
    mcp.run()

if __name__ == "__main__":
    main()