#! /usr/bin/env python3
# script to fetch Matt Levine's Money Stuff article URLs from Bloomberg.
# Sample usage:
# rajulocal@hogwarts ~/work/github/market_data/money_stuff_urls
#  % $market_data_processor/src/scripts/money_stuff_urls.py --page 1 > 1.txt
import sys

import requests
import pandas as pd
import typer
from pathlib import Path

import project_root
from src.utils.DataFrameUtils import to_fwf

# If you do
#   app = typer.Typer()
# help is printed only for --help. But I want help to be printed for
# both -h and --help.
app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})

BASE_URL = (
    "https://www.bloomberg.com/lineup-next/api/author/ARbTQlRLRjE/matthew-s-levine"
)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}


def load_cookies(cookies_file: Path) -> dict:
    with open(cookies_file) as f:
        cookie_str = f.read().strip()
        cookie_str = "\n".join(
            line for line in cookie_str.splitlines() if not line.startswith("#")
        )
    cookies = dict(item.split("=", 1) for item in cookie_str.split("; "))
    return cookies


# Cookies are read from cookies/bloomberg.txt in the project root (not committed to git)
# See cookies/bloomberg.txt.example for instructions on how to get your
cookies_file = (
    Path(__file__).parent.parent.parent / "config" / "cookies" / "bloomberg.txt"
)
cookies = load_cookies(cookies_file)


def fetch_articles(
    page: int, cookies: dict, headers: dict, cookies_file: Path
) -> pd.DataFrame:
    # Ex:- If page is 3, this will fetch
    # https://www.bloomberg.com/lineup-next/api/author/ARbTQlRLRjE/matthew-s-levine?pageNumber=3

    response = requests.get(
        BASE_URL, params={"pageNumber": page}, cookies=cookies, headers=headers
    )
    if response.status_code == 403:
        print("Request failed. Maybe cookies are outdated or invalid.", file=sys.stderr)
        print(f"Try updating your cookies in {cookies_file}", file=sys.stderr)
        print(
            f"See {cookies_file}.example for instructions on how to get your cookies.",
            file=sys.stderr,
        )
        raise typer.Exit(code=1)
    response.raise_for_status()

    data = response.json()
    # Use https://jsonformatter.org/ to pretty print and to analyze this json.
    items = data.get("items", [])

    rows = []
    for item in items:
        rows.append(
            {
                "publishedAt": item["publishedAt"],
                "url": item["raw"]["url"],
                "headline": item["headline"],
            }
        )
    df = pd.DataFrame(rows)
    df["publishedAt"] = pd.to_datetime(df["publishedAt"])
    df = df.sort_values("publishedAt")
    df["publishedAt"] = df["publishedAt"].dt.date
    return df


@app.command()
def main(page: int = typer.Option(default=1, help="Page number to fetch")):
    """Fetch Matt Levine's Money Stuff article URLs from Bloomberg."""
    df = fetch_articles(page, cookies, headers, cookies_file)
    pd.set_option("display.max_colwidth", None)
    pd.set_option("display.max_rows", None)
    # print(df.to_string(index=False, justify="left"))
    df.to_fwf(sys.stdout, index=False)


if __name__ == "__main__":
    app()
