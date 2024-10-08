# Zappy

Zappy is a Python app to track the zap status periodically on the Derozap website.
Notifications are sent using Pushover to acknowledge Zaps or warn that a Zap has not been registered today.

## Features

- Automated zap status checks.
- Notifications via Pushover, with priority settings for different conditions.
- State management (via `zappy_state.json`) to prevent redundant notifications after the zap status has been acknowledged for the day.

## Requirements

- Pushover account for notifications
- Environment variables configured for credentials and tokens.

## Installation

1. **Set up environment variables**:
   Create a `.env` file in the root directory of the project with the following environment variables:
   ```env
   DEROZAP_EMAIL=your_derozap_email
   DEROZAP_PASSWORD=your_derozap_password
   PUSHOVER_USER=your_pushover_user_key
   PUSHOVER_ZAPPY_TOKEN=your_pushover_zappy_token
   PUSHOVER_LOGS_TOKEN=your_pushover_logs_token # optional, can use same token as Zappy app if you prefer
   ```

## Usage

The main file, `zappy.py`, is intended to be called periodically by a cron job (or other task scheduler) every 5 minutes to check the zap status. However, it keeps track of whether the zap status has already been acknowledged for the day, so no redundant notifications are sent.

## File Descriptions

- **`zappy.py`**: The main script for managing zap status checks.
- **`pushover.py`**: Contains the `Pushover` class for sending notifications to the Pushover service.
- **`derozap.py`**: Contains the `Derozap` class for making requests to the Derozap website to get the zap status.
- **`warn.py`**: Sends a warning notification if a zap is not received.
- **`state_machine.py`**: Manages the state transitions and logic to keep track of zap status over time.
- **`logger.py`**: Provides logging functionality to keep track of the application's events.