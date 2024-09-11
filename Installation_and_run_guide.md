# Installation and Run guide

## Installation

### Environment

Using Dot Env.
Create a .env file in the root directory and include two parameters:
USER=(Email of a Canvas account with admin rights)
PASS=(pass)

## Run Guide

## Design choices

# To API or not

I have chosen NOT to leverage the Canvas API.
This is something that should be remedied in a proper production build as some tasks will be much easier through the API rather than using Playwright to get that information.
However, this project is built as it is to explore the use of Playwright first, and provide utility second.

# External CDN based images and files

Currently it will report external files like these as an issue.

## Known issues and quirks
