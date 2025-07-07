import os
import datetime
import json
import subprocess
from typing import Dict, Any
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# Environment variables
gemini_api_key = os.environ.get("GEMINI_API_KEY", "")

def get_current_time() -> Dict[str, Any]:
    """Get the current time."""
    now = datetime.datetime.now()
    return {
        "status": "success",
        "report": f"The current time is {now.strftime('%Y-%m-%d %H:%M:%S')}",
    }

def get_workshop_info() -> Dict[str, Any]:
    """Get information about this workshop."""
    return {
        "status": "success",
        "report": "This workshop demonstrates AI agent integration for Ruby developers and platform engineers. Learn how to integrate Gemini API into Ruby applications, CI/CD pipelines, and Kubernetes deployments.",
    }

def analyze_ruby_code() -> Dict[str, Any]:
    """Provide Ruby code analysis and best practices."""
    return {
        "status": "success",
        "report": """Ruby Code Integration Patterns:

1. **Ruby Gem Integration**:
   ```ruby
   # Gemfile
   gem 'faraday', '~> 2.0'
   gem 'json', '~> 2.0'

   # lib/ai_agent_client.rb
   class AIAgentClient
     def initialize(api_key)
       @api_key = api_key
       @base_url = "http://ai-agent-service:4000"
     end

     def chat(message, session_id = SecureRandom.uuid)
       response = connection.post('/agents/workshop_agent/chat') do |req|
         req.headers['Content-Type'] = 'application/json'
         req.body = { message: message, session_id: session_id }.to_json
       end
       JSON.parse(response.body)
     end

     private

     def connection
       @connection ||= Faraday.new(url: @base_url)
     end
   end
   ```

2. **Rails Integration**:
   ```ruby
   # app/services/ai_assistant_service.rb
   class AIAssistantService
     include HTTParty
     base_uri ENV.fetch('AI_AGENT_URL', 'http://localhost:4000')

     def self.get_help(user_question)
       response = post('/agents/workshop_agent/chat', {
         body: { message: user_question, session_id: SecureRandom.uuid }.to_json,
         headers: { 'Content-Type' => 'application/json' }
       })
       response.parsed_response
     end
   end
   ```""",
    }

def cicd_integration_guide() -> Dict[str, Any]:
    """Provide CI/CD integration patterns for Ruby applications."""
    return {
        "status": "success",
        "report": """CI/CD Integration Patterns:

1. **GitHub Actions for Ruby + AI Agent**:
   ```yaml
   # .github/workflows/deploy-with-ai.yml
   name: Deploy Ruby App with AI Agent
   on:
     push:
       branches: [main]

   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - uses: ruby/setup-ruby@v1
           with:
             ruby-version: 3.2
             bundler-cache: true
         - run: bundle exec rspec

     deploy-ai-agent:
       needs: test
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - name: Deploy AI Agent
           run: |
             kubectl apply -f k8s/ai-agent-deployment.yaml
             kubectl set env deployment/ai-agent GEMINI_API_KEY=${{ secrets.GEMINI_API_KEY }}

     deploy-ruby-app:
       needs: deploy-ai-agent
       runs-on: ubuntu-latest
       steps:
         - name: Deploy Ruby App
           run: |
             kubectl apply -f k8s/ruby-app-deployment.yaml
             kubectl set env deployment/ruby-app AI_AGENT_URL=http://ai-agent-service:4000
   ```

2. **GitLab CI for Ruby + AI**:
   ```yaml
   # .gitlab-ci.yml
   stages:
     - test
     - build
     - deploy

   test:
     stage: test
     image: ruby:3.2
     script:
       - bundle install
       - bundle exec rspec

   deploy_ai_agent:
     stage: deploy
     script:
       - helm upgrade --install ai-agent ./helm/ai-agent
         --set gemini.apiKey=$GEMINI_API_KEY
         --set image.tag=$CI_COMMIT_SHA

   deploy_ruby_app:
     stage: deploy
     script:
       - helm upgrade --install ruby-app ./helm/ruby-app
         --set aiAgent.url=http://ai-agent-service:4000
   ```""",
    }

def kubernetes_deployment_guide() -> Dict[str, Any]:
    """Provide Kubernetes deployment patterns for Ruby apps with AI agents."""
    return {
        "status": "success",
        "report": """Kubernetes Deployment Patterns:

1. **AI Agent Service Deployment**:
   ```yaml
   # k8s/ai-agent-deployment.yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: ai-agent
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: ai-agent
     template:
       metadata:
         labels:
           app: ai-agent
       spec:
         containers:
         - name: agent
           image: your-registry/ai-agent:latest
           ports:
           - containerPort: 4000
           env:
           - name: GEMINI_API_KEY
             valueFrom:
               secretKeyRef:
                 name: ai-secrets
                 key: gemini-api-key
           resources:
             requests:
               memory: "256Mi"
               cpu: "250m"
             limits:
               memory: "512Mi"
               cpu: "500m"
   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: ai-agent-service
   spec:
     selector:
       app: ai-agent
     ports:
     - port: 4000
       targetPort: 4000
   ```

2. **Ruby App Deployment with AI Integration**:
   ```yaml
   # k8s/ruby-app-deployment.yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: ruby-app
   spec:
     replicas: 2
     selector:
       matchLabels:
         app: ruby-app
     template:
       metadata:
         labels:
           app: ruby-app
       spec:
         containers:
         - name: app
           image: your-registry/ruby-app:latest
           ports:
           - containerPort: 3000
           env:
           - name: AI_AGENT_URL
             value: "http://ai-agent-service:4000"
           - name: RAILS_ENV
             value: "production"
   ```""",
    }

def helm_chart_patterns() -> Dict[str, Any]:
    """Provide Helm chart patterns for Ruby + AI deployment."""
    return {
        "status": "success",
        "report": """Helm Chart Patterns:

1. **AI Agent Helm Chart Structure**:
   ```
   charts/ai-agent/
   ├── Chart.yaml
   ├── values.yaml
   ├── templates/
   │   ├── deployment.yaml
   │   ├── service.yaml
   │   ├── secret.yaml
   │   └── ingress.yaml
   ```

2. **values.yaml for AI Agent**:
   ```yaml
   # charts/ai-agent/values.yaml
   replicaCount: 3

   image:
     repository: your-registry/ai-agent
     tag: latest
     pullPolicy: IfNotPresent

   gemini:
     apiKey: ""  # Set via --set or CI/CD

   service:
     type: ClusterIP
     port: 4000

   ingress:
     enabled: true
     annotations:
       kubernetes.io/ingress.class: nginx
       cert-manager.io/cluster-issuer: letsencrypt-prod
     hosts:
       - host: ai-agent.yourdomain.com
         paths:
           - path: /
             pathType: Prefix

   resources:
     limits:
       cpu: 500m
       memory: 512Mi
     requests:
       cpu: 250m
       memory: 256Mi

   autoscaling:
     enabled: true
     minReplicas: 2
     maxReplicas: 10
     targetCPUUtilizationPercentage: 80
   ```

3. **ArgoCD Application**:
   ```yaml
   # argocd/ai-agent-app.yaml
   apiVersion: argoproj.io/v1alpha1
   kind: Application
   metadata:
     name: ai-agent
     namespace: argocd
   spec:
     project: default
     source:
       repoURL: https://github.com/your-org/ai-agent-charts
       targetRevision: main
       path: charts/ai-agent
       helm:
         valueFiles:
         - values.yaml
         parameters:
         - name: image.tag
           value: $ARGOCD_APP_REVISION
     destination:
       server: https://kubernetes.default.svc
       namespace: production
     syncPolicy:
       automated:
         prune: true
         selfHeal: true
   ```""",
    }

def ruby_testing_patterns() -> Dict[str, Any]:
    """Provide testing patterns for Ruby apps with AI integration."""
    return {
        "status": "success",
        "report": """Testing Patterns for Ruby + AI:

1. **RSpec Tests with AI Agent Mocking**:
   ```ruby
   # spec/services/ai_assistant_service_spec.rb
   RSpec.describe AIAssistantService do
     let(:mock_response) do
       {
         'response' => 'AI generated response',
         'session_id' => 'test-session-123'
       }
     end

     before do
       stub_request(:post, "#{ENV['AI_AGENT_URL']}/agents/workshop_agent/chat")
         .to_return(status: 200, body: mock_response.to_json)
     end

     it 'returns AI response' do
       result = AIAssistantService.get_help('What time is it?')
       expect(result['response']).to eq('AI generated response')
     end
   end
   ```

2. **Integration Tests**:
   ```ruby
   # spec/integration/ai_integration_spec.rb
   RSpec.describe 'AI Integration', type: :request do
     context 'when AI agent is available' do
       it 'processes user questions' do
         post '/api/ask', params: { question: 'Help with deployment' }
         expect(response).to have_http_status(:success)
         expect(JSON.parse(response.body)).to include('answer')
       end
     end

     context 'when AI agent is unavailable' do
       before do
         stub_request(:post, %r{ai-agent-service})
           .to_return(status: 503)
       end

       it 'handles graceful degradation' do
         post '/api/ask', params: { question: 'Help needed' }
         expect(response).to have_http_status(:service_unavailable)
         expect(JSON.parse(response.body)['message'])
           .to eq('AI assistant temporarily unavailable')
       end
     end
   end
   ```""",
    }

if not gemini_api_key:
    raise ValueError("❌ GEMINI_API_KEY is required!")

print(f"🚀 Initializing Ruby Developer AI Agent...")

# Initialize LiteLLM with Gemini
llm_model = LiteLlm(
    model="gemini/gemini-2.0-flash",
    api_key=gemini_api_key,
)

print(f"✅ Gemini model initialized successfully!")

# Create the enhanced agent for Ruby developers
root_agent = Agent(
    name="ruby_workshop_agent",
    model=llm_model,
    description="AI agent for Ruby developers demonstrating integration patterns, CI/CD workflows, and deployment strategies.",
    instruction="""You are a helpful AI assistant specialized in helping Ruby developers integrate AI agents into their applications and workflows.

    You can help with:
    1. Current time and workshop information
    2. Ruby code integration patterns (gems, Rails, HTTP clients)
    3. CI/CD integration (GitHub Actions, GitLab CI, Jenkins)
    4. Kubernetes deployment patterns and best practices
    5. Helm chart configurations and ArgoCD setups
    6. Testing strategies for AI-integrated Ruby applications
    7. Production deployment and monitoring advice

    Always provide practical, production-ready examples that Ruby developers can immediately use in their projects. Focus on real-world integration patterns, error handling, and scalability considerations.""",
    tools=[
        get_current_time,
        get_workshop_info,
        analyze_ruby_code,
        cicd_integration_guide,
        kubernetes_deployment_guide,
        helm_chart_patterns,
        ruby_testing_patterns,
    ],
)

print("✅ Ruby Developer AI Agent created successfully!")