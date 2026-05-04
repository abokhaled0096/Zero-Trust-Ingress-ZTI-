# Implementation Plan: Zero-Trust AI Security Gateway

This document outlines the phased implementation of a Zero-Trust AI Security Gateway using FastAPI, Gemini CLI Integration, and Docker.

## Project Overview
A security gateway that proxies requests to an AI service, performing real-time security scanning using hybrid logic (Regex + AI Scoring) and maintaining persistent, tamper-evident logs.

---

## Task 1: Basic FastAPI Proxy & Gemini CLI Integration
*   **Objective:** Set up a FastAPI server that acts as a proxy for AI requests, integrating with Gemini CLI for core AI capabilities.
*   **Architect:** 
    *   Define project structure (src/, tests/, logs/).
    *   Initialize `requirements.txt` (fastapi, uvicorn, pydantic, requests).
*   **Coder:**
    *   Implement `/v1/chat/completions` (or similar) endpoint.
    *   Develop a wrapper to invoke `gemini-cli` via shell.
*   **Tester:**
    *   `curl` command to verify proxy connectivity and AI response.
*   **Verification:** `test_proxy_connectivity.py` - Must return 200 OK and a valid AI response.

## Task 2: Security Logging & Blacklist Logic (Hybrid Security)
*   **Objective:** Implement the "Zero-Trust" core with hybrid security filtering and persistent logging.
*   **Architect:**
    *   Define log schema (timestamp, source_ip, payload, security_score, action).
    *   Configure persistent storage for logs (local file/volume).
*   **Coder:**
    *   **Regex Engine:** Filter for PII (emails, SSNs) and common injection patterns.
    *   **AI Scoring:** Use Gemini to score the "risk" of the prompt (0.0 - 1.0).
    *   **Blacklist Logic:** Block requests exceeding a threshold or matching regex.
    *   **Persistent Logger:** Write all attempts to `gateway.log`.
*   **Tester:**
    *   `pytest` suite covering clean prompts (Success) vs. malicious prompts (403 Forbidden).
*   **Verification:** `test_security_filters.py` - Must confirm 403 for blocked patterns and 200 for safe ones.

## Task 3: Dockerization & Volume Mapping
*   **Objective:** Containerize the application for consistent deployment and secure log persistence.
*   **Architect:**
    *   Define `Dockerfile` (multi-stage build preferred).
    *   Define `docker-compose.yml` for orchestration.
*   **Coder:**
    *   Configure environment variables (API keys, security thresholds).
    *   Implement volume mapping for `/logs` to ensure persistence across restarts.
*   **Tester:**
    *   `docker-compose up --build`
    *   Connectivity check to the containerized service.
*   **Verification:** `test_docker_deployment.sh` - Must verify container is running and logs are being written to the host volume.

## Task 4: Automated Log Analysis Script
*   **Objective:** Provide a utility for post-hoc security auditing and trend analysis.
*   **Architect:**
    *   Define analysis requirements (top blocked IPs, common attack patterns).
*   **Coder:**
    *   Python script to parse `gateway.log`.
    *   Generate a summary report (Console + JSON).
*   **Tester:**
    *   Run script against a populated log file.
*   **Verification:** `test_log_analysis.py` - Must verify script correctly counts blocks and identifies "high-risk" entries.

---

## Status Tracking
- [ ] Task 1: FastAPI Proxy & Gemini CLI Integration
- [ ] Task 2: Security Logging & Blacklist Logic
- [ ] Task 3: Dockerization & Volume Mapping
- [ ] Task 4: Automated Log Analysis Script
