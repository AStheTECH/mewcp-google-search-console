**Full Google Search Console control — search analytics, sitemaps, sites, and URL inspection via MCP.**

A Model Context Protocol (MCP) server that exposes Google Search Console's API for querying search traffic data, managing sitemaps and sites, and inspecting URL indexing status.


## Overview

The mewcp-google-search-console MCP Server provides comprehensive access to Google Search Console through authenticated API calls:

- Query search analytics data with flexible dimension grouping and filtering
- Manage sitemaps: list, get, submit, and delete sitemap entries
- Manage sites: add, remove, and inspect Search Console properties
- Inspect the indexed status of any URL within your properties

Perfect for:

- SEO teams monitoring search performance and diagnosing indexing issues
- Developers automating sitemap submission and site property management
- Analysts pulling search traffic data programmatically for reporting pipelines


## Tools


<details>
<summary><code>get_search_analysis</code> — Query search traffic data with filters and grouping dimensions</summary>

Query your search traffic data with filters and parameters that you define. The method returns zero or more rows grouped by the row keys (dimensions) that you define. You must define a date range of one or more days. When date is one of the dimensions, any days without data are omitted from the result list. To learn which days have data, issue a query without filters grouped by date, for the date range of interest. Results are sorted by click count descending. If two rows have the same click count, they are sorted in an arbitrary way.

**Inputs:**
```
- `siteUrl` (string, required) — The site's URL, including protocol. For a URL-prefix property, supply the full URL (e.g. 'https://www.example.com/'). For a domain property, supply 'sc-domain:example.com'.
- `startDate` (string, required) — Start date of the requested date range, in YYYY-MM-DD format, in PT time (UTC - 7:00/8:00). Must be less than or equal to the end date. This value is included in the range.
- `endDate` (string, required) — End date of the requested date range, in YYYY-MM-DD format, in PT time (UTC - 7:00/8:00). Must be greater than or equal to the start date. This value is included in the range.
- `dimensions` (array of string, optional) — Zero or more dimensions to group results by. Results are grouped in the order that you supply these dimensions. You can use any dimension name in dimensionFilterGroups[].filters[].dimension as well as date and hour. The grouping dimension values are combined to create a unique key for each result row. If no dimensions are specified, all values will be combined into a single row. There is no limit to the number of dimensions that you can group by, but you cannot group by the same dimension twice. Example: [country, device]
- `type` (string, optional) — Filter results to the following type: discover: Discover results; googleNews: Results from news.google.com and the Google News app on Android and iOS. Doesn't include results from the News tab in Google Search., news: Search results from the News tab in Google Search., image: Search results from the Image tab in Google Search.; video: Video search results; web: [Default] Filter results to the combined (All) tab in Google Search. Does not include Discover or Google News results.
- `dimensionFilterGroups` (array of DimensionFilterGroup, optional) — Zero or more groups of filters to apply to the dimension grouping values. All filter groups must match in order for a row to be returned in the response. Within a single filter group, you can specify whether all filters must match, or at least one must match.
- `aggregationType` (string, optional) — How data is aggregated. 'auto': [Default] let the service decide. 'byNewsShowcasePanel': aggregate by News Showcase panel (requires the NEWS_SHOWCASE searchAppearance filter and type=discover or type=googleNews). 'byPage': aggregate by URI. 'byProperty': aggregate by property (not supported for type=discover or type=googleNews). Note: if you group or filter by page, you cannot aggregate by property.
- `rowLimit` (integer, optional, default: 1000) — The maximum number of rows to return. Valid range is 1-25,000; default is 1,000. To page through results, use the startRow offset.
- `startRow` (integer, optional, default: 0) — Zero-based index of the first row in the response. Must be a non-negative number. Default is 0. If startRow exceeds the number of results for the query, the response will be a successful response with zero rows.
- `dataState` (string, optional) — If 'all' (case-insensitive), data will include fresh data. If 'final' (case-insensitive) or if omitted, the returned data will include only finalized data. If 'hourly_all' (case-insensitive), data will include an hourly breakdown; this indicates that hourly data includes partial data and should be used when grouping by the HOUR API dimension.
```

**`dimensionFilterGroups` item schema:**
```
- `groupType` (string, optional, default: "and") — Whether all filters in this group must return true ('and'), or one or more must return true (not yet supported). Acceptable value: 'and' (all filters must return true).
- `filters` (array of DimensionFilter, optional) — Zero or more filters to test against the row. Each filter consists of a dimension name, an operator, and a value. Examples: country equals FRA; query contains mobile use; device notContains tablet.
```

**`filters` item schema:**
```
- `dimension` (string, required) — The dimension that this filter applies to. You can filter by any dimension even if you are not grouping by it. 'country': 3-letter country code (ISO 3166-1 alpha-3). 'device': DESKTOP, MOBILE or TABLET. 'page': a URI string. 'query': a query string. 'searchAppearance': a specific search result feature.
- `operator` (string, optional, default: "equals") — How your specified value must match (or not match) the dimension value. 'contains': row value contains or equals expression (non-case-sensitive). 'equals': [Default] exact match (case-sensitive for page and query). 'notContains': row value must not contain expression. 'notEquals': must not exactly equal. 'includingRegex': RE2 regex that must match. 'excludingRegex': RE2 regex that must not match.
- `expression` (string, required) — The value for the filter to match or exclude, depending on the operator. Max length 4096 characters.
```

**Output `data` schema:**

```typescript
{
  rows: any[];
  responseAggregationType: string | null;
}
```

</details>


<details>
<summary><code>delete_sitemap</code> — Permanently delete a sitemap entry (destructive, requires user confirmation)</summary>

DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Permanently deletes a sitemap from this site. This action is irreversible — the sitemap entry cannot be recovered once deleted. NEVER call this tool autonomously or as part of an automated flow. You MUST stop, tell the user exactly what will be deleted and that it is permanent, and wait for their explicit written confirmation before proceeding.

**Inputs:**
```
- `feedpath` (string, required) — The URL of the actual sitemap. For example: http://www.example.com/sitemap.xml
- `siteUrl` (string, required) — The URL of the property as defined in Search Console. For example: http://www.example.com/
```

**Output `data` schema:**

```typescript
{
  success: boolean;
  message: string | null;
}
```

</details>


<details>
<summary><code>get_sitemap</code> — Retrieve information about a specific sitemap</summary>

Retrieves information about a specific sitemap.

**Inputs:**
```
- `feedpath` (string, required) — The URL of the actual sitemap. For example: http://www.example.com/sitemap.xml
- `siteUrl` (string, required) — The URL of the property as defined in Search Console. For example: http://www.example.com/
```

**Output `data` schema:**

```typescript
{
  path: string | null;
  lastSubmitted: string | null;
  isPending: boolean | null;
  isSitemapsIndex: boolean | null;
  type: string | null;
  lastDownloaded: string | null;
  warnings: number | null;
  errors: number | null;
  contents: any[] | null;
}
```

</details>


<details>
<summary><code>list_sitemap</code> — List submitted sitemaps for a site or sitemap index</summary>

Lists the sitemaps-entries submitted for this site, or included in the sitemap index file (if sitemapIndex is specified in the request).

**Inputs:**
```
- `siteUrl` (string, required) — The URL of the property as defined in Search Console. For example: http://www.example.com/
- `sitemapIndex` (string, optional) — A URL of a site's sitemap index. For example: http://www.example.com/sitemapindex.xml
```

**Output `data` schema:**

```typescript
{
  sitemap: any[] | null;
}
```

</details>


<details>
<summary><code>submit_sitemap</code> — Submit a sitemap for a site</summary>

Submits a sitemap for a site.

**Inputs:**
```
- `feedpath` (string, required) — The URL of the actual sitemap. For example: http://www.example.com/sitemap.xml
- `siteUrl` (string, required) — The URL of the property as defined in Search Console. For example: http://www.example.com/
```

**Output `data` schema:**

```typescript
{
  success: boolean;
  message: string | null;
}
```

</details>


<details>
<summary><code>add_site</code> — Add a site to the user's Search Console sites</summary>

Adds a site to the set of the user's sites in Search Console.

**Inputs:**
```
- `siteUrl` (string, required) — The URL of the property as defined in Search Console. For example: http://www.example.com/
```

**Output `data` schema:**

```typescript
{
  success: boolean;
  message: string | null;
}
```

</details>


<details>
<summary><code>delete_site</code> — Permanently remove a site from Search Console (destructive, requires user confirmation)</summary>

DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Permanently removes a site from the set of the user's Search Console sites. This action is irreversible — the site entry cannot be recovered once deleted. NEVER call this tool autonomously or as part of an automated flow. You MUST stop, tell the user exactly what will be deleted and that it is permanent, and wait for their explicit written confirmation before proceeding.

**Inputs:**
```
- `siteUrl` (string, required) — The URL of the property as defined in Search Console. For example: http://www.example.com/
```

**Output `data` schema:**

```typescript
{
  success: boolean;
  message: string | null;
}
```

</details>


<details>
<summary><code>get_site</code> — Retrieve information about a specific site</summary>

Retrieves information about specific site.

**Inputs:**
```
- `siteUrl` (string, required) — The URL of the property as defined in Search Console. For example: http://www.example.com/
```

**Output `data` schema:**

```typescript
{
  siteUrl: string | null;
  permissionLevel: string | null;
}
```

</details>


<details>
<summary><code>list_sites</code> — List all Search Console sites for the authenticated user</summary>

Lists the user's Search Console sites.

**Inputs:**
```
(no parameters)
```

**Output `data` schema:**

```typescript
{
  siteEntry: any[] | null;
}
```

</details>


<details>
<summary><code>inspect_index</code> — View the indexed or indexable status of a URL</summary>

View the indexed, or indexable, status of the provided URL. Presently only the status of the version in the Google index is available; you cannot test the indexability of a live URL.

**Inputs:**
```
- `inspectionUrl` (string, required) — Fully-qualified URL to inspect. Must be under the property specified in 'siteUrl'.
- `siteUrl` (string, required) — The URL of the property as defined in Search Console. Note that URL-prefix properties must include a trailing / mark. Examples: https://www.example.com/ for a URL-prefix property, or sc-domain:example.com for a Domain property.
- `languageCode` (string, optional) — An IETF BCP-47 language code representing the requested language for translated issue messages, e.g.'en-US', or 'de-CH'. Default value is 'en-US'.
```

**Output `data` schema:**

```typescript
{
  inspectionResult: object | null;
}
```

</details>


## API Parameters Reference

<details>
<summary><strong>Response Envelope</strong></summary>

Every tool returns the same top-level envelope. Only `data` varies per tool.

```json
// Success
{
  "success": true,
  "statusCode": 200,
  "retriable": false,
  "retry_after_seconds": null,
  "error": null,
  "data": { ... }
}

// Error
{
  "success": false,
  "statusCode": 400,
  "retriable": false,
  "retry_after_seconds": null,
  "error": { "code": "{ERROR_CODE}", "message": "{description}", "details": {} },
  "data": null
}
```

- `retriable` — `true` when it is safe to retry (rate limit, network error, 503). `false` for validation and auth errors.
- `retry_after_seconds` — seconds to wait before retrying; present only when `retriable` is `true` and the upstream specifies a delay.
- `error.code` — machine-readable string: `VALIDATION_ERROR`, `AUTH_ERROR`, `UPSTREAM_ERROR`, `SERVER_ERROR`.

</details>

<details>
<summary><strong>Resource Formats</strong></summary>

**URL-prefix property:**

```
https://www.example.com/
Example: https://www.example.com/
```

**Domain property:**

```
sc-domain:{domain}
Example: sc-domain:example.com
```

**Sitemap URL:**

```
https://www.example.com/sitemap.xml
Example: https://www.example.com/sitemap.xml
```

</details>


## Authentication

This server uses OAuth. Pass the user's Google OAuth access token via the `Authorization: Bearer <token>` header on every request. The token must have the `https://www.googleapis.com/auth/webmasters` scope (read/write) or `https://www.googleapis.com/auth/webmasters.readonly` scope (read-only tools only).

The user must have verified ownership of the site in Search Console for the requested `siteUrl`.


## Troubleshooting

<details>
<summary><strong>Missing or Invalid Authorization Header</strong></summary>

- **Cause:** OAuth access token not provided or malformed
- **Solution:**
  1. Verify `Authorization: Bearer <oauth_access_token>` header is present on the request
  2. Ensure the token has not expired — Google OAuth access tokens typically expire after 1 hour
  3. Re-authenticate to obtain a fresh access token

</details>

<details>
<summary><strong>Insufficient Permissions</strong></summary>

- **Cause:** The authenticated user does not have access to the requested site property
- **Solution:**
  1. Verify the user has verified ownership of the `siteUrl` in Google Search Console
  2. Check that the OAuth token includes the required `webmasters` scope
  3. For read-only tools, `webmasters.readonly` scope is sufficient; write tools require `webmasters`

</details>

<details>
<summary><strong>Site Not Found</strong></summary>

- **Cause:** The `siteUrl` is not registered under the authenticated user's Search Console account
- **Solution:**
  1. Use `list_sites` to confirm the exact URL format registered in Search Console
  2. URL-prefix properties require a trailing slash (e.g. `https://www.example.com/`)
  3. Domain properties must use the `sc-domain:` prefix (e.g. `sc-domain:example.com`)

</details>

<details>
<summary><strong>Malformed Request Payload</strong></summary>

- **Cause:** JSON payload is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending
  2. Ensure all required tool parameters are included
  3. Check parameter types match expected values

</details>

<details>
<summary><strong>Google Search Console API Error</strong></summary>

- **Cause:** Upstream Google Search Console API returned an error
- **Solution:**
  1. Check Google service status at [Google Workspace Status Dashboard](https://www.google.com/appsstatus)
  2. Verify your credential has the required permissions for the requested operation
  3. Review the error message for specific details

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[Google Search Console API Documentation](https://developers.google.com/webmaster-tools/v1/api_reference_index)** — Official API reference
- **[Search Analytics API Reference](https://developers.google.com/webmaster-tools/v1/searchanalytics/query)** — Complete search analytics endpoint reference
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling

</details>
