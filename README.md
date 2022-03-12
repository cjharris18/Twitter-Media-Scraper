<h1 align="center">
  Twitter Media Scraper
</h1>

<h3 align="center">
  Scrape Tweets and extract Possible Personally Identifiable Information from Twitter accounts.
</h2>

<br>

# What Does This Tool Do?

This tool takes a Twitter username and extracts possible PII. It aims to extract the following from tweets:

- Phone Numbers
- Emails
- Names

It also extracts any information stored for the username itself, this includes emails and mobile numbers linked.

# Installation

```
$ git clone https://github.com/cjharris18/Twitter-Media-Scraper.git
```

From here, enter the repository like so:

```
$ cd Twitter-Media-Scraper
```

Running the tool can be done as follows:

```
$ python3 twitter-media-scraper-python3.py
```

## Usage

As highlighted previously, the most basic usage can be done as follows:

```
$ python3 twitter-media-scraper-python3.py
```

Using the above command, the user will be prompted for all the fields the tool requires. These can also be specified at the command line:

```
$ python3 twitter-media-scraper-python3.py --help
usage: twitter-media-scraper-python3.py [-h] [-t TWITTER] [-e]

Extract and Analyse GeoSocial Data.

optional arguments:
  -h, --help            show this help message and exit
  -t TWITTER, --twitter TWITTER
                        Specify Twitter Username at the Command Line.
  -e, --env             Do not prompt for Enviroment Variables.
```

For getting the required Twitter Keys and Tokens required, you will need a Twitter Developer account. Please follow [this link](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api) for more. The tool requires the following:

- Twitter Access Token (`ACCESS_TOKEN`)
- Twitter Access Secret (`ACCESS_SECRET`)
- Twitter Consumer Key (`CONSUMER_KEY`)
- Twitter Consumer Secret (`CONSUMER_SECRET`)
- Twitter Bearer Token (`BEARER_TOKEN`)

# License

This tool is free and open-source, licensed under the [MIT License](LICENSE)
