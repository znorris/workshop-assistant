# Workshop Assistant Optimization Guide

*A practical guide to maximizing effectiveness with the workshop-assistant MCP server*

## Quick Start: Optimal System Prompts

### 🚀 Fast Development (12s avg response)
```
You are a Python expert. Respond with working code only, no explanations unless explicitly asked. Focus on the most pythonic and efficient solution.
```
**When to use**: Rapid prototyping, simple tasks, tight deadlines

### 🔍 Code Review (85s avg response)  
```
You are an expert code reviewer. Always analyze code for best practices, potential bugs, security issues, and performance optimizations. Provide detailed explanations of your recommendations.
```
**When to use**: Security audits, production code review, learning best practices

### 🏗️ Production Code (66s avg response)
```
You are a senior software engineer. Provide accurate, production-ready code solutions. Always use standard library when possible. Include error handling and document any assumptions. Prioritize code correctness over brevity.
```
**When to use**: Enterprise development, critical systems, maintainable codebases

### 📚 Learning & Workshops (87s avg response)
```
You are a workshop instructor helping developers learn step-by-step. Break down complex topics into digestible pieces. Always provide practical examples and encourage experimentation.
```
**When to use**: Teaching, onboarding, concept explanation, team workshops

### 🐛 Debugging (50s avg response)
```
You are a debugging specialist. When analyzing code or problems, think through the issue systematically: 1) Identify the problem, 2) Analyze root causes, 3) Propose solutions, 4) Suggest prevention strategies.
```
**When to use**: Complex bugs, system analysis, troubleshooting

## Performance Optimization Strategy

### Speed vs Quality Matrix
| Need | Prompt Type | Response Time | Use Case |
|------|-------------|---------------|----------|
| Maximum Speed | Code-Only Expert | ~12s | Quick prototypes, simple functions |
| Balanced | Debugging Specialist | ~50s | Most development tasks |
| High Quality | Production Engineer | ~66s | Critical business logic |
| Maximum Detail | Code Reviewer | ~85s | Security, compliance, learning |

### Efficiency Rules
1. **Start fast, refine later**: Use code-only prompts for initial development
2. **Batch related queries**: Keep the model loaded for sequential requests  
3. **Match prompt to task**: Don't use detailed prompts for simple tasks
4. **Consider context switching cost**: Model loading adds ~8.6s overhead

## Practical Workflows

### Development Phase Workflow
```
1. Exploration Phase → Code-Only Expert prompt
2. Implementation Phase → Production Engineer prompt  
3. Review Phase → Code Reviewer prompt
4. Documentation Phase → Workshop Instructor prompt
```

### Team Collaboration Workflow
```
1. Individual Development → Fast prompts
2. Pair Programming → Production prompts
3. Code Review → Reviewer prompts
4. Knowledge Sharing → Instructor prompts
```

## Common Scenarios & Solutions

### Scenario: "I need a quick function to solve X"
**Optimal Prompt**: Code-Only Expert
**Expected Response**: 12s, ~120 tokens, working code
**Follow-up**: If bugs found, switch to Debugging Specialist

### Scenario: "Review this code before production"
**Optimal Prompt**: Code Reviewer
**Expected Response**: 85s, ~480 tokens, comprehensive analysis
**Follow-up**: Use Production Engineer for fixes

### Scenario: "Explain this concept to my team"
**Optimal Prompt**: Workshop Instructor  
**Expected Response**: 87s, ~530 tokens, educational breakdown
**Follow-up**: Create documentation with structured examples

### Scenario: "Debug this complex issue"
**Optimal Prompt**: Debugging Specialist
**Expected Response**: 50s, ~450 tokens, systematic analysis
**Follow-up**: Use Production Engineer for implementation

## Advanced Techniques

### Prompt Chaining Strategy
1. **Start with exploration**: Use fast prompts to understand the problem
2. **Develop systematically**: Apply appropriate detailed prompts
3. **Validate thoroughly**: Use reviewer prompts for quality assurance
4. **Document clearly**: Use instructor prompts for team knowledge

### Context Management
- **Batch related queries** to avoid model reload overhead
- **Use consistent prompt styles** within a session
- **Switch prompts explicitly** when changing task types
- **Monitor response quality** and adjust prompts accordingly

### Quality Assurance
- **Test prompts with known scenarios** before critical use
- **Validate generated code** especially for security-sensitive functions
- **Cross-check with different prompt styles** for important decisions
- **Document successful prompt patterns** for team reuse

### Concurrent Execution Patterns

#### Parallel Development Template
```python
# Optimal: Batch related tasks to leverage model caching
async def parallel_development():
    # Start workshop-assistant on implementation
    implementation_task = mcp__workshop-assistant__chat_with_model(
        model_name="codellama:13b",
        prompt="Implement authentication middleware with JWT...",
        system_prompt="Senior backend engineer, production-ready code",
        verbose=True
    )
    
    # Concurrently, Claude writes tests and docs
    claude_tasks = [
        write_comprehensive_tests(),
        create_api_documentation(), 
        plan_integration_strategy()
    ]
    
    # Combine results
    return await asyncio.gather(implementation_task, *claude_tasks)
```

#### Multi-Perspective Analysis
```
Workshop Assistant (Technical Focus):
"You are a technical architect. Focus on implementation details, performance, and technical feasibility."

Claude (Business/UX Focus):  
While workshop-assistant analyzes technical aspects, Claude evaluates:
- User experience implications
- Business logic validation
- API design consistency
- Documentation quality
```

## Troubleshooting Guide

### Issue: Responses too slow
**Solution**: Switch to Code-Only Expert or Debugging Specialist prompts

### Issue: Responses lack detail
**Solution**: Use Code Reviewer or Production Engineer prompts

### Issue: Code has bugs/security issues
**Solution**: Always use Code Reviewer prompt for critical code paths

### Issue: Explanations too verbose
**Solution**: Add "be concise" or "code only" to your prompt

### Issue: Model suggests non-existent libraries
**Solution**: Add "use only standard library" to your prompt

## Best Practices Checklist

### Before Starting a Session
- [ ] Choose appropriate prompt based on task urgency/complexity
- [ ] Understand the speed/quality trade-off for your needs
- [ ] Plan to batch related queries together

### During Development
- [ ] Use fast prompts for exploration and iteration
- [ ] Switch to detailed prompts for critical components
- [ ] Validate generated code with appropriate review prompts
- [ ] Document successful prompt patterns

### For Team Use
- [ ] Establish standard prompts for different roles
- [ ] Share successful prompt patterns with team
- [ ] Use consistent prompt styles for similar tasks
- [ ] Train team members on prompt selection

## Measuring Success

### Speed Metrics
- Target <15s for rapid development tasks
- Target <60s for balanced development tasks
- Allow >60s only for comprehensive analysis tasks

### Quality Metrics
- Code compiles and runs without errors
- Security vulnerabilities identified and addressed
- Best practices followed (proper error handling, documentation)
- Solutions are maintainable and readable

## Summary

The workshop-assistant's effectiveness depends on strategic prompt selection:

1. **Match prompts to tasks** - Don't use detailed prompts for simple tasks
2. **Understand the trade-offs** - Speed vs quality is a conscious choice
3. **Develop workflows** - Different development phases need different prompts
4. **Measure and iterate** - Track what works for your specific use cases

By following this guide, you can achieve 10x performance improvements for rapid development while maintaining high quality for critical code paths.

## Quick Reference Card

```
Fast Development:     Code-Only Expert (12s)
Balanced Development: Debugging Specialist (50s)  
Production Quality:   Senior Engineer (66s)
Code Review:         Expert Reviewer (85s)
Learning/Teaching:   Workshop Instructor (87s)
```

Remember: The right prompt at the right time is the key to workshop-assistant mastery.