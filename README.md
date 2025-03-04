# TikTok Downloader Bot

A Telegram bot to download TikTok videos directly within Telegram. This bot uses `yt-dlp` to download videos and `pyrogram` to interact with the Telegram API.

## Features

- 🤖 Download TikTok videos by providing a link.
- 📊 Display video metadata such as title, views, and duration.
- 📈 Show upload progress with a progress bar.
- 📥 Automatically delete the downloaded video after sending.

## Setup

### Prerequisites

- Python 3.9+
- A Telegram account to create a bot and get the API credentials.
- A VPS or local machine to run the bot.

### Installation

1. **Clone the repository:**

```sh
git clone https://github.com/abirxdhack/TikTokDL.git
cd TikTokDL
```

2. **Create a virtual environment and activate it:**

```sh
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. **Install the required libraries:**

```sh
pip install -r requirements.txt
```

4. **Configure your environment variables:**

Create a `.env` file in the root directory of the project and add your API credentials:

````dotenv name=.env
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
````

5. **Create the `config.py` file:**

```python name=config.py
import os

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
```

### Running the Bot

1. **Run the bot:**

```sh
python bot.py
```

### VPS Setup (Optional)

1. **Connect to your VPS and update the system:**

```sh
sudo apt update && sudo apt upgrade -y
```

2. **Install necessary packages:**

```sh
sudo apt install python3 python3-venv python3-pip ffmpeg -y
```

3. **Clone the repository and navigate to the directory:**

```sh
git clone https://github.com/abirxdhack/TikTokDL.git
cd TikTokDL
```

4. **Set up the virtual environment and install dependencies:**

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. **Configure your environment variables:**

Create a `.env` file and add your API credentials as mentioned above.

6. **Run the bot inside a screen session:**

```sh
screen -S tiktok-bot
python bot.py
```

To detach from the screen session, press `Ctrl + A` followed by `D`. To reattach, use:

```sh
screen -r tiktok-bot
```

## Libraries Used

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - A youtube-dl fork with additional features and fixes.
- [pyrogram](https://docs.pyrogram.org/) - A Telegram API framework to build bots and clients.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
