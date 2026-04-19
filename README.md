# DispatcherIQ - Agentic AI Application

A production-ready starter template for building agentic AI applications using **FastAPI**, **Langchain**, and **Langgraph**.

## 🎯 Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **Langgraph**: State-based agent orchestration with conversation memory
- **Langchain**: LLM integration and tool management
- **Async Support**: Full async/await support for non-blocking I/O
- **Tool Integration**: Easy-to-extend tool system for agents
- **Error Handling**: Robust error handling and logging
- **CORS Support**: Pre-configured CORS middleware

## 📁 Project Structure

```
DispatcherIQ/
├── app/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   └── graph_agent.py          # Langgraph agent implementation
│   ├── tools/
│   │   ├── __init__.py
│   │   └── base_tools.py           # Tool definitions
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── models.py               # Pydantic models
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py             # Configuration & env vars
│   └── utils/
│       ├── __init__.py
│       └── logging_utils.py        # Logging setup
├── main.py                         # FastAPI app entry point
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
└── README.md                       # This file
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
cd c:\Users\Abhishek\PROJECTS\DispatcherIQ
python -m venv venv
venv\Scripts\activate  # On Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy the example env file
copy .env.example .env

# Edit .env and add your API keys
# OPENAI_API_KEY=your_key_here
```

### 4. Run the Application

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## 📚 API Endpoints

### Health Check
```bash
GET /health
```

### Chat with Agent
```bash
POST /agent/chat
Content-Type: application/json

{
  "query": "What is 2 + 2?",
  "conversation_history": [
    {
      "role": "user",
      "content": "Hello"
    },
    {
      "role": "assistant",
      "content": "Hi there!"
    }
  ],
  "metadata": {}
}
```

### Stream Agent Response
```bash
POST /agent/stream
Content-Type: application/json

{
  "query": "Your query here",
  "conversation_history": [],
  "metadata": {}
}
```

## 🛠️ Customization

### Adding New Tools

Edit `app/tools/base_tools.py`:

```python
@tool
def my_custom_tool(input_param: str) -> str:
    """Description of what the tool does"""
    return f"Result: {input_param}"

def get_tools() -> List:
    return [
        search_tool,
        calculate_tool,
        my_custom_tool,  # Add your tool here
    ]
```

### Adding New Agents

Create a new file in `app/agents/`:

```python
def create_specialized_agent():
    """Create a specialized agent for specific tasks"""
    # Implementation here
    pass
```

### Modifying the Prompt

Edit `app/agents/graph_agent.py` and update the `ChatPromptTemplate`:

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "Your custom system prompt here"),
    MessagesPlaceholder(variable_name="messages"),
])
```

## 🔧 Configuration

Edit `app/config/settings.py` or `.env` file to configure:

- **LLM Provider**: OpenAI, Anthropic, Cohere, etc.
- **Model Name**: Specify which model to use
- **Temperature**: Control response randomness (0-1)
- **Debug Mode**: Enable verbose logging
- **Checkpointer Type**: Memory or persistent storage

## 📖 Using with Different LLM Providers

### OpenAI (Default)
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(api_key=settings.openai_api_key, model="gpt-4")
```

### Anthropic
```bash
pip install langchain-anthropic
```
```python
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(api_key=settings.anthropic_api_key, model="claude-3-opus-20240229")
```

## 🧪 Development

### Run with Auto-reload
```bash
python main.py  # Debug mode auto-enabled in settings
```

### Interactive API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🚢 Production Deployment

1. Set `DEBUG=False` in `.env`
2. Use a production ASGI server:
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

3. Use environment variables for sensitive data
4. Set up proper logging and monitoring
5. Consider using a persistent checkpointer (PostgreSQL, Redis)

## 📝 Logging

Logs are written to both console and `app.log` file. Configure in `app/utils/logging_utils.py`.

## 🤝 Contributing

Feel free to extend and customize this template for your use case!

## 📄 License

MIT License

## 🆘 Troubleshooting

### ModuleNotFoundError
Ensure virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

### API Key Issues
Check that your `.env` file has the correct API key:
```bash
cat .env  # Verify your setup
```

### Agent Not Responding
Check logs in `app.log` for detailed error messages.

---

**Happy building with DispatcherIQ!** 🚀
