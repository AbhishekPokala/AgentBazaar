# Python Locus Application

A sample Python application that connects to Locus MCP server using Claude SDK.

## Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create a `.env` file** in this directory with your API keys:
   ```
   LOCUS_API_KEY=your_locus_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

4. **Test MCP connection (optional):**
   ```bash
   python mcp_example.py
   ```

## Features

- ✅ Claude API integration
- ✅ Environment variable configuration
- ✅ Basic API connection testing
- ✅ Locus MCP server configuration
- ✅ Sample queries to Claude

## Project Structure

- `main.py` - Main application file with Claude API integration
- `mcp_example.py` - Example MCP server connection test
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (create this file)
- `README.md` - This file

## Next Steps

For full MCP integration, you may want to:
- Install MCP Python client library
- Implement MCP protocol handlers
- Connect to Locus MCP server endpoints
- Use Locus tools and resources

## Learn More

- [Locus Documentation](https://docs.paywithlocus.com)
- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python)
- [MCP Protocol](https://modelcontextprotocol.io)

---

Built with Locus 🎯

