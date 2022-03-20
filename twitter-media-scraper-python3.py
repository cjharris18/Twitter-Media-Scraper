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
import requests
import json
import regex
import requests
from pylatex import Document, Section, Command, NoEscape, LargeText
from datetime import date

# Define colours we will use for text back to the user.
class colours:
    GREEN = "\033[92m"
    ERROR = "\033[93m"
    BOLD = "\033[1m"
    ITALIC = "\x1B[3m"
    DEFAULT = "\033[0m"


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
    if (
        ("CONSUMER_KEY")
        and ("CONSUMER_SECRET")
        and ("ACCESS_TOKEN")
        and ("ACCESS_SECRET")
        and ("BEARER_TOKEN") in os.environ
    ):
        print(
            colours.GREEN
            + " [✓] Consumer Key, Consumer Secret, Access Token, Access Token Secret and Bearer Token Successfully Read."
            + colours.DEFAULT
        )
    else:
        # If they are not, check for what is not present and return an error.
        if ("CONSUMER_KEY") not in os.environ:
            print(colours.ERROR + " [!] Consumer Key not Found..." + colours.DEFAULT)

        if ("CONSUMER_SECRET") not in os.environ:
            print(colours.ERROR + " [!] Consumer Secret not Found..." + colours.DEFAULT)

        if ("ACCESS_TOKEN") not in os.environ:
            print(colours.ERROR + " [!] Access Token not Found..." + colours.DEFAULT)

        if ("ACCESS_SECRET") not in os.environ:
            print(
                colours.ERROR
                + " [!] Access Token Secret not Found..."
                + colours.DEFAULT
            )

        if ("BEARER_TOKEN") not in os.environ:
            print(colours.ERROR + " [!] Bearer Token not Found..." + colours.DEFAULT)

        exit()


# Allow the user the options to enter the enviroment variables.
def enter_enviroment_variables():
    os.system("clear")
    starter_message()

    os.environ["CONSUMER_KEY"] = input("Please Enter your Consumer Key: ")
    os.environ["CONSUMER_SECRET"] = input("Please Enter your Consumer Secret: ")

    os.environ["ACCESS_TOKEN"] = input("Please Enter your Access Token: ")
    os.environ["ACCESS_SECRET"] = input("Please Enter your Access Token Secret: ")

    os.environ["BEARER_TOKEN"] = input("Please Enter the your Bearer Token: ")


def get_client():
    # Accessing our Enviroment variables.
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_SECRET")
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    bearer_token = os.getenv("BEARER_TOKEN")

    # Authorise ourselves with the API.
    client = tweepy.Client(
        bearer_token=bearer_token,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
        return_type=requests.Response,
        wait_on_rate_limit=True,
    )

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

        print(colours.GREEN + " [✓] Username Validated Successfully." + colours.DEFAULT)
        return user_id

    # If the user does not exist, then this will error. We can handle this here.
    except:
        print(
            colours.ERROR
            + " [!] Invalid Username. Please Try Again..."
            + colours.DEFAULT
        )
        exit()


# Write the JSON tweet data to a file.
def write_file(tweets_json):
    # If the file is a directory, an erorr will be thrown as it can not be written to.
    if os.path.isdir(args.output):
        print(
            colours.ERROR
            + " [!] Specified Output File is an Existing Directory..."
            + colours.DEFAULT
        )
    else:
        # Write to the file by dumping the JSON.
        with open(args.output, "w") as file:
            json.dump(tweets_json, file)
            print(colours.GREEN + " [✓] Successfully wrote to file." + colours.DEFAULT)


# Get the raw tweets from the user.
def get_tweets(twitter_username):

    # Call the function to authenticate us with the Twitter API.
    client = get_client()

    # Call the fucntion to grab the user ID from the username.
    user_id = get_id(client, twitter_username)

    # Send the request to the api for the users recent tweets.
    # Academic access is required to do it any other way. We can grab up to 100 tweets.
    tweets = client.get_users_tweets(id=user_id, max_results=100, exclude=["retweets"])

    # Save the data as a dictionary.
    tweets_dict = tweets.json()

    tweets_data = tweets_dict["data"]
    # Check if the user wishes to output the data to a file.
    if args.output:
        write_file(tweets_data)

    return tweets_data


# Here we grab the information we want from the tweets.
def grab_information(tweet_data):

    # Lets have a check for if we find anything or not.
    information = False

    # we need to grab the text itself, its stored as an array of dictionaries. Type to string.
    str_tweet_data = [x["text"] for x in tweet_data]

    # Define our regular expressions to be used.
    emails_regex = r"(\b[\w.]+@+[\w.]+.+[\w.]\b)"
    mentions_regex = r"(?<=^|(?<=[^a-zA-Z0-9-\.]))@([A-Za-z0-9_]+)"
    hashtags_regex = r"(?<=^|(?<=[^a-zA-Z0-9-\.]))#([A-Za-z0-9_]+)"
    url_regex = r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
    ip_regex = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"

    # Call the regex extraction function we made using the different regex.
    emails = grab_info_regex(str_tweet_data, emails_regex)
    mentions = grab_info_regex(str_tweet_data, mentions_regex)
    hashtags = grab_info_regex(str_tweet_data, hashtags_regex)
    urls = grab_info_regex(str_tweet_data, url_regex)
    ips = grab_info_regex(str_tweet_data, ip_regex)

    # Correctly format the mentions.
    for n in range(len(mentions)):
        mentions[n] = "@" + mentions[n]

    # Correctly format the hashtags.
    for n in range(len(hashtags)):
        hashtags[n] = "#" + hashtags[n]

    return emails, mentions, hashtags, urls, ips


# Grab the data from the tweets using regex.
def grab_info_regex(tweet_data, regex_str):
    # apply the regular expression and add the results to a list.
    expression = regex.compile(regex_str)
    matched_regex = [y for x in tweet_data for y in expression.findall(x)]

    return matched_regex


# Validate the URLs found.
def validate_urls(all_urls):

    # Lets predefine our array.
    redirected_urls = []

    # They will always redirect, we need to handle this before we validate the URL.
    for new_url in all_urls:
        try:
            # This grabs the redirect urls.
            url_response = requests.head(new_url, allow_redirects=True)
            redirected_urls.append(url_response.url)
        except:
            # If they dont redirect, there is an error.
            redirected_urls.append("No Successful URL Found.")

    return all_urls, redirected_urls


# We shall generate a report to display our output to the user.
def generate_report(emails, mentions, hashtags, urls, ips, twitter_username):
    # Set the geometry options for the report.
    geometry_options = {
        "tmargin": "1cm",
    }
    doc = Document(geometry_options=geometry_options)

    # Generate the title, subtitle and date.
    doc.preamble.append(Command("title", "Twitter Media Scraper Results"))
    doc.preamble.append(Command("date", NoEscape(r"\today")))
    doc.append(NoEscape(r"\maketitle"))

    # Create the heading for the document.
    doc.append(NoEscape("{"))
    doc.append(Command("centering"))
    doc.append(
        LargeText(
            "Personally Identifiable Information from {0}\n".format(twitter_username)
        )
    )
    doc.append(Command("par"))
    doc.append(NoEscape("}"))

    # Create the subheading and show the emails.
    with doc.create(Section("Possible Emails")):
        if emails:
            for n in range(len(emails)):
                doc.append(" - " + emails[n] + "\n")
        else:
            doc.append("NOTHING FOUND...\n")

    # Create the subheading and show the mentions.
    with doc.create(Section("Possible Mentions")):
        if mentions:
            for n in range(len(mentions)):
                doc.append(" - " + mentions[n] + "\n")
        else:
            doc.append("NOTHING FOUND...\n")

    # Create the subheading and show the hashtags.
    with doc.create(Section("Possible Hashtags")):
        if hashtags:
            for n in range(len(hashtags)):
                doc.append(" - " + hashtags[n] + "\n")
        else:
            doc.append("NOTHING FOUND...\n")

    # Validate the URLs.
    all_urls, redirected_urls = validate_urls(urls)

    # Create the subheading and show the urls, both successful and not.
    with doc.create(Section("URLs")):
        if urls:
            doc.append(
                "URLs for Twitter use their built-in link shortner, as a result, we have checked which redirect to a successful url.\n\n"
            )
            for n in range(len(all_urls)):
                doc.append(
                    "- {0}    Redirects to ---->    {1}\n".format(
                        all_urls[n], redirected_urls[n]
                    )
                )
            else:
                doc.append("NOTHING FOUND...\n")

    # Create the subheading and show the ips.
    with doc.create(Section("Possible IP Adresses")):
        if ips:
            for n in range(len(ips)):
                doc.append(" - " + ips[n] + "\n")
        else:
            doc.append("NOTHING FOUND...\n")

    # Be sure to handle any errors here.
    try:
        # Check if the user has specified a name for the file, if not, use a default.
        if args.report:
            doc.generate_pdf(args.report.split(".")[0], clean_tex=True)
            print(
                colours.GREEN
                + " [✓] Successfully Generated the Report to '{0}'.".format(args.report)
                + colours.DEFAULT
            )
        else:
            doc.generate_pdf("report", clean_tex=True)
            print(
                colours.GREEN
                + " [✓] Successfully Generated the Report to 'report.pdf'."
                + colours.DEFAULT
            )
    except:
        print(colours.ERROR + " [!] Error Generating the Report..." + colours.DEFAULT)
        exit()


# If the user wishes to display to stdout, this function is called.
def display_stdout(emails, mentions, hashtags, urls, ips, twitter_username):
    # Generate our title, date and subtitle.
    print("\n" + ("-" * 60))
    print(
        colours.BOLD + (" " * 15) + "Twitter Media Scraper Results\n" + colours.DEFAULT
    )
    print(
        colours.BOLD
        + (" " * 20)
        + "Date of Search: {0}".format(date.today())
        + colours.DEFAULT
    )

    print(
        colours.BOLD
        + (" " * 6)
        + "Personally Identifiable Information from "
        + colours.ITALIC
        + "{0}\n".format(twitter_username)
        + colours.DEFAULT
    )
    print(("-" * 60) + "\n")

    # Show the Emails
    print(colours.BOLD + " Possible Emails Found:\n" + colours.DEFAULT)
    if emails:
        for n in range(len(emails)):
            print(" - " + emails[n] + "\n")
    else:
        print(" NOTHING FOUND...\n")
    print("-" * 60)

    # Show the Mentions.
    print(colours.BOLD + " Possible Mentions Found:\n" + colours.DEFAULT)
    if mentions:
        for n in range(len(mentions)):
            print(" - " + mentions[n] + "\n")
    else:
        print(" NOTHING FOUND...\n")
    print("-" * 60)

    # Show the Hashtags.
    print(colours.BOLD + " Possible Hashtags Found:\n" + colours.DEFAULT)
    if hashtags:
        for n in range(len(hashtags)):
            print(" - " + hashtags[n] + "\n")
    else:
        print(" NOTHING FOUND...\n")
    print("-" * 60)

    # Validate the URLs.
    all_urls, redirected_urls = validate_urls(urls)

    # Show the URLs and their redirects.
    print(colours.BOLD + " Possible URLs Found:" + colours.DEFAULT)
    if urls:
        print(
            " URLs for Twitter use their built-in link shortner, as a result, we have checked which redirect to a successful url.\n"
        )
        for n in range(len(all_urls)):
            print(
                "- {0}    Redirects to ---->    {1}\n".format(
                    all_urls[n], redirected_urls[n]
                )
            )
    else:
        print(" NOTHING FOUND...\n")
    print("-" * 60)

    # Show the ips.
    print(colours.BOLD + " Possible IP Adresses found:\n" + colours.DEFAULT)
    if ips:
        for n in range(len(ips)):
            print(" - " + ips[n] + "\n")
    else:
        print(" NOTHING FOUND...\n")


if __name__ == "__main__":

    # Argument Handler.
    parser = argparse.ArgumentParser(
        description="Extract and Analyse Tweets for potential PII."
    )

    # Allow the user the option to specify a username at the command line.
    parser.add_argument(
        "-t",
        "--twitter",
        type=str,
        help="Specify Twitter Username at the Command Line.",
    )
    # Allow the user to specify an output for the JSON data.
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Specify a filename to store the JSON tweet data.",
    )

    # Allow the user to bypass entering enviroment variables.
    parser.add_argument(
        "-e",
        "--env",
        help="Do not prompt for Enviroment Variables.",
        action="store_true",
    )

    parser.add_argument(
        "-r",
        "--report",
        help="Specify a filename for the report.",
    )

    parser.add_argument(
        "-s",
        "--stdout",
        help="Output the information to stdout, not as a report (the default).",
        action="store_true",
    )

    args = parser.parse_args()

    twitter_uname = ""

    # Check if the username is specified at the command line or not.
    if args.twitter:
        starter_message()
        print(
            colours.GREEN
            + " [✓] Twitter Username Successfully Read from the Command Line."
            + colours.DEFAULT
        )
        twitter_uname = args.twitter
    else:
        starter_message()
        twitter_uname = prompt_username()

    # If the user wants to specify the enviroment variables, we should ask for them.
    if args.env == True:
        # We need to check the variables needed exist.
        check_env_var()
    else:
        # If the variables dont exist, we can prompt the user for them.
        enter_enviroment_variables()

    # We need to retrieve the tweets from the username now.
    tweet_data = get_tweets(twitter_uname)

    # Here we will grab the information we want from the tweets.
    emails, mentions, hashtags, urls, ips = grab_information(tweet_data)

    # Check if the user has the flag set for stdout.
    if args.stdout:
        display_stdout(emails, mentions, hashtags, urls, ips, twitter_uname)
    else:
        generate_report(emails, mentions, hashtags, urls, ips, twitter_uname)
