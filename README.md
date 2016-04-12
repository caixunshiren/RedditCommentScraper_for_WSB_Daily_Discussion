# Reddit Comment Scraper

Scrape comments from a given thread on reddit.com using PRAW

## License
Copyright (c) Ian Hussey 2016 (ian.hussey@ugent.be)

Distributed under the MIT license.

## Version
1.0 (12/4/2016)

## Description
1. Scrapes all comments from a given reddit thread
2. Extracts top level comments
3. Saves to a csv file

## Known issues
None. 

## Notes
1. Although the script only uses publiclly available information, PRAW's call to the reddit API requires a reddit login (see line 44).
2. Reddit API limits number of calls (1 per second IIRC). For a large thread (e.g., 1000s of comments) script execution time may therefore be c.1 hour.
3. Does not extract comment creation date (or other properties), which might be useful. 


