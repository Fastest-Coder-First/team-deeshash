# Weather Aplication

Welcome to the weather application, a simple and convenient weather monitoring application.

## Overview

This weather application is designed to check weather of a city and it sends your mobile a notification if it rains.

## Architecture

![s](https://github.com/Fastest-Coder-First/team-deeshash/assets/86907177/824c4592-22ae-4c16-936a-38e192bdb108)


It sends a text message to your number if it rains.

## Features

- Hourly weather update: User can see weather changes every 3 hours.
- Tomorrow's weather: User can see the weather tomorrow.
- Cli Application: User can use the application in the console.
- It sends your mobile phone a notification if it rains.
- Web application: User can monitor the weather changes in web application also.

## Usage

- Console application usage:

  1. Clone the repository

     ```bash
        git clone https://github.com/Fastest-Coder-First/team-deeshash/

  2. Run the cli application

      ```bash
       python3 weather_cli.py <city_name> [-time tomorrow/hourly] [-help]

- Web application

  1. After cloning the repository, run this command to turn on the server

     ``` bash
     python3 weatherapp.py

  2. Navigate to browser and access

     ```bash
     http://localhost:5000




## Technologies Used

- Python
- Flask
  
