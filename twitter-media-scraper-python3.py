#!/usr/bin/env python3

"""
Twitter Media Scraper Python3 v1.0
Created by Chris Harris
cjharris.co.uk
GitHub: cjharris18
"""

import argparse
import os
import tweepy
import pandas as pd
import requests
import json

# Define colours we will use for text back to the user.
class colours:
    GREEN = '\033[92m'
    ERROR = '\033[93m'
    DEFAULT = '\033[0m'

# Display program information to the user.
def starter_message():
    print(
        r"""
        Twitter Media Scraper Python3 v1.0
             ------------------------
           Version 1.0 by Chris Harris
                 cjharris.co.uk
               Github: cjharris18
        """
        )

# Take the username from the user if not already specified on the command line.
def prompt_username():
    error = True

    while error == True:
        # Loop until an input is specified that is valid.
        twitter_uname == input("Please enter your Twitter Username: ")
        error = False

        # Later here, validate the account exists.
        return twitter_uname

# Function to validate that the enviroment variables exist. If not, we will error and exit.
def check_env_var():
    # If all are present, show a success message.
    if ('CONSUMER_KEY') and ('CONSUMER_SECRET') and ('ACCESS_TOKEN') and ('ACCESS_SECRET') and ('BEARER_TOKEN') in os.environ:
        print(colours.GREEN + " [✓] Consumer Key, Consumer Secret, Access Token, Access Token Secret and Bearer Token Successfully Read.\n" + colours.DEFAULT)
    else:
        # If they are not, check for what is not present and return an error.
        if ('CONSUMER_KEY') not in os.environ:
            print(colours.ERROR + " [!] Consumer Key not Found.\n" + colours.DEFAULT)
        
        if ('CONSUMER_SECRET') not in os.environ:
            print(colours.ERROR + " [!] Consumer Secret not Found.\n" + colours.DEFAULT)

        if ('ACCESS_TOKEN') not in os.environ:
            print(colours.ERROR + " [!] Access Token not Found.\n" + colours.DEFAULT)

        if ('ACCESS_SECRET') not in os.environ:
            print(colours.ERROR + " [!] Access Token Secret not Found.\n" + colours.DEFAULT)

        if ('BEARER_TOKEN') not in os.environ:
            print(colours.ERROR + " [!] Bearer Token not Found.\n" + colours.DEFAULT)
        
        exit()

# Allow the user the options to enter the enviroment variables.
def enter_enviroment_variables():
    os.system('clear')
    starter_message()

    os.environ['CONSUMER_KEY'] = input("Please Enter your Consumer Key: ")
    os.environ['CONSUMER_SECRET'] = input("Please Enter your Consumer Secret: ")

    os.environ['ACCESS_TOKEN'] = input("Please Enter your Access Token: ")
    os.environ['ACCESS_SECRET'] = input("Please Enter your Access Token Secret: ")    

    os.environ['BEARER_TOKEN'] = input("Please Enter the your Bearer Token: ")

def get_client():
    # Accessing our Enviroment variables.
    access_token = os.getenv('ACCESS_TOKEN')
    access_token_secret = os.getenv('ACCESS_SECRET')
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    bearer_token = os.getenv('BEARER_TOKEN')

    # Authorise ourselves with the API.
    client = tweepy.Client( bearer_token=bearer_token, 
                            consumer_key=consumer_key, 
                            consumer_secret=consumer_secret, 
                            access_token=access_token, 
                            access_token_secret=access_token_secret, 
                            return_type = requests.Response,
                            wait_on_rate_limit=True) 
    return client

# Get the ID from the username.
def get_id(client, username):
    try:
        # Use the get_user function to grab the information.
        user = client.get_user(username=username)

        # Get the user data in json format.
        user_data = json.loads(user.content)

        # Filter out the specific ID that we need.
        user_id = user_data["data"]["id"]

        print(colours.GREEN + " [✓] Username Validated Successfully.\n" + colours.DEFAULT)
        return user_id
    
    # If the user does not exist, then this will error. We can handle this here.
    except:
        print(colours.ERROR + " [!] Invalid Username. Please Try Again...\n" + colours.DEFAULT)
        exit()
    
def get_tweets(twitter_username):

    # Call the function to authenticate us with the Twitter API.
    client = get_client()
    
    # Call the fucntion to grab the user ID from the username.
    user_id = get_id(client, twitter_username)
    
    # Send the request to the api for the users recent tweets.
    # Academic access is required to do it any other way. We can grab up to 100 tweets.
    tweets = client.get_users_tweets(id=user_id,
                                    max_results=100,
                                    exclude=['retweets','replies']
                                    )
    
    # Save the data as a dictionary.
    tweets_dict = tweets.json() 

    # Check if the user wishes to output the data to a file.
    if args.output:
        write_file(tweets_dict)

    # Extract the "data" value from the dictionary.
    tweets_data = tweets_dict['data'] 

    # Transform to pandas Dataframe, to make it more readable.
    df = pd.json_normalize(tweets_data)

    print(df)

# Write the JSON tweet data to a file.
def write_file(tweets_json):
    # If the file is a directory, an erorr will be thrown as it can not be written to.
    if os.path.isdir(args.output):
        print(colours.ERROR + " [!] Specified Output File is an Existing Directory.\n" + colours.DEFAULT)
    elif os.path.isfile(args.output):
        # Write to the file by dumping the JSON.
        with open(args.output, 'w') as file:
            json.dump(tweets_json, file)
            print(colours.GREEN + " [✓] Successfully wrote to file.\n" + colours.DEFAULT)
    # Handle any other errors.
    else:
        print(colours.ERROR + " [!] Error Writing to File.\n" + colours.DEFAULT)


if __name__ == "__main__":

    # Argument Handler.
    parser = argparse.ArgumentParser(description='Extract and Analyse Twitter Data.')

    # Allow the user the option to specify a username at the command line.
    parser.add_argument('-t', '--twitter', type=str, help='Specify Twitter Username at the Command Line.')
    parser.add_argument('-o', '--output', type=str, help='Specify a filename to store the JSON tweet data.')
    
    # Allow the user to bypass entering enviroment variables.
    parser.add_argument('-e','--env', help='Do not prompt for Enviroment Variables.', action='store_true')

    args = parser.parse_args()    
    
    twitter_uname = ''

    # Check if the username is specified at the command line or not.
    if args.twitter:
        starter_message()
        print(colours.GREEN + " [✓] Twitter Username Successfully Read from the Command Line.\n" + colours.DEFAULT)
        twitter_uname = args.twitter
    else:
        starter_message()
        twitter_uname = prompt_username()
        

    # If the user wants to specify the enviroment variables, we should ask for them. 
    if args.env == True:
        # We need to check the variables needed exist.
            check_env_var()
    else:
        enter_enviroment_variables()

    get_tweets(twitter_uname)