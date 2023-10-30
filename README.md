# Job Search Engine
Detailed description of this project can be found here: __

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
