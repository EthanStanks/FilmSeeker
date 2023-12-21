# FilmSeeker

## Description
FilmSeeker is an advanced movie recommender system developed in Python, leveraging state-of-the-art Natural Language Processing (NLP) and Machine Learning techniques. Integrated into a Discord bot for an easy interface, FilmSeeker showcases algorithmic implementations for personalized content recommendation.

## Features
- **NLP-Based Analysis**: Utilizes natural language processing to understand and interpret user preferences and movie descriptions.
- **Machine Learning Algorithms**: Implements sophisticated machine learning models for accurate recommendation predictions.
- **Data Preprocessing and Analysis**: Involves comprehensive data cleaning, preprocessing, and exploratory data analysis for optimal model training.
- **Sentiment Analysis**: Employs sentiment analysis to gauge user reviews and ratings, enhancing recommendation accuracy.
- **Collaborative Filtering**: Integrates collaborative filtering methods to provide recommendations based on similar user interests.

## Installation and Running the Script

To install and run FilmSeeker on your Windows machine, follow these steps:

1. **Clone the Repository**: Download the FilmSeeker codebase to your local machine.<br />
```git clone https://github.com/EthanStanks/FilmSeeker.git```
2. **Install Dependencies**: Ensure you have Python installed, then use `pip` to install the required libraries.<br />
```pip install -r requirements.txt```
3. **Run the Script Without Discord**: Navigate to the ```src``` directory and execute the script.<br />
```python model.py```
4. **Run the Script With Discord**: Navigate to the ```src``` directory and execute the script. Your Discord bot should then be online and ready to use.<br />
```python bot.py```

## Setting Up Discord Bot
The bot application I created will not be hosted online, so you'll have to make your own. It's very easy, follow these steps:

1. **Create Application**: Go to Discord's [developer portal](https://discord.com/developers/applications) and click "New Application".
2. **Application Settings**: Under the ```Bot``` section of the application, enable everything expect for "REQUIRES OAUTH2 CODE GRANT".
3. **Create Text File**: Under the Root directory of FilmSeeker create a text file ```discord_token.txt``` to store the bot's token.
4. **Copy Token**: Reset and copy your bot's new token. Your token is under the ```Bot``` section. Also, don't share this token with anyone.
5. **Paste Token**: Paste the copied token into the created text file.
6. **Invite Bot to Your Server**: Under ```OAuth2 -> URL Generator``, select "bot" as the scope then Administrator as the permission level. Copy the generated URL to invite the bot.

## Credits

Data for FilmSeeker is sourced from Kaggle's "Millions of Movies" dataset, available [here](https://www.kaggle.com/datasets/akshaypawar7/millions-of-movies/). This rich dataset has been instrumental in the development and training of my recommendation algorithms.

---

**Note**: This project is currently tailored for ```Windows operating``` systems.

