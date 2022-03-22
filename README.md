<h1 align="center">
  Twitter Media Scraper
</h1>

<p align="center">
<img alt="Supported Platforms" src="https://img.shields.io/badge/Platform-Linux-blue?style=for-the-badge">
<img alt="Language" src="https://img.shields.io/badge/Language-Python3-green?style=for-the-badge">
<img alt="GitHub file size in bytes" src="https://img.shields.io/github/size/cjharris18/Twitter-Media-Scraper/twitter-media-scraper-python3.py?color=brightgreen&style=for-the-badge">
<img alt="License" src="https://img.shields.io/badge/License-MIT-orange?style=for-the-badge">
</p>

<h3 align="center">
  Scrape Tweets and extract Possible Personally Identifiable Information from Twitter accounts.
</h2>

<br>

# What Does This Tool Do?

This tool takes a Twitter username and extracts possible PII. It aims to extract the following from tweets:

- Emails
- Mentions
- Hashtags
- URLs
- IPs

For Output, the default generates a LaTex report titled: `report.pdf`, this name can be changed, it can also be directed to `stdout` instead.

Further Development should focus on increasing the number of available information, as well as improving the regex.

# Installation

```
$ git clone https://github.com/cjharris18/Twitter-Media-Scraper.git
```

From here, enter the repository like so:

```
$ cd Twitter-Media-Scraper/
```
You will want to install any project dependencies, you can do this by running the following:

```
$ pip3 install -r requirements.txt
```

Running the tool can be done as follows:

```
$ python3 twitter-media-scraper-python3.py
```

# Usage

As highlighted previously, the most basic usage can be done as follows:

```
$ python3 twitter-media-scraper-python3.py
```

Using the above command, the user will be prompted for all the fields the tool requires. These can also be specified at the command line:

```
$ python3 twitter-media-scraper-python3.py -h               
usage: twitter-media-scraper-python3.py [-h] [-t TWITTER] [-o OUTPUT] [-e] [-r REPORT] [-s]

Extract and Analyse Tweets for potential PII.

optional arguments:
  -h, --help            show this help message and exit
  -t TWITTER, --twitter TWITTER
                        Specify Twitter Username at the Command Line.
  -o OUTPUT, --output OUTPUT
                        Specify a filename to store the JSON tweet data.
  -e, --env             Do not prompt for Enviroment Variables.
  -r REPORT, --report REPORT
                        Specify a filename for the report.
  -s, --stdout          Output the information to stdout, not as a report (the default).
```

For getting the required Twitter Keys and Tokens required, you will need a Twitter Developer account. Please follow [this link](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api) for more. The tool requires the following:

- Twitter Access Token (`ACCESS_TOKEN`)
- Twitter Access Secret (`ACCESS_SECRET`)
- Twitter Consumer Key (`CONSUMER_KEY`)
- Twitter Consumer Secret (`CONSUMER_SECRET`)
- Twitter Bearer Token (`BEARER_TOKEN`)

# License

This tool is free and open-source, licensed under the [MIT License](LICENSE)
