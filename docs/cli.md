# Minet Command Line Usage

## Summary

*Global utilities*

* [-h/--help/help](#help-flag)
* [--version](#version-flag)
* [minetrc config files](#minetrc)
* [minet environment variables](#envvars)

*Generic commands*

* [crawl](#crawl)
* [fetch](#fetch)
* [extract](#extract)
* [scrape](#scrape)
* [url-extract](#url-extract)
* [url-join](#url-join)
* [url-parse](#url-parse)

*Platform-related commands*

* [crowdtangle (ct)](#crowdtangle)
  * [leaderboard](#leaderboard)
  * [lists](#lists)
  * [posts-by-id](#posts-by-id)
  * [posts](#posts)
  * [search](#ct-search)
  * [summary](#summary)
* [facebook (fb)](#facebook)
  * [comments](#facebook-comments)
  * [url-likes](#facebook-url-likes)
* [hyphe](#hyphe)
  * [dump](#dump)
* [mediacloud (mc)](#mediacloud)
  * [medias](#mc-medias)
  * [search](#mc-search)
  * [topic](#topic)
    * [stories](#stories)
* [twitter](#twitter)
  * [followers](#followers)
  * [friends](#friends)
  * [scrape](#twitter-scrape)
  * [users](#users)
* [youtube (yt)](#youtube)
  * [captions](#captions)
  * [comments](#youtube-comments)
  * [search](#youtube-search)
  * [videos](#videos)


<h2 id="help-flag">-h/--help</h2>

If you need help about a command, don't hesitate to use the `-h/--help` flag or the `help` command:

```
minet ct posts -h
# or:
minet ct posts --help
# or
minet help ct posts
```

<h2 id="version-flag"></h2>

To check the installed version of `minet`, you can use the `--version` flag:

```
minet --version
>>> minet x.x.x
```

<h2 id="minetrc">minetrc config files</h2>

Minet supports configuration files so you can skip some tedious command line arguments that you would need to provide each time you call `minet` otherwise (such as `--token` for crowdtangle commands).

Those configuration files can be written in YAML or JSON and can either be passed to minet using the `--rcfile` argument or will be searched at the following paths (with this precedence):

* `./.minetrc{,.yml,.yaml,.json}`
* `~/.minetrc{,.yml,.yaml,.json}`

*Configuration file*

```yml
---
crowdtangle:
  token: "MY_CT_TOKEN" # Used as --token for `minet ct` commands
  rate_limit: 10 # Used as --rate-limit for `minet ct` commands
facebook:
  cookie: "MY_FACEBOOK_COOKIE" # Used as --cookie for `minet fb` commands
mediacloud:
  token: "MY_MC_TOKEN" # Used as --token for `minet mc` commands
twitter:
  api_key: "MY_API_KEY" # Used as --api-key for `minet tw` commands
  api_secret_key: "MY_API_SECRET_KEY" # Used as --api-secret-key for `minet tw` commands
  access_token: "MY_ACCESS_TOKEN" # Used as --access-token for `minet tw` commands
  access_token_secret: "MY_ACCESS_TOKEN_SECRET" # Used as --access-token-secret for `minet tw` commands
youtube:
  key: "MY_YT_API_KEY" # Used as --key for `minet yt` commands
```

<h2 id="envvars">minet environment variables</h2>

Alternatively you can also set some arguments using environment variables whose name starts with `MINET_` and followed by the proper key.

To build the name of the variable, first check what can be configured in a minet [rcfile](#minetrc) and build your variable name by joining its path using an underscore:

For instance, to override `facebook.cookie`, the variable will be `MINET_FACEBOOK_COOKIE`.

If one of the path's key already contains underscore, it will work all the same. So to override `twitter.api_key`, the variable will be `MINET_TWITTER_API_KEY`.

Note that the given variable will be cast to the proper type as if it was passed as a command line argument (for instance, `MINET_CROWDTANGLE_RATE_LIMIT` will correctly be cast as an integer).

Finally note that command line arguments and flags will take precedence over environment variables, and that environment variables will take precedence over any rcfile configuration, but you can of course mix and match.

## crawl

```
usage: minet crawl [-h] [-d OUTPUT_DIR] [--resume] [--throttle THROTTLE] crawler

Minet Crawl Command
===================

Use multiple threads to crawl the web using minet crawling and
scraping DSL.

positional arguments:
  crawler                                 Path to the crawler definition file.

optional arguments:
  -h, --help                              show this help message and exit
  -d OUTPUT_DIR, --output-dir OUTPUT_DIR  Output directory.
  --resume                                Whether to resume an interrupted crawl.
  --throttle THROTTLE                     Time to wait - in seconds - between 2 calls to the same domain. Defaults to 0.2.

examples:

. TODO:
    `minet crawl`

```

## fetch

```
usage: minet fetch [-h] [--compress] [--contents-in-report] [-d OUTPUT_DIR]
                   [--domain-parallelism DOMAIN_PARALLELISM] [-f FILENAME]
                   [--filename-template FILENAME_TEMPLATE]
                   [--folder-strategy FOLDER_STRATEGY]
                   [-g {chrome,chromium,edge,firefox,opera}] [-H HEADERS]
                   [--resume] [--standardize-encoding] [-o OUTPUT] [-s SELECT]
                   [-t THREADS] [--throttle THROTTLE] [--timeout TIMEOUT]
                   [--total TOTAL] [--url-template URL_TEMPLATE] [-X METHOD]
                   column [file]

Minet Fetch Command
===================

Use multiple threads to fetch batches of urls from a CSV file. The
command outputs a CSV report with additional metadata about the
HTTP calls and will generally write the retrieved files in a folder
given by the user.

positional arguments:
  column                                          Column of the CSV file containing urls to fetch or a single url to fetch.
  file                                            CSV file containing the urls to fetch.

optional arguments:
  -h, --help                                      show this help message and exit
  --compress                                      Whether to compress the contents.
  --contents-in-report, --no-contents-in-report   Whether to include retrieved contents, e.g. html, directly in the report
                                                  and avoid writing them in a separate folder. This requires to standardize
                                                  encoding and won't work on binary formats.
  -d OUTPUT_DIR, --output-dir OUTPUT_DIR          Directory where the fetched files will be written. Defaults to "content".
  --domain-parallelism DOMAIN_PARALLELISM         Max number of urls per domain to hit at the same time. Defaults to 1
  -f FILENAME, --filename FILENAME                Name of the column used to build retrieved file names. Defaults to an uuid v4 with correct extension.
  --filename-template FILENAME_TEMPLATE           A template for the name of the fetched files.
  --folder-strategy FOLDER_STRATEGY               Name of the strategy to be used to dispatch the retrieved files into folders to alleviate issues on some filesystems when a folder contains too much files. Note that this will be applied on top of --filename-template. Defaults to "flat". All of the strategies are described at the end of this help.
  -g {chrome,chromium,edge,firefox,opera}, --grab-cookies {chrome,chromium,edge,firefox,opera}
                                                  Whether to attempt to grab cookies from your computer's browser (supports "firefox", "chrome", "chromium", "opera" and "edge").
  -H HEADERS, --header HEADERS                    Custom headers used with every requests.
  --resume                                        Whether to resume from an aborted report.
  --standardize-encoding                          Whether to systematically convert retrieved text to UTF-8.
  -o OUTPUT, --output OUTPUT                      Path to the output report file. By default, the report will be printed to stdout.
  -s SELECT, --select SELECT                      Columns to include in report (separated by `,`).
  -t THREADS, --threads THREADS                   Number of threads to use. Defaults to 25.
  --throttle THROTTLE                             Time to wait - in seconds - between 2 calls to the same domain. Defaults to 0.2.
  --timeout TIMEOUT                               Maximum time - in seconds - to spend for each request before triggering a timeout. Defaults to ~30s.
  --total TOTAL                                   Total number of lines in CSV file. Necessary if you want to display a finite progress indicator.
  --url-template URL_TEMPLATE                     A template for the urls to fetch. Handy e.g. if you need to build urls from ids etc.
  -X METHOD, --request METHOD                     The http method to use. Will default to GET.

--folder-strategy options:

. "flat": default choice, all files will be written in the indicated
  content folder.

. "prefix-x": e.g. "prefix-4", files will be written in folders
  having a name that is the first x characters of the file's name.
  This is an efficient way to partition content into folders containing
  roughly the same number of files if the file names are random (which
  is the case by default since uuids will be used).

. "hostname": files will be written in folders based on their url's
  full host name.

. "normalized-hostname": files will be written in folders based on
  their url's hostname stripped of some undesirable parts (such as
  "www.", or "m." or "fr.", for instance).

examples:

. Fetching a batch of url from existing CSV file:
    `minet fetch url_column file.csv > report.csv`

. CSV input from stdin:
    `xsv select url_column file.csv | minet fetch url_column > report.csv`

. Fetching a single url, useful to pipe into `minet scrape`:
    `minet fetch http://google.com | minet scrape ./scrape.json > scraped.csv`

```

## extract

```
usage: minet extract [-h] [-i INPUT_DIRECTORY] [-o OUTPUT] [-p PROCESSES]
                     [-s SELECT] [--total TOTAL]
                     [report]

Minet Extract Command
=====================

Use multiple processes to extract raw content and various metadata
from a batch of HTML files. This command can either work on a
`minet fetch` report or on a bunch of files. It will output an
augmented report with the extracted text.

Extraction is performed using the `trafilatura` library by Adrien
Barbaresi. More information about the library can be found here:
https://github.com/adbar/trafilatura

positional arguments:
  report                                          Input CSV fetch action report file.

optional arguments:
  -h, --help                                      show this help message and exit
  -i INPUT_DIRECTORY, --input-directory INPUT_DIRECTORY
                                                  Directory where the HTML files are stored. Defaults to "content".
  -o OUTPUT, --output OUTPUT                      Path to the output report file. By default, the report will be printed to stdout.
  -p PROCESSES, --processes PROCESSES             Number of processes to use. Defaults to 4.
  -s SELECT, --select SELECT                      Columns to include in report (separated by `,`).
  --total TOTAL                                   Total number of HTML documents. Necessary if you want to display a finite progress indicator.

examples:

. Extracting raw text from a `minet fetch` report:
    `minet extract report.csv > extracted.csv`

. Working on a report from stdin:
    `minet fetch url_column file.csv | minet extract > extracted.csv`

. Extracting raw text from a bunch of files:
    `minet extract --glob "./content/*.html" > extracted.csv`

```

## scrape

For more documentation about minet's scraping DSL check this [page](../cookbook/scraping_dsl.md) from the Cookbook.

```
usage: minet scrape [-h] [-f {csv,jsonl}] [-g GLOB] [-i INPUT_DIRECTORY]
                    [-o OUTPUT] [-p PROCESSES] [--total TOTAL]
                    scraper [report]

Minet Scrape Command
====================

Use multiple processes to scrape data from a batch of HTML files.
This command can either work on a `minet fetch` report or on a bunch
of files. It will output the scraped items.

positional arguments:
  scraper                                         Path to a scraper definition file.
  report                                          Input CSV fetch action report file.

optional arguments:
  -h, --help                                      show this help message and exit
  -f {csv,jsonl}, --format {csv,jsonl}            Output format.
  -g GLOB, --glob GLOB                            Whether to scrape a bunch of html files on disk matched by a glob pattern rather than sourcing them from a CSV report.
  -i INPUT_DIRECTORY, --input-directory INPUT_DIRECTORY
                                                  Directory where the HTML files are stored. Defaults to "content".
  -o OUTPUT, --output OUTPUT                      Path to the output report file. By default, the report will be printed to stdout.
  -p PROCESSES, --processes PROCESSES             Number of processes to use. Defaults to 4.
  --total TOTAL                                   Total number of HTML documents. Necessary if you want to display a finite progress indicator.

examples:

. Scraping item from a `minet fetch` report:
    `minet scrape scraper.json report.csv > scraped.csv`

. Working on a report from stdin:
    `minet fetch url_column file.csv | minet scrape scraper.json > scraped.csv`

. Scraping a single page from the web:
    `minet fetch https://news.ycombinator.com/ | minet scrape scraper.json > scraped.csv`

. Scraping items from a bunch of files:
    `minet scrape scraper.json --glob "./content/*.html" > scraped.csv`

```

## url-extract

```
usage: minet url-extract [-h] [--base-url BASE_URL] [--from {html,text}]
                         [-o OUTPUT] [-s SELECT] [--total TOTAL]
                         column [file]

Minet Url Extract Command
=========================

Extract urls from a CSV column containing either raw text or raw
HTML.

positional arguments:
  column                      Name of the column containing text or html.
  file                        Target CSV file.

optional arguments:
  -h, --help                  show this help message and exit
  --base-url BASE_URL         Base url used to resolve relative urls.
  --from {html,text}          Extract urls from which kind of source?
  -o OUTPUT, --output OUTPUT  Path to the output file. By default, the result will be printed to stdout.
  -s SELECT, --select SELECT  Columns to keep in output, separated by comma.
  --total TOTAL               Total number of lines in CSV file. Necessary if you want to display a finite progress indicator.

examples:

. Extracting urls from a text column:
    `minet url-extract text posts.csv > urls.csv`

. Extracting urls from a html column:
    `minet url-extract html --from html posts.csv > urls.csv`

```

## url-join

```
usage: minet url-join [-h] [-o OUTPUT] [-p MATCH_COLUMN_PREFIX] [-s SELECT]
                      [--separator SEPARATOR]
                      column1 file1 column2 file2

Minet Url Join Command
======================

Join two CSV files by matching them on columns containing urls. In
fact, the command will index the first file's urls into a
hierchical trie before attempting to match the second file's ones.

positional arguments:
  column1                                         Name of the url column in the first file.
  file1                                           Path to the first file.
  column2                                         Name of the url column in the second file.
  file2                                           Path to the second file.

optional arguments:
  -h, --help                                      show this help message and exit
  -o OUTPUT, --output OUTPUT                      Path to the output joined file. By default, the join will be printed to stdout.
  -p MATCH_COLUMN_PREFIX, --match-column-prefix MATCH_COLUMN_PREFIX
                                                  Optional prefix to add to the first file's column names to avoid conflicts.
  -s SELECT, --select SELECT                      Columns from the first file to keep, separated by comma.
  --separator SEPARATOR                           Split indexed url column by a separator?

examples:

. Joining two files:
    `minet url-join url webentities.csv post_url posts.csv > joined.csv`

. Keeping only some columns from first file:
    `minet url-join url webentities.csv post_url posts.csv -s url,id > joined.csv`

```

## url-parse

```
usage: minet url-parse [-h] [--facebook] [-o OUTPUT] [-s SELECT]
                       [--separator SEPARATOR] [--strip-protocol]
                       [--total TOTAL] [--youtube]
                       column [file]

Minet Url Parse Command
=======================

Overload a CSV file containing urls with a selection of additional
metadata such as their normalized version, domain name etc.

positional arguments:
  column                                 Name of the column containing urls.
  file                                   Target CSV file.

optional arguments:
  -h, --help                             show this help message and exit
  --facebook                             Whether to consider and parse the given urls as coming from Facebook.
  -o OUTPUT, --output OUTPUT             Path to the output file. By default, the result will be printed to stdout.
  -s SELECT, --select SELECT             Columns to keep in output, separated by comma.
  --separator SEPARATOR                  Split url column by a separator?
  --strip-protocol, --no-strip-protocol  Whether or not to strip the protocol when normalizing the url. Defaults to strip protocol.
  --total TOTAL                          Total number of lines in CSV file. Necessary if you want to display a finite progress indicator.
  --youtube                              Whether to consider and parse the given urls as coming from YouTube.

examples:

. Creating a report about a file's urls:
    `minet url-parse url posts.csv > report.csv`

. Keeping only selected columns from the input file:
    `minet url-parse url posts.csv -s id,url,title > report.csv`

. Multiple urls joined by separator:
    `minet url-parse urls posts.csv --separator "|" > report.csv`

. Parsing Facebook urls:
    `minet url-parse url fbposts.csv --facebook > report.csv`

. Parsing YouTube urls:
    `minet url-parse url ytvideos.csv --youtube > report.csv`

```

## CrowdTangle

```
usage: minet crowdtangle [-h] [--rate-limit RATE_LIMIT] [-o OUTPUT] [-t TOKEN]
                         {leaderboard,lists,posts,posts-by-id,search,summary}
                         ...

Minet Crowdtangle Command
=========================

Gather data from the CrowdTangle APIs easily and efficiently.

optional arguments:
  -h, --help                                      show this help message and exit
  --rate-limit RATE_LIMIT                         Authorized number of hits by minutes. Defaults to 6. Rcfile key: crowdtangle.rate_limit
  -o OUTPUT, --output OUTPUT                      Path to the output file. By default, everything will be printed to stdout.
  -t TOKEN, --token TOKEN                         CrowdTangle dashboard API token. Rcfile key: crowdtangle.token

actions:
  {leaderboard,lists,posts,posts-by-id,search,summary}
                                                  Action to perform using the CrowdTangle API.

```

### leaderboard

```
usage: minet crowdtangle leaderboard [-h] [--rate-limit RATE_LIMIT] [-o OUTPUT]
                                     [-t TOKEN] [--no-breakdown]
                                     [-f {csv,jsonl}] [-l LIMIT]
                                     [--list-id LIST_ID]

Minet CrowdTangle Leaderboard Command
=====================================

Gather information and aggregated stats about pages and groups of the designated dashboard (indicated by a given token).

For more information, see the API endpoint documentation: https://github.com/CrowdTangle/API/wiki/Leaderboard.

optional arguments:
  -h, --help                            show this help message and exit
  --rate-limit RATE_LIMIT               Authorized number of hits by minutes. Defaults to 6. Rcfile key: crowdtangle.rate_limit
  -o OUTPUT, --output OUTPUT            Path to the output file. By default, everything will be printed to stdout.
  -t TOKEN, --token TOKEN               CrowdTangle dashboard API token. Rcfile key: crowdtangle.token
  --no-breakdown                        Whether to skip statistics breakdown by post type in the CSV output.
  -f {csv,jsonl}, --format {csv,jsonl}  Output format. Defaults to `csv`.
  -l LIMIT, --limit LIMIT               Maximum number of accounts to retrieve. Will fetch every account by default.
  --list-id LIST_ID                     Optional list id from which to retrieve accounts.

examples:

. Fetching accounts statistics for every account in your dashboard:
    `minet ct leaderboard --token YOUR_TOKEN > accounts-stats.csv`

```

### lists

```
usage: minet crowdtangle lists [-h] [--rate-limit RATE_LIMIT] [-o OUTPUT]
                               [-t TOKEN]

Minet CrowdTangle Lists Command
===============================

Retrieve the lists from a CrowdTangle dashboard (indicated by a given token).

For more information, see the API endpoint documentation: https://github.com/CrowdTangle/API/wiki/Lists.

optional arguments:
  -h, --help                  show this help message and exit
  --rate-limit RATE_LIMIT     Authorized number of hits by minutes. Defaults to 6. Rcfile key: crowdtangle.rate_limit
  -o OUTPUT, --output OUTPUT  Path to the output file. By default, everything will be printed to stdout.
  -t TOKEN, --token TOKEN     CrowdTangle dashboard API token. Rcfile key: crowdtangle.token

examples:

. Fetching a dashboard's lists:
    `minet ct lists --token YOUR_TOKEN > lists.csv`

```

### posts-by-id

```
usage: minet crowdtangle posts-by-id [-h] [--rate-limit RATE_LIMIT] [-o OUTPUT]
                                     [-t TOKEN] [-s SELECT] [--resume]
                                     [--total TOTAL]
                                     column [file]

Minet CrowdTangle Post By Id Command
====================================

Retrieve metadata about batches of posts using Crowdtangle's API.

For more information, see the API endpoint documentation: https://github.com/CrowdTangle/API/wiki/Posts#get-postid.

positional arguments:
  column                      Name of the column containing the posts URL or id in the CSV file.
  file                        CSV file containing the inquired URLs or ids.

optional arguments:
  -h, --help                  show this help message and exit
  --rate-limit RATE_LIMIT     Authorized number of hits by minutes. Defaults to 6. Rcfile key: crowdtangle.rate_limit
  -o OUTPUT, --output OUTPUT  Path to the output file. By default, everything will be printed to stdout.
  -t TOKEN, --token TOKEN     CrowdTangle dashboard API token. Rcfile key: crowdtangle.token
  -s SELECT, --select SELECT  Columns to include in report (separated by `,`).
  --resume                    Whether to resume an aborted collection.
  --total TOTAL               Total number of posts. Necessary if you want to display a finite progress indicator.

examples:

. Retrieving information about a batch of posts:
    `minet ct posts-by-id post-url posts.csv --token YOUR_TOKEN > metadata.csv`

. Retrieving information about a single post:
    `minet ct posts-by-id 1784333048289665 --token YOUR_TOKEN`

```

### posts

```
usage: minet crowdtangle posts [-h] [--rate-limit RATE_LIMIT] [-o OUTPUT]
                               [-t TOKEN] [--chunk-size CHUNK_SIZE]
                               [--end-date END_DATE] [-f {csv,jsonl}]
                               [--language LANGUAGE] [-l LIMIT]
                               [--list-ids LIST_IDS] [--resume]
                               [--sort-by {date,interaction_rate,overperforming,total_interactions,underperforming}]
                               [--start-date START_DATE]

Minet CrowdTangle Posts Command
===============================

Gather post data from the designated dashboard (indicated by a given token).

For more information, see the API endpoint documentation: https://github.com/CrowdTangle/API/wiki/Posts.

optional arguments:
  -h, --help                                      show this help message and exit
  --rate-limit RATE_LIMIT                         Authorized number of hits by minutes. Defaults to 6. Rcfile key: crowdtangle.rate_limit
  -o OUTPUT, --output OUTPUT                      Path to the output file. By default, everything will be printed to stdout.
  -t TOKEN, --token TOKEN                         CrowdTangle dashboard API token. Rcfile key: crowdtangle.token
  --chunk-size CHUNK_SIZE                         When sorting by date (default), the number of items to retrieve before shifting the inital query to circumvent the APIs limitations. Defaults to 500.
  --end-date END_DATE                             The latest date at which a post could be posted (UTC!). You can pass just a year or a year-month for convenience.
  -f {csv,jsonl}, --format {csv,jsonl}            Output format. Defaults to `csv`.
  --language LANGUAGE                             Language of posts to retrieve.
  -l LIMIT, --limit LIMIT                         Maximum number of posts to retrieve. Will fetch every post by default.
  --list-ids LIST_IDS                             Ids of the lists from which to retrieve posts, separated by commas.
  --resume                                        Whether to resume an interrupted collection. Requires -o/--output & --sort-by date
  --sort-by {date,interaction_rate,overperforming,total_interactions,underperforming}
                                                  The order in which to retrieve posts. Defaults to `date`.
  --start-date START_DATE                         The earliest date at which a post could be posted (UTC!). You can pass just a year or a year-month for convenience.

examples:

. Fetching the 500 most latest posts from a dashboard (a start date must be precised):
    `minet ct posts --token YOUR_TOKEN --limit 500 --start-date 2021-01-01 > latest-posts.csv`

. If your collection is interrupted, it can be restarted from the last data collected with the --resume option:
    `minet ct posts --token YOUR_TOKEN --limit 500 --start-date 2021-01-01 --resume --output latest-posts.csv`

. Fetching all the posts from a specific list of groups or pages:
    `lminet ct posts --token YOUR_TOKEN --start-date 2021-01-01 --list-ids YOUR_LIST_ID > posts_from_one_list.csv`
(To know the different list ids associated with your dashboard: `minet ct lists --token YOUR_TOKEN`)

```

<h3 id="ct-search">search</h3>

```
usage: minet crowdtangle search [-h] [--rate-limit RATE_LIMIT] [-o OUTPUT]
                                [-t TOKEN] [--and AND] [--chunk-size CHUNK_SIZE]
                                [--end-date END_DATE] [-f {csv,jsonl}]
                                [--language LANGUAGE] [-l LIMIT]
                                [--not-in-title] [--offset OFFSET]
                                [-p PLATFORMS]
                                [--search-field {account_name_only,image_text_only,include_query_strings,text_fields_and_image_text,text_fields_only}]
                                [--sort-by {date,interaction_rate,overperforming,total_interactions,underperforming}]
                                [--start-date START_DATE] [--types TYPES]
                                terms

Minet CrowdTangle Search Command
================================

Search posts on the whole CrowdTangle platform.

For more information, see the API endpoint documentation: https://github.com/CrowdTangle/API/wiki/Search.

positional arguments:
  terms                                           The search query term or terms.

optional arguments:
  -h, --help                                      show this help message and exit
  --rate-limit RATE_LIMIT                         Authorized number of hits by minutes. Defaults to 6. Rcfile key: crowdtangle.rate_limit
  -o OUTPUT, --output OUTPUT                      Path to the output file. By default, everything will be printed to stdout.
  -t TOKEN, --token TOKEN                         CrowdTangle dashboard API token. Rcfile key: crowdtangle.token
  --and AND                                       AND clause to add to the query terms.
  --chunk-size CHUNK_SIZE                         When sorting by date (default), the number of items to retrieve before shifting the inital query to circumvent the APIs limitations. Defaults to 500.
  --end-date END_DATE                             The latest date at which a post could be posted (UTC!). You can pass just a year or a year-month for convenience.
  -f {csv,jsonl}, --format {csv,jsonl}            Output format. Defaults to `csv`.
  --language LANGUAGE                             Language ISO code like "fr" or "zh-CN".
  -l LIMIT, --limit LIMIT                         Maximum number of posts to retrieve. Will fetch every post by default.
  --not-in-title                                  Whether to search terms in account titles also.
  --offset OFFSET                                 Count offset.
  -p PLATFORMS, --platforms PLATFORMS             The platforms from which to retrieve links (facebook, instagram, or reddit). This value can be comma-separated.
  --search-field {account_name_only,image_text_only,include_query_strings,text_fields_and_image_text,text_fields_only}
                                                  In what to search the query. Defaults to `text_fields_and_image_text`.
  --sort-by {date,interaction_rate,overperforming,total_interactions,underperforming}
                                                  The order in which to retrieve posts. Defaults to `date`.
  --start-date START_DATE                         The earliest date at which a post could be posted (UTC!). You can pass just a year or a year-month for convenience.
  --types TYPES                                   Types of post to include, separated by comma.

examples:

. Fetching all the 2021 posts containing the words 'acetylsalicylic acid':
    `minet ct search 'acetylsalicylic acid' --start-date 2021-01-01 --token YOUR_TOKEN > posts.csv`

```

### summary

```
usage: minet crowdtangle summary [-h] [--rate-limit RATE_LIMIT] [-o OUTPUT]
                                 [-t TOKEN] [-p PLATFORMS] [--posts POSTS]
                                 [-s SELECT]
                                 [--sort-by {date,subscriber_count,total_interactions}]
                                 [--start-date START_DATE] [--total TOTAL]
                                 column [file]

Minet CrowdTangle Link Summary Command
======================================

Retrieve aggregated statistics about link sharing on the Crowdtangle API and by platform.

For more information, see the API endpoint documentation: https://github.com/CrowdTangle/API/wiki/Links.

positional arguments:
  column                                          Name of the column containing the URL in the CSV file.
  file                                            CSV file containing the inquired URLs.

optional arguments:
  -h, --help                                      show this help message and exit
  --rate-limit RATE_LIMIT                         Authorized number of hits by minutes. Defaults to 6. Rcfile key: crowdtangle.rate_limit
  -o OUTPUT, --output OUTPUT                      Path to the output file. By default, everything will be printed to stdout.
  -t TOKEN, --token TOKEN                         CrowdTangle dashboard API token. Rcfile key: crowdtangle.token
  -p PLATFORMS, --platforms PLATFORMS             The platforms from which to retrieve links (facebook, instagram, or reddit). This value can be comma-separated.
  --posts POSTS                                   Path to a file containing the retrieved posts.
  -s SELECT, --select SELECT                      Columns to include in report (separated by `,`).
  --sort-by {date,subscriber_count,total_interactions}
                                                  How to sort retrieved posts. Defaults to `date`.
  --start-date START_DATE                         The earliest date at which a post could be posted (UTC!). You can pass just a year or a year-month for convenience.
  --total TOTAL                                   Total number of HTML documents. Necessary if you want to display a finite progress indicator.

examples:

. Computing a summary of aggregated stats for urls contained in a CSV row:
    `minet ct summary url urls.csv --token YOUR_TOKEN --start-date 2019-01-01 > summary.csv`

```

## Facebook

```
usage: minet facebook [-h] {comments,post-stats,url-likes} ...

Minet Facebook Command
======================

Collects data from Facebook.

optional arguments:
  -h, --help                       show this help message and exit

actions:
  {comments,post-stats,url-likes}  Action to perform to collect data on Facebook

```

<h3 id="facebook-comments">comments</h3>

```
usage: minet facebook comments [-h] [-c COOKIE] [-o OUTPUT] [-s SELECT]
                               column [file]

Minet Facebook Comments Command
===============================

Scrape series of comments on Facebook.

positional arguments:
  column                      Column of the CSV file containing post urls or a single post url to fetch.
  file                        CSV file containing the post urls.

optional arguments:
  -h, --help                  show this help message and exit
  -c COOKIE, --cookie COOKIE  Authenticated cookie to use or browser from which to extract it (supports "firefox", "chrome", "chromium", "opera" and "edge"). Defaults to "firefox".
  -o OUTPUT, --output OUTPUT  Path to the output report file. By default, the report will be printed to stdout.
  -s SELECT, --select SELECT  Columns to include in report (separated by `,`).

examples:

. Fetching a post's comments:
    `minet fb comments -c firefox https://www.facebook.com/page/posts/3601645349798293 > comments.csv`

```

<h3 id="facebook-url-likes">url-likes</h3>

```
usage: minet facebook url-likes [-h] [-o OUTPUT] [-s SELECT] [--total TOTAL]
                                column [file]

Minet Facebook Url Likes Command
================================

Retrieve the approximate number of Facebook 'likes' about a given list of URLs.
It is obtained by scraping Facebook's like button, but it is approximate:
"1.2K people like this."
The number does not actually correspond to the number of like reactions, but rather to
the sum of like, love, 'ahah', angry, etc, reactions plus the number of comments and shares
that the URL generated on Facebook.

positional arguments:
  column                      Name of the column containing the URL in the CSV file or a single url.
  file                        CSV file containing the inquired URLs.

optional arguments:
  -h, --help                  show this help message and exit
  -o OUTPUT, --output OUTPUT  Path to the output report file. By default, the report will be printed to stdout.
  -s SELECT, --select SELECT  Columns to include in report (separated by `,`).
  --total TOTAL               Total number of lines in CSV file. Necessary if you want to display a finite progress indicator.

example:
. `minet fb url-likes url url.csv > url_likes.csv`
```

## Hyphe

### dump

```
usage: minet hyphe dump [-h] [-d OUTPUT_DIR] [--body] url corpus

Minet Hyphe Dump Command
========================

Command dumping page-level information from a given
Hyphe corpus.

positional arguments:
  url                                     Url of the Hyphe API.
  corpus                                  Id of the corpus.

optional arguments:
  -h, --help                              show this help message and exit
  -d OUTPUT_DIR, --output-dir OUTPUT_DIR  Output directory for dumped files. Will default to some name based on corpus name.
  --body                                  Whether to download pages body.

examples:

. Dumping a corpus into the ./corpus directory:
    `minet hyphe dump http://myhyphe.com/api/ corpus-name -d corpus`

```

## Mediacloud

<h3 id="mc-medias">medias</h3>

```
usage: minet mediacloud medias [-h] [-t TOKEN] [-o OUTPUT] [--feeds FEEDS]
                               [-s SELECT] [--total TOTAL]
                               column [file]

Minet Mediacloud Medias Command
===============================

Retrieve metadata about a list of Mediacloud medias.

positional arguments:
  column                      Name of the column containing the Mediacloud media ids.
  file                        CSV file containing the searched Mediacloud media ids.

optional arguments:
  -h, --help                  show this help message and exit
  -t TOKEN, --token TOKEN     Mediacloud API token (also called key).
  -o OUTPUT, --output OUTPUT  Path to the output file. By default, the output will be printed to stdout.
  --feeds FEEDS               If given, path of the CSV file listing media RSS feeds.
  -s SELECT, --select SELECT  Columns to include in report (separated by `,`).
  --total TOTAL               Total number of medias. Necessary if you want to display a finite progress indicator.

```

<h3 id="mc-search">search</h3>

```
usage: minet mediacloud search [-h] [-t TOKEN] [-o OUTPUT] [-c COLLECTIONS]
                               [--skip-count]
                               query

Minet Mediacloud Search Command
===============================

Search stories on the Mediacloud platform.

positional arguments:
  query                                      Search query.

optional arguments:
  -h, --help                                 show this help message and exit
  -t TOKEN, --token TOKEN                    Mediacloud API token (also called key).
  -o OUTPUT, --output OUTPUT                 Path to the output file. By default, the output will be printed to stdout.
  -c COLLECTIONS, --collections COLLECTIONS  List of searched collections separated by commas.
  --skip-count                               Whether to skip the first API call counting the number of posts for the progress bar.

```

### topic

#### stories

```
usage: minet mediacloud topic stories [-h] [-t TOKEN] [-o OUTPUT]
                                      [--media-id MEDIA_ID]
                                      [--from-media-id FROM_MEDIA_ID]
                                      topic_id

Minet Mediacloud Topic Stories Command
======================================

Retrieves the list of stories from a mediacloud topic.

positional arguments:
  topic_id                       Id of the topic.

optional arguments:
  -h, --help                     show this help message and exit
  -t TOKEN, --token TOKEN        Mediacloud API token (also called key).
  -o OUTPUT, --output OUTPUT     Path to the output file. By default, the output will be printed to stdout.
  --media-id MEDIA_ID            Return only stories belonging to the given media_ids.
  --from-media-id FROM_MEDIA_ID  Return only stories that are linked from stories in the given media_id.

```

## Twitter

### followers

```
usage: minet twitter followers [-h] [--api-key API_KEY]
                               [--api-secret-key API_SECRET_KEY]
                               [--access-token ACCESS_TOKEN]
                               [--access-token-secret ACCESS_TOKEN_SECRET]
                               [--id] [-o OUTPUT] [-s SELECT] [--resume]
                               [--total TOTAL]
                               column [file]

Minet Twitter Followers Command
===============================

Retrieve followers of given user.

positional arguments:
  column                                     Name of the column containing the Twitter account screen names.
  file                                       CSV file containing the inquired Twitter users.

optional arguments:
  -h, --help                                 show this help message and exit
  --api-key API_KEY                          Twitter API key.
  --api-secret-key API_SECRET_KEY            Twitter API secret key.
  --access-token ACCESS_TOKEN                Twitter API access token.
  --access-token-secret ACCESS_TOKEN_SECRET  Twitter API access token secret.
  --id                                       Whether to use Twitter user ids rather than screen names.
  -o OUTPUT, --output OUTPUT                 Path to the output file. By default, the result will be printed to stdout.
  -s SELECT, --select SELECT                 Columns to include in report (separated by `,`).
  --resume                                   Whether to resume an aborted collection.
  --total TOTAL                              Total number of accounts. Necessary if you want to display a finite progress indicator.

examples:

. Getting followers of a list of user:
    `minet tw followers screen_name users.csv > followers.csv`

```

### friends

```
usage: minet twitter friends [-h] [--api-key API_KEY]
                             [--api-secret-key API_SECRET_KEY]
                             [--access-token ACCESS_TOKEN]
                             [--access-token-secret ACCESS_TOKEN_SECRET] [--id]
                             [-o OUTPUT] [-s SELECT] [--resume] [--total TOTAL]
                             column [file]

Minet Twitter Friends Command
=============================

Retrieve friends, i.e. followed users, of given user.

positional arguments:
  column                                     Name of the column containing the Twitter account screen names.
  file                                       CSV file containing the inquired Twitter users.

optional arguments:
  -h, --help                                 show this help message and exit
  --api-key API_KEY                          Twitter API key.
  --api-secret-key API_SECRET_KEY            Twitter API secret key.
  --access-token ACCESS_TOKEN                Twitter API access token.
  --access-token-secret ACCESS_TOKEN_SECRET  Twitter API access token secret.
  --id                                       Whether to use Twitter user ids rather than screen names.
  -o OUTPUT, --output OUTPUT                 Path to the output file. By default, the result will be printed to stdout.
  -s SELECT, --select SELECT                 Columns to include in report (separated by `,`).
  --resume                                   Whether to resume an aborted collection.
  --total TOTAL                              Total number of accounts. Necessary if you want to display a finite progress indicator.

examples:

. Getting friends of a list of user:
    `minet tw friends screen_name users.csv > friends.csv`

```

<h3 id="twitter-scrape">scrape</h3>

```
usage: minet twitter scrape [-h] [--include-refs] [-l LIMIT] [-o OUTPUT]
                            [--query-template QUERY_TEMPLATE] [-s SELECT]
                            {tweets} query [file]

Minet Twitter Scrape Command
============================

Scrape Twitter's public facing search API to collect tweets etc.

positional arguments:
  {tweets}                         What to scrape. Currently only `tweets` is possible.
  query                            Search query or name of the column containing queries to run in given CSV file.
  file                             Optional CSV file containing the queries to be run.

optional arguments:
  -h, --help                       show this help message and exit
  --include-refs                   Whether to emit referenced tweets (quoted, retweeted & replied) in the CSV output. Note that it consumes a memory proportional to the total number of unique tweets retrieved.
  -l LIMIT, --limit LIMIT          Maximum number of tweets to collect per query.
  -o OUTPUT, --output OUTPUT       Path to the output file. By default, the result will be printed to stdout.
  --query-template QUERY_TEMPLATE  Query template. Can be useful for instance to change a column of twitter user screen names into from:@user queries.
  -s SELECT, --select SELECT       Columns to include in report (separated by `,`).

examples:

. Collecting the latest 500 tweets of a given Twitter user:
    `minet tw scrape tweets "from:@jack" --limit 500 > tweets.csv`

. Collecting the tweets from multiple Twitter queries listed in a CSV file:
    `minet tw scrape tweets query queries.csv > tweets.csv`

. Templating the given CSV column to query tweets by users:
    `minet tw scrape tweets user users.csv --query-template 'from:@{value}' > tweets.csv`

```

### users

```
usage: minet twitter users [-h] [--api-key API_KEY]
                           [--api-secret-key API_SECRET_KEY]
                           [--access-token ACCESS_TOKEN]
                           [--access-token-secret ACCESS_TOKEN_SECRET] [--id]
                           [-o OUTPUT] [-s SELECT] [--resume] [--total TOTAL]
                           column [file]

Minet Twitter Users Command
===========================

Retrieve metadata from a given user.

positional arguments:
  column                                     Name of the column containing the Twitter account screen names.
  file                                       CSV file containing the inquired Twitter users.

optional arguments:
  -h, --help                                 show this help message and exit
  --api-key API_KEY                          Twitter API key.
  --api-secret-key API_SECRET_KEY            Twitter API secret key.
  --access-token ACCESS_TOKEN                Twitter API access token.
  --access-token-secret ACCESS_TOKEN_SECRET  Twitter API access token secret.
  --id                                       Whether to use Twitter user ids rather than screen names.
  -o OUTPUT, --output OUTPUT                 Path to the output file. By default, the result will be printed to stdout.
  -s SELECT, --select SELECT                 Columns to include in report (separated by `,`).
  --resume                                   Whether to resume an aborted collection.
  --total TOTAL                              Total number of accounts. Necessary if you want to display a finite progress indicator.

examples:

. Getting metadata from an user:
    `minet tw users screen_name users.csv > data_users.csv`

```

## Youtube

### captions

```
usage: minet youtube captions [-h] [-o OUTPUT] [-s SELECT] [--lang LANG]
                              column [file]

Youtube captions
================

Retrieve metadata about Youtube captions.

positional arguments:
  column                      Name of the column containing the video's url or id.
  file                        CSV file containing the Youtube videos urls or ids.

optional arguments:
  -h, --help                  show this help message and exit
  -o OUTPUT, --output OUTPUT  Path to the output report file. By default, the report will be printed to stdout.
  -s SELECT, --select SELECT  Columns to include in report (separated by `,`).
  --lang LANG                 Language (ISO code like "fr") of captions to retrieve.

```

<h3 id="youtube-comments">comments</h3>

```
usage: minet youtube comments [-h] [-o OUTPUT] [-f] [-k KEY] [-s SELECT]
                              column [file]

Youtube comments
================

Retrieve metadata about Youtube comments using the API.

positional arguments:
  column                      This argument can either take the name of the column containing the video's id/url if a file is passed as an argument, or a single youtube video's id/url if there is no file 
  file                        CSV file containing the Youtube videos ids.

optional arguments:
  -h, --help                  show this help message and exit
  -o OUTPUT, --output OUTPUT  Path to the output report file. By default, the report will be printed to stdout.
  -f, --full                  YouTube API does not always return every comments as some replies can be omitted. By adding this flag, one ensures to make every needed API call to retrieve all the comments.
  -k KEY, --key KEY           YouTube API Data dashboard API key.
  -s SELECT, --select SELECT  Columns to include in report (separated by `,`).

example:

. Fetching a video's comments:
    `minet yt comments https://www.youtube.com/watch?v=7JTb2vf1OQQ -k my-api-key --full -o comments.csv`

```

<h3 id="youtube-search">search</h3>

```
usage: minet youtube search [-h] [-o OUTPUT] [-k KEY] [-s SELECT] [-l LIMIT]
                            [--order {date,rating,relevance,title,videoCount,viewCount}]
                            column [file]

Youtube search
==============

Retrieve metadata about Youtube search field using the API.

positional arguments:
  column                                          This argument can either take the keyword on which we want to retrieve videos from the API or the name of the column containing that keyword
  file                                            CSV file containing the keyword for youtube Search.

optional arguments:
  -h, --help                                      show this help message and exit
  -o OUTPUT, --output OUTPUT                      Path to the output report file. By default, the report will be printed to stdout.
  -k KEY, --key KEY                               YouTube API Data dashboard API key.
  -s SELECT, --select SELECT                      Columns to include in report (separated by `,`).
  -l LIMIT, --limit LIMIT                         Maximum number of videos to retrieve.
  --order {date,rating,relevance,title,videoCount,viewCount}
                                                  Order in which videos are retrieved. The default one is relevance.

example:

. Searching videos about birds:
    `minet youtube search bird -k my-api-key > bird_videos.csv`

```

### videos

```
usage: minet youtube videos [-h] [-o OUTPUT] [-s SELECT] [-k KEY] column [file]

Youtube videos
==============

Retrieve metadata about Youtube videos using the API.

positional arguments:
  column                      Name of the column containing the video's url or id.
  file                        CSV file containing the Youtube videos urls or ids.

optional arguments:
  -h, --help                  show this help message and exit
  -o OUTPUT, --output OUTPUT  Path to the output report file. By default, the report will be printed to stdout.
  -s SELECT, --select SELECT  Columns to include in report (separated by `,`).
  -k KEY, --key KEY           YouTube API Data dashboard API key.

```

