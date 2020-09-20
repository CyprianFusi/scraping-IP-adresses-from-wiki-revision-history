Crawling and Scraping IP Addresses from Wikipedia Revision History Pages
========================================================================
Those who edit the contents of Wikipedia leave behind their names. If they don't indicate their names the IP addresses from where the revision was done is indicated instead. The editor's device identification number may also be indicated in some situations.

Links on Wikipedia mostly start with '/wiki/<title of article>', without the root url. For example /wiki/Python_(programming_language).
The revision history page on the other hand has the format https://en.wikipedia.org/w/index.php?title=<Title_in_URL>&action=history.

This script would kick off with a sample article link, extract the title of the article from a link and build a revision history url and move on to extract or scrape more article links and the IP addresses from the page. It then selects a new link at random from the list of scraped links, extracts the title, builds a new revision history link and repeat the process (the crawling) until the user interrupts by pressing CTR-C or when Python hits its maximum iteration.

We use IP Geolocation API to match the scraped IP addresses to some location parameters like country and city. The IP addresses can also be mapped to longitudes and latitudes which can be used to pin the location on Google map!

This can find applications in security, that is, to track down malicious individuals who might be using gadgets on the internet but believing that they are invisible :)!

I made use of knowledge gained from Web Scraping with Python by Ryan Mitchell