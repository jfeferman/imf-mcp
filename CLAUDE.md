# IMF-MCP retrieval guide (for Claude)

Use this when answering questions that need IMF data. This MCP uses the **IMF DataMapper API** (v1) only. That API exposes the same series as the [IMF DataMapper](https://www.imf.org/external/datamapper/) app — a curated set of indicators and datasets, not the full underlying databases (e.g. the full IFS code list is much larger and available via other IMF APIs like SDMX).

## How the API behaves

- **DataMapper vs full IFS:** The tools talk to the **DataMapper API**. `get_ifs_indicators()` and `get_indicators("IFS")` return **whatever that API exposes** for IFS — often the same or similar to the broader DataMapper indicator set, not the full IFS code list. Use the **codes returned by these tools** with `get_timeseries`; those are the codes this API accepts.
- **`get_datasets()`** returns the dataset list the DataMapper API knows about. Use **`get_indicators(dataset_id)`** and **`get_countries(dataset_id)`** (or `get_ifs_indicators()` / `get_ifs_countries()`) to get the **codes** that work with `get_timeseries`.
- **`get_timeseries(indicator, countries, start, end)`** requires **indicator and country codes** from those responses, not full names. Years are integers. **Only request the countries the user asked for** — resolve their query to codes first; do not request data for all countries.

## Recommended flow

1. **If the user wants IFS-style data:**  
   Call **`get_ifs_indicators()`** and **`get_ifs_countries()`** to get the indicator and country codes **this API** exposes. Use only those returned codes with `get_timeseries`. (What the API returns may be DataMapper coverage; the full IFS database is elsewhere.)

2. **If the user wants another dataset (e.g. WEO) or asks “what’s available”:**  
   Call `get_datasets()` to list dataset IDs and names. For concrete series, call `get_indicators(dataset_id)` and `get_countries(dataset_id)` for the relevant dataset.

3. **For time series — resolve countries first:**  
   **Do not** request data for all countries. First get the relevant country/region list (`get_ifs_countries()` or `get_countries(dataset_id)`), map the **user’s query** to the correct codes (e.g. “Germany” → DE, “US and China” → US,CN), then call `get_timeseries(indicator, countries, start, end)` only for those codes. Use indicator and country **codes** from the indicators/countries responses, not full names.

## Common dataset IDs

| ID   | Description                          |
|------|--------------------------------------|
| **IFS** | International Financial Statistics   |
| **WEO** | World Economic Outlook               |
| **FSI** | Financial Soundness Indicators       |
| **GFS** | Government Finance Statistics        |
| **BOP** | Balance of Payments                  |
| **CPI** | Consumer Price Index                 |

When in doubt, start with **IFS** or **WEO** for macroeconomic and growth data.

## IFS and DataMapper — what this API returns

- **This MCP uses the DataMapper API only.** `get_ifs_indicators()` (and `get_indicators("IFS")`) return whatever that API exposes — often the **broader DataMapper indicator set**, not the full IFS code list. The full International Financial Statistics (IFS) database is larger and is accessed via other IMF channels (e.g. SDMX). Do not claim this tool returns "the full IFS"; say it returns the IFS-related indicators **available through this DataMapper API**, and use those codes with `get_timeseries`.
- **Always use the codes this API returns.** For time series, use only indicator and country codes from `get_ifs_indicators()` / `get_ifs_countries()` (or the generic get_indicators / get_countries) with `get_timeseries`. Indicator codes may include suffixes (e.g. `.A`, `.Q`); use the exact codes from the response.
- **If the user asks about "full IFS" or SDMX:** You can explain that this tool is built on the DataMapper API and exposes its curated set; the full IFS is available through the IMF’s other APIs (e.g. [SDMX](https://data.imf.org/)).

## Tool summary

| Tool | Purpose |
|------|---------|
| `get_datasets()` | List dataset IDs and metadata (not full indicator/country lists). |
| `get_indicators(dataset_id)` | Get indicator **codes** for that dataset (required for `get_timeseries`). |
| `get_countries(dataset_id)` | Get country/region **codes** for that dataset (required for `get_timeseries`). |
| **`get_ifs_indicators()`** | Indicator codes for IFS **as exposed by the DataMapper API**; use with get_timeseries. |
| **`get_ifs_countries()`** | Country/region codes for IFS from this API; use with get_timeseries. |
| `get_timeseries(indicator, countries, start, end)` | Get series for **only the countries in the user’s query**. Resolve names to codes first; do not request all countries. |

**Time series and countries:** Resolve the user’s intent to specific country/region codes (using the countries list for that dataset), then pass only those codes to `get_timeseries` — e.g. `"US"` or `"US,CN"`. Do not fetch data for every country when the user asked about one or a few.
