# IMF-MCP retrieval guide (for Claude)

Use this when answering questions that need IMF data. It describes how the IMF DataMapper API works through the MCP tools so you can retrieve data in one or two steps instead of trial-and-error.

## How the API behaves

- **`get_datasets()`** returns the **IMF DataMapper** dataset list (WEO and other DataMapper series). It does **not** return the full **IFS** (International Financial Statistics) database — IFS is a separate, much larger dataset. Use `get_datasets()` to discover dataset IDs; for IFS content, always call **`get_indicators("IFS")`** and **`get_countries("IFS")`** directly.
- To get **usable series**, you need a **dataset ID** (e.g. `IFS`), then call **`get_indicators(dataset_id)`** and **`get_countries(dataset_id)`** to get the **codes** used in `get_timeseries`.
- **`get_timeseries(indicator, countries, start, end)`** requires **indicator and country codes** (from the indicators/countries responses for that dataset), not full names. Years are integers.

## Recommended flow

1. **If the user wants IFS (International Financial Statistics):**  
   Call **`get_ifs_indicators()`** and **`get_ifs_countries()`** (or `get_indicators("IFS")` / `get_countries("IFS")`). Do not rely on `get_datasets()` for IFS — it returns the DataMapper set, not the full IFS database. Use the returned codes for `get_timeseries`.

2. **If the user wants another dataset (e.g. WEO) or asks “what’s available”:**  
   Call `get_datasets()` to list dataset IDs and names. For concrete series, call `get_indicators(dataset_id)` and `get_countries(dataset_id)` for the relevant dataset.

3. **For time series:**  
   Use **codes** from the indicators and countries responses, e.g.  
   `get_timeseries("NGDP_R", "US", 2019, 2023)`  
   not full names.

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

## IFS (International Financial Statistics) specifics

- **IFS is separate from the DataMapper list:** The list returned by `get_datasets()` reflects DataMapper coverage (e.g. WEO). For IFS, call **`get_ifs_indicators()`** and **`get_ifs_countries()`** (or `get_indicators("IFS")` / `get_countries("IFS")`) to get the full live list — IFS contains thousands of indicators.
- **SDMX-style codes:** IFS uses SDMX-style indicator codes that can include frequency and base-year suffixes, e.g. `.A` (annual), `.Q` (quarterly). The exact code may depend on frequency and base year; use the codes returned by `get_indicators("IFS")` for reliable lookups.
- **Granularity:** IFS is more granular than WEO — it reports higher-frequency (quarterly, monthly) data where available.

## Tool summary

| Tool | Purpose |
|------|---------|
| `get_datasets()` | List dataset IDs and metadata (not full indicator/country lists). |
| `get_indicators(dataset_id)` | Get indicator **codes** for that dataset (required for `get_timeseries`). |
| `get_countries(dataset_id)` | Get country/region **codes** for that dataset (required for `get_timeseries`). |
| **`get_ifs_indicators()`** | IFS indicator codes (prefer over get_indicators for IFS). |
| **`get_ifs_countries()`** | IFS country/region codes (prefer over get_countries for IFS). |
| `get_timeseries(indicator, countries, start, end)` | Get series; use **codes** from indicators/countries and integer years. |

**`countries`** in `get_timeseries` can be a single code (e.g. `"US"`) or comma-separated (e.g. `"US,CN"`).
