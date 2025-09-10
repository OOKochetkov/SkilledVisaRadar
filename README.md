# SkilledVisaRadar

![Python](https://img.shields.io/badge/python-3.11-blue)
![Docker](https://img.shields.io/badge/docker-ready-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

Monitor Australian Skilled Visa programs (190 & 491) with AI-generated summaries and email alerts.

---

## Overview

SkilledVisaRadar automatically checks official Australian visa websites (namely, Victorian) for updates, summarises important changes using AI, and sends email notifications.

This helps users stay informed about any updates of Skilled Visa 190 and 491 programs without manually monitoring multiple pages.

---

## Features

- Periodically monitors multiple visa program URLs.  
- Summarises changes using OpenAI GPT.  
- Sends email alerts when relevant updates are detected.  
- Dockerised for easy deployment and consistent operation.  

---

## Setup & Usage

1. **Clone the repository**

```bash
git clone https://github.com/OOKochetkov/SkilledVisaRadar.git
cd SkilledVisaRadar
```
2. **Create a .env file in the project root:**
```
URLS=https://example1.com,https://example2.com
CHECK_INTERVAL=3600
EMAIL_FROM=youremail@gmail.com
EMAIL_TO=recipient@gmail.com
EMAIL_PASS=your_app_password
OPENAI_API_KEY=your_openai_api_key
```
3. **Build Docker image:**
```bash
docker build -t visa-watcher .
```
4. **Run the container**
```bash
docker run -d --restart=always --env-file .env --name visa-watcher visa-watcher python -u main.py
```
-d runs in the background
--restart=always keeps the container running after reboots
-u ensures real-time logging

5. **Check logs**
```bash
docker logs -f visa-watcher
```
Notes:
The script uses OpenAI GPT to generate summaries. Make sure your API key is valid.
The .env file is required for email and API configuration.

License:
MIT License. See LICENSE for details.


