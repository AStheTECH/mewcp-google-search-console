"""Upstream API client for MewCP Google Search Console MCP Server."""

import logging

from fastmcp_credentials import get_credentials
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


logger = logging.getLogger("google-search-console-mcp.service")


def get_service():
    cred = get_credentials()
    if not cred.access_token:
        raise ValueError("No OAuth access token available in credentials")
    logger.info("Creating Google Search Console API service with provided access token")
    creds = Credentials(token=cred.access_token, scopes=cred.scopes)
    service = build("searchconsole", "v1", credentials=creds)
    logger.info("Google Search Console API service created successfully")
    return service
