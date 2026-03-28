"""
MCP server exposing code analysis tools to the review agents.
Run standalone: python mcp_server.py
"""
import ast
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import mcp.server.stdio
import mcp.types as types
from mcp.server import Server

server = Server("code-review-tools")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="detect_language",
            description="Detect programming language from code snippet",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {"type": "string"},
                    "filename": {"type": "string", "default": ""},
                },
                "required": ["code"],
            },
        ),
        types.Tool(
            name="lint_python",
            description="Run pyflakes lint on Python code, returns issues",
            inputSchema={
                "type": "object",
                "properties": {"code": {"type": "string"}},
                "required": ["code"],
            },
        ),
        types.Tool(
            name="parse_python_ast",
            description="Parse Python AST and return structural summary",
            inputSchema={
                "type": "object",
                "properties": {"code": {"type": "string"}},
                "required": ["code"],
            },
        ),
        types.Tool(
            name="count_complexity",
            description="Count cyclomatic complexity indicators in code",
            inputSchema={
                "type": "object",
                "properties": {"code": {"type": "string"}},
                "required": ["code"],
            },
        ),
        types.Tool(
            name="run_python_safe",
            description="Run small Python snippet in subprocess with 5s timeout",
            inputSchema={
                "type": "object",
                "properties": {"code": {"type": "string"}},
                "required": ["code"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    code = arguments.get("code", "")

    if name == "detect_language":
        filename = arguments.get("filename", "")
        lang = _detect_language(code, filename)
        return [types.TextContent(type="text", text=lang)]

    elif name == "lint_python":
        result = _lint_python(code)
        return [types.TextContent(type="text", text=result)]

    elif name == "parse_python_ast":
        result = _parse_ast(code)
        return [types.TextContent(type="text", text=result)]

    elif name == "count_complexity":
        result = _count_complexity(code)
        return [types.TextContent(type="text", text=json.dumps(result))]

    elif name == "run_python_safe":
        result = _run_python(code)
        return [types.TextContent(type="text", text=result)]

    return [types.TextContent(type="text", text="Unknown tool")]


def _detect_language(code: str, filename: str) -> str:
    ext_map = {
        ".py": "python", ".js": "javascript", ".ts": "typescript",
        ".java": "java", ".go": "go", ".rs": "rust", ".cpp": "cpp",
        ".c": "c", ".cs": "csharp", ".rb": "ruby", ".php": "php",
    }
    if filename:
        for ext, lang in ext_map.items():
            if filename.endswith(ext):
                return lang
    # Heuristics
    if "def " in code and "import " in code:
        return "python"
    if "function " in code or "const " in code or "let " in code:
        return "javascript"
    if "public class" in code or "System.out" in code:
        return "java"
    if "fn " in code and "let mut" in code:
        return "rust"
    if "func " in code and "package " in code:
        return "go"
    return "unknown"


def _lint_python(code: str) -> str:
    try:
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write(code)
            tmp = f.name
        result = subprocess.run(
            [sys.executable, "-m", "pyflakes", tmp],
            capture_output=True, text=True, timeout=10
        )
        output = result.stdout + result.stderr
        return output.replace(tmp, "<code>") if output.strip() else "No lint issues found."
    except Exception as e:
        return f"Lint error: {e}"


def _parse_ast(code: str) -> str:
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return f"SyntaxError: {e}"

    functions, classes, imports = [], [], []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            args = [a.arg for a in node.args.args]
            functions.append(f"{node.name}({', '.join(args)}) at line {node.lineno}")
        elif isinstance(node, ast.ClassDef):
            classes.append(f"{node.name} at line {node.lineno}")
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(ast.dump(node)[:60])

    lines = [f"Lines: {len(code.splitlines())}"]
    if classes:
        lines.append(f"Classes: {', '.join(classes)}")
    if functions:
        lines.append(f"Functions: {'; '.join(functions)}")
    if imports:
        lines.append(f"Imports: {len(imports)} found")
    return "\n".join(lines)


def _count_complexity(code: str) -> dict:
    keywords = ["if ", "elif ", "else:", "for ", "while ", "try:", "except ", "with "]
    counts = {kw.strip(": "): code.count(kw) for kw in keywords}
    counts["total_branches"] = sum(counts.values())
    counts["lines"] = len(code.splitlines())
    return counts


def _run_python(code: str) -> str:
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True, text=True, timeout=5
        )
        out = result.stdout[:500] if result.stdout else ""
        err = result.stderr[:300] if result.stderr else ""
        return f"stdout:\n{out}\nstderr:\n{err}" if (out or err) else "No output."
    except subprocess.TimeoutExpired:
        return "Execution timed out (5s limit)."
    except Exception as e:
        return f"Execution error: {e}"


if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server

    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options(),
            )

    asyncio.run(main())