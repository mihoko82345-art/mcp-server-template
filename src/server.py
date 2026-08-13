#!/usr/bin/env python3
import os
from pathlib import Path
from fastmcp import FastMCP

mcp = FastMCP("Sample MCP Server")

import urllib.request

@mcp.tool(description="读取私密 GitHub 仓库中的 Markdown 文件")
def read_markdown(path: str) -> str:
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPO")
    branch = os.environ.get("GITHUB_BRANCH", "main")

    print("GitHub Repo:", repo)
    print("GitHub Branch:", branch)
    print("GitHub Path:", path)

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
        data = response.read().decode("utf-8")

        print("========== GITHUB RESPONSE ==========")
        print("GitHub Status:", response.status)
        print("GitHub Content Length:", len(data))
        print("GitHub Content Preview:", data[:300])
        print("=====================================")

        return data

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
    
@mcp.tool(description="读取服务器上的 Markdown 文件内容")
def read_markdown(file_path: str) -> str:
    path = Path(file_path)

    print("========== READ_MARKDOWN CALLED ==========")

    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPO")
    branch = os.environ.get("GITHUB_BRANCH", "main")

    print("GitHub Repo:", repo)
    print("GitHub Branch:", branch)
    print("GitHub Path:", path)

    if not token:
        return "错误：没有配置 GITHUB_TOKEN"

    if not repo:
        return "错误：没有配置 GITHUB_REPO"

    if not path.exists():
        return f"找不到文件：{file_path}"

    if not path.is_file():
        return f"这不是一个文件：{file_path}"

    if path.suffix.lower() != ".md":
        return "这里只允许读取 .md Markdown 文件"

    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        return f"读取文件失败：{e}"

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
