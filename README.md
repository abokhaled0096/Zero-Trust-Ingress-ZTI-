# Zero-Trust AI Security Gateway

A robust, multi-layered security gateway designed to protect AI service interactions. This project implements a "Zero-Trust" architecture by intercepting requests, performing real-time threat analysis using hybrid logic (Regex + AI Scoring), and maintaining tamper-evident logs for audit and compliance.

## 🚀 Features

- **AI-Powered Threat Analysis**: Integrates with Gemini AI to perform deep semantic analysis of prompts to identify malicious intent.
- **Hybrid Security Filtering**: Combines fast regex-based pattern matching (for PII and common injections) with sophisticated AI scoring.
- **Real-Time Blacklisting**: Automatically blocks malicious IPs for 24 hours using Redis for high-performance session management.
- **Persistent Audit Logging**: Stores detailed security event logs in PostgreSQL, including risk scores, payloads, and mitigation actions.
- **Automated Security Insights**: Includes a utility to generate Markdown security reports summarizing recent threats and suggested mitigations.
- **Containerized Architecture**: Fully dockerized for consistent deployment across any environment.

## 🏗️ Architecture

The gateway consists of several microservices:
1. **Gateway Service**: The entry point that handles incoming requests and orchestrates security checks.
2. **AI Analyzer Service**: Specialized service that invokes the Gemini CLI for deep threat analysis.
3. **Redis**: Used for high-speed blacklisted IP storage.
4. **PostgreSQL**: Used for long-term persistence of security audit logs.

## 📋 Prerequisites

- **Docker & Docker Compose**
- **Google API Key**: Required for Gemini AI analysis.
- **Gemini CLI**: Installed and configured (if running outside of Docker).

## 🛠️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/zero-trust-ai-security-gateway.git
   cd zero-trust-ai-security-gateway
   ```

2. **Configure Environment Variables**:
   Create a `.env` file or export your API key:
   ```bash
   export GOOGLE_API_KEY="your_actual_api_key_here"
   ```

3. **Deploy with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

The gateway will be accessible at `http://localhost:8000`.

## 📖 Usage

### 🔍 Analyzing a Prompt
Send a POST request to the gateway to analyze a potential AI prompt:

```bash
curl -X POST http://localhost:8000/analyze \
     -H "Content-Type: application/json" \
     -d '{"text": "How do I secure my web application?"}'
```

### 📊 Generating Security Reports
To generate a security audit report based on the latest logs:

```bash
docker-compose exec ai-analyzer-service python src/log_auditor.py
```
This will generate a `SECURITY_INSIGHTS.md` file with AI-generated summaries of recent activity.

## ⚙️ Configuration

Security thresholds and whitelists can be managed in `security_config.json`:

```json
{
    "whitelisted_ips": ["127.0.0.1"],
    "strict_mode": true,
    "score_threshold": 7
}
```

- `score_threshold`: Risk score (1-10) above which a request is automatically blocked.
- `strict_mode`: If true, any AI analysis failure results in a blocked request.

## 📂 Project Structure

```text
├── src/
│   ├── ai_analyzer.py   # AI deep scan service
│   ├── log_auditor.py   # Security report generator
│   ├── models.py        # Database models (SQLAlchemy)
│   └── main.py          # Main Gateway entry point (FastAPI)
├── tests/
│   └── verify_security.py # Integration tests
├── docker-compose.yml   # Infrastructure orchestration
├── Dockerfile           # Multi-service build configuration
└── security_config.json # Gateway security policy
```

## 🛡️ Security Note

Ensure your `GOOGLE_API_KEY` is never committed to version control. Use Docker secrets or environment variables for production deployments.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
