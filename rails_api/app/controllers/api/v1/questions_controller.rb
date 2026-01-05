require 'net/http'
require 'uri'
require 'json'

module Api
  module V1
    class QuestionsController < ActionController::API
      def create
        store_id = params[:store_id]
        question = params[:question]

        # Input Validation
        if store_id.blank? || question.blank?
          render json: { error: "store_id and question are required" }, status: 422 and return
        end

        # Security & Auth Placeholder (Requirement: Secure handling of tokens)
        # In a real app:
        # - Authenticate the request (via HMAC or session).
        # - Retrieve the encrypted 'offline' access token from PostgreSQL database.
        shop_token = mock_secure_token_lookup(store_id)

        if shop_token.nil?
           render json: { error: "Unauthorized: Shop not found or app not installed." }, status: 401 and return
        end

        # Forward to Python AI Service
        begin
          uri = URI.parse("http://localhost:8000/ask")
          http = Net::HTTP.new(uri.host, uri.port)
          
          # Prepare request with secure headers
          req = Net::HTTP::Post.new(uri.path, {
            'Content-Type' => 'application/json',
            'X-Shopify-Access-Token' => shop_token # Pass token securely for the Agent to use
          })
          
          req.body = { store_id: store_id, question: question }.to_json

          resp = http.request(req)
          
          # Return the Python service response exactly as received
          render json: JSON.parse(resp.body), status: resp.code.to_i
        rescue Errno::ECONNREFUSED
          render json: { error: "AI Service unavailable. Is the Python server running on port 8000?" }, status: 503
        rescue => e
          render json: { error: "Internal Gateway Error: #{e.message}" }, status: 500
        end
      end

      private

      # Simulates looking up a securely stored token in DB
      def mock_secure_token_lookup(id)
        return "shpat_mock_secure_token_12345" if id.present?
        nil
      end
    end
  end
end