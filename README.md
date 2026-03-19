# OTP-Spam-IDN

> [!CAUTION]
> **Educational Purposes Only**
> This project is created strictly for educational purposes to demonstrate API interactions, HTTP request handling, and building a Python-based Flask web interface. The author is not responsible for any misuse of this tool. Do not use this script against numbers without explicit permission from the owner.

A Python-based OTP request automation tool with a modern Retro Futurism (Cyberpunk) web interface. OTP-Spam-IDN automates HTTPS requests to various public APIs to simulate OTP deliveries.

## Features

- **Retro Futurism Web UI**: A clean, fully responsive cyberpunk-themed dashboard that replaces the traditional command-line interface.
- **API Debug Monitor**: Real-time tracking of API request statuses directly from the browser. Automatically highlights Dead APIs (timeouts, 404s, 500s) as they execute.
- **Smart Prefix Normalization**: Automatically formats and adapts input phone numbers (`08`, `+628`, `628`, or `8`) to match exactly what each target API payload requires.
- **Asynchronous Execution**: The core logic runs safely in a Flask background thread, allowing you to stop or start the process instantly via the UI dashboard without crashing.

## Installation

Ensure you have [Python](https://www.python.org/downloads/) installed on your system. 

1. Clone the repository:
   ```bash
   git clone https://github.com/ro-boduck/OTP-Spam-IDN.git
   cd OTP-Spam-IDN
   ```

2. Install the required dependencies:
   ```bash
   pip install flask requests bs4 urllib3
   ```

## Usage

1. Start the Flask application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to the local server address:
   `http://127.0.0.1:5000`

3. Enter the target phone number and click **START**. The system will normalize the input and start streaming logs to the terminal UI.
4. Click **KILL** at any time to halt the operation safely.

## Known Dead APIs (Inactive)

The following APIs are currently disabled in the script due to timeout errors or strict security countermeasures:
- `KlikIndomaret` (403 Forbidden)
- `Kredito` (404 Not Found)
- `Gojek` (405 Method Not Allowed)
- `Oyo` (503 Service Unavailable)
- `Foreignadmits` (404 Not Found)
- `Sayurbox` (567 Custom Error)
- `Tokko.io` (Max Retries Exceeded)

You can view the health of active APIs directly through the Web UI's Debug Monitor.
