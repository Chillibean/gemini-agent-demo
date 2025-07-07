# Google Agent Workshop - Gemini API Integration

This workshop demonstrates how to build AI agents using Google's Gemini API.

## 🚀 Workshop Overview

Learn how to:
- Integrate Gemini API into your applications
- Build AI agents with Google ADK
- Deploy AI-powered services on Kubernetes
- Use environment variables for API configuration

## 📋 Prerequisites

- Docker installed
- Google Cloud account with Gemini API enabled
- Gemini API key (get from Google AI Studio)

## 🔧 Setup Instructions

### 1. Get Your Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Copy the key for use in the workshop

### 2. Running with Docker (Recommended for Workshop)

```bash
# Build the Docker image
docker build -t google-agent-demo .

# Run with Gemini API (Primary method)
docker run -p 4000:4000 \
    -e GEMINI_API_KEY=" < GEMINI_API_KEY >" \
    google-agent-demo


## 🧪 Testing the Agent

### Using curl

```bash
# Test the agent
curl -X POST "http://localhost:4000/agents/workshop_agent/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What time is it?",
    "session_id": "workshop-session-1"
  }'

# Get workshop info
curl -X POST "http://localhost:4000/agents/workshop_agent/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tell me about this workshop",
    "session_id": "workshop-session-1"
  }'
```

## 🔧 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GEMINI_API_KEY` | Your Gemini API key | Yes (for Gemini) | - |
| `MODEL_GEMINI` | Gemini model to use | No | `gemini/gemini-2.0-flash` |
| `GEMINI_BASE_URL` | Gemini API base URL | No | `https://generativelanguage.googleapis.com/v1beta/models` |
| `OPENAI_BASE_URL` | OpenAI-compatible base URL | Yes (for OpenAI) | - |
| `OPENAI_API_KEY` | OpenAI API key | Yes (for OpenAI) | - |


## 📚 Workshop Exercises

1. **Basic Integration**: Get the agent running with your Gemini API key
2. **Custom Tools**: Add a new tool function to the agent
3. **Model Comparison**: Try different Gemini models
4. **Kubernetes Deploy**: Deploy the agent to your EKS cluster
5. **ArgoCD Integration**: Set up GitOps deployment with ArgoCD

## 🔍 Troubleshooting

### Common Issues:

1. **API Key Issues**: Make sure your Gemini API key is valid and has proper permissions
2. **Model Not Found**: Ensure you're using a supported Gemini model name
3. **Docker Networking**: Use `host.docker.internal` for local services from Docker
4. **Port Conflicts**: Change the port if 4000 is already in use


## 🎯 Next Steps

- Explore more Gemini models
- Add custom business logic tools
- Integrate with your existing microservices
- Set up monitoring and logging
- Implement proper authentication

## 📖 Additional Resources

- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Google ADK Documentation](https://cloud.google.com/agent-framework)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/)
