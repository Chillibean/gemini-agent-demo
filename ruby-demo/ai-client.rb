#!/usr/bin/env ruby
# workshop_demo.rb

require 'faraday'
require 'json'
require 'securerandom'

class AIClient
  def initialize(base_url = 'http://localhost:4000')
    @base_url = base_url
    @app_name = 'example_agent'
    @connection = Faraday.new(url: @base_url)
  end

  def test_connection
    puts "🔍 Testing connection to #{@base_url}"

    response = @connection.get('/health')
    if response.success?
      puts "✅ Health check passed"

      apps_response = @connection.get('/list-apps')
      if apps_response.success?
        apps = JSON.parse(apps_response.body)
        puts "✅ Available apps: #{apps}"
        return true
      end
    else
      puts "❌ Health check failed: #{response.status}"
      return false
    end
  rescue => e
    puts "❌ Connection failed: #{e.message}"
    false
  end

  def create_session
    response = @connection.post("/apps/#{@app_name}/users/user/sessions") do |req|
      req.headers['Content-Type'] = 'application/json'
      req.body = {}.to_json
    end

    if response.success?
      session_data = JSON.parse(response.body)
      session_id = session_data['id']
      puts "✅ Session created: #{session_id}"
      return session_id
    else
      puts "❌ Session creation failed: #{response.status}"
      return nil
    end
  rescue => e
    puts "❌ Session creation error: #{e.message}"
    nil
  end

  def ask(question)
    puts "\n🤖 Question: #{question}"
    puts "-" * 50

    # Create session
    session_id = create_session
    return nil unless session_id

    # Send message
    response = @connection.post('/run_sse') do |req|
      req.headers['Content-Type'] = 'application/json'
      req.body = {
        appName: @app_name,
        userId: "user",
        sessionId: session_id,
        newMessage: {
          role: "user",
          parts: [{ text: question }]
        },
        streaming: false
      }.to_json
    end

    if response.success?
      parse_ai_response(response.body)
    else
      puts "❌ Message failed: #{response.status}"
      nil
    end
  rescue => e
    puts "❌ Error: #{e.message}"
    nil
  end

  def parse_ai_response(sse_data)
    puts "🤖 AI Response:"

    # Parse Server-Sent Events format
    final_response = ""

    sse_data.split("\n").each do |line|
      next unless line.start_with?("data: ")

      begin
        json_data = JSON.parse(line[6..-1])  # Remove "data: " prefix

        if json_data['content'] && json_data['content']['parts']
          json_data['content']['parts'].each do |part|

            # Handle function calls
            if part['functionCall']
              function_name = part['functionCall']['name']
              puts "   🔧 Calling function: #{function_name}"
            end

            # Handle function responses
            if part['functionResponse']
              response_data = part['functionResponse']['response']
              if response_data['report']
                puts "   📋 Function result: #{response_data['report']}"
              end
            end

            # Handle text responses
            if part['text']
              final_response += part['text']
              puts "   💬 #{part['text'].strip}"
            end
          end
        end
      rescue JSON::ParserError
        # Skip malformed JSON
      end
    end

    puts "✅ Complete!"
    final_response
  end
end

# Workshop Demo Script
puts "🚀 Ruby + AI Workshop Demo"
puts "=" * 50

client = AIClient.new

# Test connection
unless client.test_connection
  puts "❌ Connection failed. Make sure agent is running!"
  exit 1
end

puts "\n🎪 Live Demo Starting..."

# Demo questions for workshop
demo_questions = [
  "What time is it?",
  "Tell me about this workshop",
  "How do I integrate this AI agent into my Rails applications?",
  "Show me CI/CD patterns for Ruby + AI"
]

demo_questions.each_with_index do |question, index|
  puts "\n" + "="*60
  puts "📋 Demo #{index + 1}/#{demo_questions.length}"

  client.ask(question)

  puts "\n⏳ (Pausing for demo effect...)"
  sleep 2
end

puts "\n" + "="*60
puts "🎉 Workshop Demo Complete!"
puts "\n📚 Key Takeaways for Ruby Developers:"
puts "✅ Easy HTTP integration with Faraday"
puts "✅ Session management patterns"
puts "✅ AI function calling in action"
puts "✅ Server-Sent Events parsing"
puts "✅ Production-ready error handling"
puts "\n🚀 Ready to integrate AI into your Ruby applications!"