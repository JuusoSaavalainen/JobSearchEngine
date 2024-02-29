# Job Search Engine :earth_americas:

Welcome to the Entry Level Job Search Engine, a powerful tool designed to assist entry-level tech job seekers in finding opportunities that do not require previous work experience in the field. This project leverages data from LinkedIn and employs NLI from Hugging Face to provide you with tailored job posts that match your skills and aspirations.

## What is This Project About?

The Entry Level Job Search Engine is created to address a common challenge faced by newcomers to the tech industry - finding job opportunities that do not demand prior work experience. Our project focuses on simplifying this process for entry-level job seekers by using natural language processing and machine learning techniques.

> Detailed description of this project in form of a report can be found [here](https://github.com/JuusoSaavalainen/miniprojektiDS/blob/main/miniprojektiDS.pdf)

## How To Use
We provide demo app hosted with streamlit [here](https://job-search-engine-demo.streamlit.app/)

For legal and privacy reason that can be found
[here](https://www.linkedin.com/robots.txt) and
[here](https://www.linkedin.com/legal/crawling-terms)
we did not want to host webapp that uses any scraping.

We decided to host demo app that simulates the scraping with static data but otherwise behaves similarly.

### If you want to use the scraper to get the realtime joblisting you can do it by running version that includes the scraper locally at your __own risk__.

**Disclaimer:**
This application is provided for informational purposes only. By using this app, you acknowledge that you are using it at your own risk. The app's developers and contributors are not responsible for any consequences resulting from its use.

## Running the App Locally 

### Generate token to use the model from Hugging Face
1. **Create account to Hugging Face and generate token**
 - [Hugging Face](https://huggingface.co/)
2. **Define an Environment Variable**
```export API_KEY="xxxxxxxxxxxx"```
3. **Alternatively you can input the key straight to code by modifying the stapp.py**

### After setting the API_KEY
1. **Clone the Repository**
2. **Navigate to the Project Directory**
3. **Install Dependencies:**
```pip install pipenv```
```pipenv install -r requirements.txt```
```pipenv shell```
5. **Run the app**
```streamlit run stapp.py```
