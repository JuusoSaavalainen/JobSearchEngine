# miniprojektiDS
Introduction to Data Science miniproject !
Epsilon-Delta 
Arkitehdin lause []

## What are we doing?
- Filtering realistic job posts for entry-level tech jobs.

## How should we do it?
- We should try to separate each part of this plan into its own modules.
- We should inform others that we are working, for example, in data cleaning to avoid conflicts.
- We should inform others about problems and progress that rise to keep everyone up to date 

## PLAN / TODO 

### Getting the data
- We can use a list of keywords to generate a big dataset covering the desired keywords, for example, "SW eng," "Software Developer," etc.
  - Note: We should collectively decide what keywords to include in the baseline CSV that we will create here. 
- We should gather this unique base dataset to proceed with labeling and modeling.
- This can be easily done with an already developed scraper by looping through all the selected keywords and appending unique posts to the CSV.

### Cleaning and wrangling the data
- We need to clean the data to reduce the words in each description.
- For example, we could use basic NLTK to remove punctuation, such as ",", ".", etc., and stopwords.
- Here, we could also convert the data into TF-IDF vectors since we need a numerical format for almost all machine learning approaches.

### Problem / We don't have labels
- We discussed different methods such as unsupervised learning and clustering.
- We believe we should try to label the job descriptions, for example, using LLMs with zero-shot learning, or [Snorkel](https://www.snorkel.org/use-cases/01-spam-tutorial).
- If we cannot achieve good results with any automatic labeling techniques, we must explore non-label approaches.
- The internet offers numerous methods for labeling in situations like ours, so feel free to explore different approaches.
- We don't have the time to label manually.

### Machine Learning
- After __labeling__ the descriptions, we can apply various methods to classify the jobs.
- We should evaluate different methods and choose the most suitable one.
- For example, a simple regression model could be a good choice, or we can try decision trees or other algorithms.
- In the best-case scenario, we would have a numerical representation of how realistic a job is based on the description.
- Most of the classification approaches provide such outcomes.

### Visualizing
- After successfully classifying the jobs, we can use clustering to group job titles into similar buckets, for example, using k-means clustering.
- Then, we would have buckets of similarly named jobs that we can organize to present the most realistic ones from each group.

#### Scraper
- Is still failing sometimes with employment types as you can see with example csv
- Might need adjusts time to time

## Feel free to refine this plan and come up with ideas to make it even better.


# Comprehensive Guide: Using `requirements.txt` with Pipenv in Python

## Overview
The purpose of this guide is to help you understand how to use Pipenv in a Python project that currently relies on a `requirements.txt` file for dependency management. This will cover how to install Pipenv, initialize a virtual environment, import dependencies, and manage your project effectively.

---

## Installation of Pipenv

### Install Pipenv

If you don't have Pipenv installed, you'll need to install it first. 

**Terminal Command**:
\```bash
pip install pipenv
\```

---

### Navigate to Project Directory

Use the terminal to navigate to the directory where your project resides.

### Initialize Virtual Environment

Run the following command to create a new virtual environment:

**Terminal Command**:
\```bash
pipenv --python 3.10
\```

---

## Importing Dependencies

### Install Packages from `requirements.txt`

If your project includes a `requirements.txt` file, you can use Pipenv to install all the dependencies listed in it.

**Terminal Command**:
\```bash
pipenv install -r path/to/requirements.txt
\```

---

##  Pipfile and Dependency Management

### Understand the Pipfile

Once you've installed packages via `requirements.txt`, Pipenv generates a `Pipfile` to manage dependencies more effectively. This `Pipfile` can eventually replace `requirements.txt`.

### Managing Individual Packages

Here are some common commands to manage packages:

- **To install a package**:  
  \```bash
  pipenv install package_name
  \```
  
- **To uninstall a package**:  
  \```bash
  pipenv uninstall package_name
  \```
  
- **To update a package**:  
  \```bash
  pipenv update package_name
  \```

---