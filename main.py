
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("imf")

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
    # countries: comma-separated country codes (e.g., "BR,US,CN")
    # indicator: indicator code (e.g., "NGDP_RPCH")
    # periods: comma-separated years
    periods = ",".join(str(y) for y in range(start, end + 1))
    path = f"timeseries/{indicator}/{countries}"
    params = {"periods": periods}
    result = await make_imf_request(path, params)
    return result

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()