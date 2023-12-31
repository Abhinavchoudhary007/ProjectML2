# -*- coding: utf-8 -*-
"""ML_project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1knLPvxYYGY0UK7WH80J8Rum2cA05OsYr
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Load the dataset
data = pd.read_csv("/content/Career_Path_Jobs.csv")

# Preprocess the data (cleaning and handling missing values)
data['jobs'] = data['jobs'].fillna('')
data['Career'] = data['Career'].fillna('')
data['Profession'] = data['Profession'].fillna('')

# Combine job descriptions and skills into a single text
data['JobText'] = data['Career'] + ' ' + data['jobs'] + ' ' + data['Profession']

# Create a TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words='english')

# Fit and transform the job text
tfidf_matrix = tfidf_vectorizer.fit_transform(data['JobText'])

# Define a function to get job recommendations based on user input
def get_job_recommendations(user_skills, num_recommendations=5):
    # Transform user input into a TF-IDF vector
    user_input = tfidf_vectorizer.transform([user_skills])

    # Calculate cosine similarity between user input and job descriptions
    cosine_similarities = linear_kernel(user_input, tfidf_matrix)

    # Calculate the weights for columns Carrer, jobs, and Proffesion
    weight_carrer = 2  # You can adjust these weights as needed
    weight_jobs = 2
    weight_proffesion = 1

    # Add weighted cosine similarities for each column
    weighted_similarities = (weight_carrer * cosine_similarities[0] +
                             weight_jobs * cosine_similarities[0] +
                             weight_proffesion * cosine_similarities[0])

    # Get the indices of the most similar jobs
    job_indices = weighted_similarities.argsort()[:-num_recommendations-1:-1]

    # Return the top recommended Proffesion titles
    recommended_proffesions = data['Profession'].iloc[job_indices].tolist()

    return recommended_proffesions


user_skills = "Computer ,Software engineer , Bioscience"

# Get Proffesion recommendations for the user
recommendations = get_job_recommendations(user_skills)
print("Recommended Career for the user and Different fields:")
for i, profession in enumerate(recommendations):
    print(f"{i + 1}. {profession}")