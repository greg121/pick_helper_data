# LoL Pick Helper

LoL Pick Helper is a web application that assists League of Legends players in making informed decisions about champion picks and item builds based on match data analysis.

## Features

- Collect and analyze match data from recent games
- Display item build paths and final builds for champions
- Provide insights on champion performance and item efficiency
- User-friendly dashboard for easy data visualization

## Getting Started

### Prerequisites

- Python 3.7+
- Flask
- Git
- League of Legends API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/lol_pick_helper.git
   cd lol_pick_helper
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your configuration file:
   Create a `config.ini` file in the `data_collector` directory with the following structure:
   ```ini
   [General]
   api_key = YOUR_RIOT_API_KEY
   region = YOUR_REGION
   summoner_name = YOUR_SUMMONER_NAME
   tag_line = YOUR_TAG_LINE
   top_enemy = 
   download_count = 10
   version = 0.1
   secret = YOUR_WEBHOOK_SECRET

   [Dashboard]
   open_ai_key = YOUR_OPENAI_API_KEY
   model = 
   ```
   Replace the placeholder values with your actual information.

### Usage

1. Run the data collector to fetch match data:
   ```bash
   python data_collector/collector.py
   ```

2. Start the Flask application:
   ```bash
   python dashboard/app.py
   ```

3. Open a web browser and navigate to `http://localhost:5000` to access the dashboard.

## Project Structure

- `data_collector/`: Scripts for collecting match data from the Riot API
- `dashboard/`: Flask application for the web interface
  - `templates/`: HTML templates for the dashboard
  - `static/`: CSS, JavaScript, and other static files
- `data/`: Storage for collected match data

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Riot Games for providing the League of Legends API
- All contributors who have helped with the project

## Contact

Your Name - [@your_twitter](https://twitter.com/your_twitter) - email@example.com

Project Link: [https://github.com/yourusername/lol_pick_helper](https://github.com/yourusername/lol_pick_helper)


