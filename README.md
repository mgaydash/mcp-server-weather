# Weather MCP Server

A Model Context Protocol (MCP) server that provides weather data and forecasting capabilities using the [Open-Meteo API](https://open-meteo.com/en/docs).

## Overview

This project implements an MCP server that enables Claude Desktop to fetch current weather conditions and forecasts for any location. Built with Python and the FastMCP framework, it exposes weather data through tools that Claude can automatically invoke during conversations.

## Tutorial

This project follows the [Building MCP Servers for Claude Desktop tutorial](https://www.linkedin.com/learning/model-context-protocol-mcp-hands-on-with-agentic-ai/), demonstrating how to create custom MCP servers that extend Claude's capabilities with external data sources.

## Testing

- Run the application in dev mode with `mcp dev server.py`
- Use the MCP Inspector at `http://localhost:5173` to test tools and view responses interactively.