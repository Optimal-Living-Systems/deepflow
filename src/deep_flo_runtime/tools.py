"""Custom tools for Deep Flo."""

from __future__ import annotations

from collections.abc import Callable
from typing import Literal

import httpx
from ddgs import DDGS
from langchain_core.tools import BaseTool, tool
from markdownify import markdownify as html_to_markdown

from deep_flo_runtime.config import DeepFloSettings


def create_runtime_tools(settings: DeepFloSettings) -> list[BaseTool | Callable]:
    """Build the custom toolset for the research runtime."""
    return [
        make_web_search_tool(settings),
        make_fetch_url_tool(settings),
        make_search_openalex_tool(settings),
        make_search_semantic_scholar_tool(settings),
    ]


def make_web_search_tool(settings: DeepFloSettings) -> BaseTool:
    """Create a web search tool with Tavily and DDGS fallback."""

    @tool
    def web_search(
        query: str,
        max_results: int = 5,
        topic: Literal["general", "news"] = "general",
    ) -> str:
        """Search the web for current information."""
        if settings.provider_status()["tavily"]:
            from tavily import TavilyClient

            client = TavilyClient()
            result = client.search(query=query, max_results=max_results, topic=topic)
            rows = []
            for item in result.get("results", []):
                rows.append(
                    "\n".join(
                        [
                            f"Title: {item.get('title', '')}",
                            f"URL: {item.get('url', '')}",
                            f"Content: {item.get('content', '')}",
                        ]
                    )
                )
            return "\n\n".join(rows) or "No search results returned."

        rows = []
        with DDGS() as client:
            for item in client.text(query, max_results=max_results):
                rows.append(
                    "\n".join(
                        [
                            f"Title: {item.get('title', '')}",
                            f"URL: {item.get('href', '')}",
                            f"Content: {item.get('body', '')}",
                        ]
                    )
                )
        return "\n\n".join(rows) or "No search results returned."

    return web_search


def make_fetch_url_tool(settings: DeepFloSettings) -> BaseTool:
    """Create a URL fetcher that returns markdown text."""

    @tool
    def fetch_url(url: str) -> str:
        """Fetch a URL and return the page as markdown-like text."""
        headers = {"User-Agent": settings.user_agent}
        with httpx.Client(timeout=settings.request_timeout_seconds, headers=headers, follow_redirects=True) as client:
            response = client.get(url)
            response.raise_for_status()
        content_type = response.headers.get("content-type", "")
        if "html" in content_type:
            return html_to_markdown(response.text)
        return response.text

    return fetch_url


def make_search_openalex_tool(settings: DeepFloSettings) -> BaseTool:
    """Create an OpenAlex academic search tool (free, no API key required)."""

    @tool
    def search_openalex(
        query: str,
        max_results: int = 20,
        from_year: int | None = None,
        open_access_only: bool = False,
    ) -> str:
        """Search OpenAlex for peer-reviewed academic papers.

        Returns structured bibliography entries with title, authors, year, DOI,
        abstract, and open access status. Best for sociology and social science coverage.
        """
        params: dict[str, str | int] = {
            "search": query,
            "per_page": min(max_results, 50),
            "select": "id,title,authorships,publication_year,doi,abstract_inverted_index,open_access,primary_location,cited_by_count",
            "mailto": "research@optimalliving.systems",
        }
        if from_year:
            params["filter"] = f"publication_year:>{from_year - 1}"
        if open_access_only:
            existing = str(params.get("filter", ""))
            params["filter"] = (existing + ",open_access.is_oa:true").lstrip(",")

        headers = {"User-Agent": settings.user_agent}
        with httpx.Client(timeout=settings.request_timeout_seconds, headers=headers) as client:
            response = client.get("https://api.openalex.org/works", params=params)
            response.raise_for_status()

        data = response.json()
        results = data.get("results", [])
        if not results:
            return "No results found on OpenAlex for this query."

        entries = []
        for work in results:
            title = work.get("title") or "Unknown Title"
            year = work.get("publication_year") or "n.d."
            doi = work.get("doi") or ""
            cited_by = work.get("cited_by_count", 0)
            oa_info = work.get("open_access") or {}
            is_oa = oa_info.get("is_oa", False)
            oa_url = oa_info.get("oa_url") or ""

            authors = []
            for authorship in (work.get("authorships") or [])[:5]:
                author = (authorship.get("author") or {}).get("display_name") or ""
                if author:
                    authors.append(author)
            authors_str = ", ".join(authors) or "Unknown Authors"

            # Reconstruct abstract from inverted index
            abstract = ""
            inv_index = work.get("abstract_inverted_index") or {}
            if inv_index:
                word_positions: list[tuple[int, str]] = []
                for word, positions in inv_index.items():
                    for pos in positions:
                        word_positions.append((pos, word))
                word_positions.sort()
                abstract = " ".join(w for _, w in word_positions)[:300]

            entry_lines = [
                f"**{title}**",
                f"Authors: {authors_str}",
                f"Year: {year}",
            ]
            if doi:
                entry_lines.append(f"DOI: {doi}")
            if oa_url:
                entry_lines.append(f"Open Access: {oa_url}")
            else:
                entry_lines.append(f"Open Access: {'Yes' if is_oa else 'No'}")
            entry_lines.append(f"Cited by: {cited_by}")
            if abstract:
                entry_lines.append(f"Abstract: {abstract}...")
            entry_lines.append("Source: OpenAlex")
            entries.append("\n".join(entry_lines))

        return f"Found {len(results)} results on OpenAlex:\n\n" + "\n\n---\n\n".join(entries)

    return search_openalex


def make_search_semantic_scholar_tool(settings: DeepFloSettings) -> BaseTool:
    """Create a Semantic Scholar academic search tool (free, rate-limited)."""

    @tool
    def search_semantic_scholar(
        query: str,
        max_results: int = 20,
        from_year: int | None = None,
        open_access_only: bool = False,
    ) -> str:
        """Search Semantic Scholar for academic papers.

        Returns structured bibliography entries with title, authors, year, DOI,
        abstract, and open access status. Good for interdisciplinary and CS coverage.
        """
        params: dict[str, str | int] = {
            "query": query,
            "limit": min(max_results, 100),
            "fields": "title,authors,year,externalIds,abstract,isOpenAccess,openAccessPdf,citationCount",
        }
        if from_year:
            params["year"] = f"{from_year}-"
        if open_access_only:
            params["openAccessPdf"] = ""  # presence filters to OA

        headers = {
            "User-Agent": settings.user_agent,
        }
        with httpx.Client(timeout=settings.request_timeout_seconds, headers=headers) as client:
            response = client.get(
                "https://api.semanticscholar.org/graph/v1/paper/search",
                params=params,
            )
            if response.status_code == 429:
                return "Semantic Scholar rate limit reached. Try again in 60 seconds or use OpenAlex instead."
            response.raise_for_status()

        data = response.json()
        papers = data.get("data", [])
        if not papers:
            return "No results found on Semantic Scholar for this query."

        entries = []
        for paper in papers:
            title = paper.get("title") or "Unknown Title"
            year = paper.get("year") or "n.d."
            external_ids = paper.get("externalIds") or {}
            doi = external_ids.get("DOI") or ""
            cited_by = paper.get("citationCount", 0)
            is_oa = paper.get("isOpenAccess", False)
            oa_pdf = (paper.get("openAccessPdf") or {}).get("url") or ""

            authors = []
            for author in (paper.get("authors") or [])[:5]:
                name = author.get("name") or ""
                if name:
                    authors.append(name)
            authors_str = ", ".join(authors) or "Unknown Authors"

            abstract = (paper.get("abstract") or "")[:300]

            entry_lines = [
                f"**{title}**",
                f"Authors: {authors_str}",
                f"Year: {year}",
            ]
            if doi:
                entry_lines.append(f"DOI: {doi}")
            if oa_pdf:
                entry_lines.append(f"Open Access PDF: {oa_pdf}")
            else:
                entry_lines.append(f"Open Access: {'Yes' if is_oa else 'No'}")
            entry_lines.append(f"Cited by: {cited_by}")
            if abstract:
                entry_lines.append(f"Abstract: {abstract}...")
            entry_lines.append("Source: Semantic Scholar")
            entries.append("\n".join(entry_lines))

        total = data.get("total", len(papers))
        return f"Found {total} total results on Semantic Scholar (showing {len(papers)}):\n\n" + "\n\n---\n\n".join(entries)

    return search_semantic_scholar
