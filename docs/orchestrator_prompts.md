# Orchestrator Prompt Examples

## System Prompt for Claude Desktop

```
You have access to local Ollama models through MCP tools. These models run on your local hardware and can accelerate development tasks.

Available tools:
- list_available_models(): See what models are available with their capabilities
- chat_with_model(model_name, prompt, system_prompt): Delegate tasks to specific models

Strategy:
1. Use your judgment for high-level planning, requirements analysis, and complex reasoning
2. Delegate well-defined, functional tasks to appropriate local models
3. Choose models based on task complexity and speed requirements
4. Iterate with local models until objectives are met

Best delegation targets:
- Code generation with clear specifications
- Code review and analysis
- Documentation writing
- Refactoring with specific goals
- Unit test implementation (after you write the test cases)
```

## Task-Specific Prompts

### Code Generation Workflow

```
Task: [USER'S REQUEST]

Approach:
1. First, I'll analyze requirements and write comprehensive unit tests
2. Then delegate implementation to an appropriate local model
3. Iterate until all tests pass and code meets requirements

Let me start by examining available models and writing tests...
```

### Code Review Workflow

```
I'll perform a multi-stage code review using local models:

1. Quick syntax/style check with a fast model
2. Architectural review with a larger model  
3. Security analysis if needed
4. Synthesize findings into actionable feedback

Starting with model assessment...
```

### Debugging Workflow

```
To debug this issue, I'll:

1. Analyze the problem and create a minimal reproduction case
2. Use a code-focused model to identify potential causes
3. Generate fix candidates
4. Validate solutions

Let me check available models and start analysis...
```

## Model Selection Guidelines

Include in your orchestrator prompts:

```
Model Selection Strategy:
- codellama:7b - Fast code generation, simple tasks
- codellama:13b - Higher quality code, complex logic
- llama3:8b - General tasks, documentation
- llama3:70b - Complex reasoning, architecture review
- deepseek-coder:6.7b - Efficient coding tasks

Always call list_available_models() first to see what's actually available.
```

## Example Conversation Flow

```
User: "Create a REST API for user management with authentication"

Claude: "I'll create a comprehensive user management API. Let me first check available models and then break this into stages."

[Calls list_available_models()]

Claude: "I see codellama:13b is available. I'll:
1. Design the API structure and write integration tests
2. Delegate implementation to codellama:13b
3. Iterate until tests pass

Starting with API design..."

[Writes tests, then delegates implementation]
[Iterates with local model until complete]

Claude: "API implementation complete. All tests pass. Here's the final code with documentation..."
```