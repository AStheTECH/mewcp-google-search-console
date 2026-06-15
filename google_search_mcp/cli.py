import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Google MCP Server")
    parser.add_argument(
        "-t",
        "--transport",
        help="Transport method for MCP (Allowed Values: 'stdio', 'sse', or 'streamable-http')",
        default="streamable-http",
    )
    parser.add_argument("--host", help="Host to bind the server to", default=None)
    parser.add_argument(
        "--port", type=int, help="Port to bind the server to", default=None
    )
    return parser.parse_args()
