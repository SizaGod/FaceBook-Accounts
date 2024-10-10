# Facebook Account Recovery Bot

This repository provides a bot that automates the process of recovering Facebook accounts using temporary emails. The bot uses a sequence of operations including generating temporary emails, requesting password reset codes, and submitting the codes for account recovery.

## Features

- Automated Facebook Account Recovery: The bot handles the entire recovery process including sending password reset requests and submitting codes.
- Temporary Email Usage: Automatically generates temporary email addresses to handle Facebook's password reset process.
- Session Management: Manages cookies and sessions to persist account recovery throughout the process.
- Code Submission: Automatically extracts the reset code from temporary emails and submits it to Facebook.
- Automatic Logging: Logs successful recoveries and checkpoints for further action.

## How It Works

1. Temporary Email Generation: The bot uses TempMail to create temporary email addresses for password reset requests.
2. Password Reset Request: The bot sends a password reset request to Facebook, using the generated email address.
3. Receive and Submit Code: The bot waits for the reset code to arrive via email, then submits it to Facebook for account recovery.
4. Logging: Successfully recovered accounts, along with their details, are logged for future reference.

## Requirements

- Python environment with necessary packages installed.

## TeleGram Channel

- https://t.me/SizaGodCh
