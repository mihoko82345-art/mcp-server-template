#!/usr/bin/env python3
import os
import urllib.request
from fastmcp import FastMCP

mcp = FastMCP("Sample MCP Server")

import urllib.request

@mcp.tool(description="读取私密 GitHub 仓库中的 Markdown 文件")
def read_markdown(path: str) -> str:
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPO")
    branch = os.environ.get("GITHUB_BRANCH", "main")

    if not token:
        return "错误：没有配置 GITHUB_TOKEN"

    if not repo:
        return "错误：没有配置 GITHUB_REPO"

    url = f"https://api.github.com/repos/{repo}/contents/{path}?ref={branch}"

    print("GitHub读取地址：", url)

    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.raw+json",
            "User-Agent": "mcp-markdown-reader"
        }
    )

    try:
    with urllib.request.urlopen(request) as response:
        content = response.read().decode("utf-8")

        print("GitHub Status:", response.status)
        print("GitHub Content Length:", len(content))
        print("GitHub Content Preview:", content[:300])

        return content

except Exception as e:
    print("========== GITHUB READ ERROR ==========")
    print("Error:", repr(e))
    print("=======================================")
    return f"读取 Markdown 失败：{e}"

@mcp.tool(description="Greet a user by name with a welcome message from the MCP server")
def greet(name: str) -> str:
    return f"Hello, {name}! Welcome to our sample MCP server running on Heroku!"

@mcp.tool(description="Get information about the MCP server including name, version, environment, and Python version")
def get_server_info() -> dict:
    return {
        "server_name": "Sample MCP Server",
        "version": "1.0.0",
        "environment": os.environ.get("ENVIRONMENT", "development"),
        "python_version": os.sys.version.split()[0]
    }
@mcp.tool(description="测试工具")
def test() -> str:
    return "成功啦！"
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    
    print(f"Starting FastMCP server on {host}:{port}")
    
    mcp.run(
        transport="http",
        host=host,
        port=port,
        stateless_http=True
    )
