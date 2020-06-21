# MatchingEngines
A project to write matching engines, potentially in multiple languages

## Python

A simple, single threaded matching engine. For each instrument an OrderBook is created and orders are matched internally.
Mutability is leaned on heavily here.

Performance:
| Number Of Orders | Total Time (secs) | Time Per Order (microsecs) |
|------------------|-------------------|----------------------------|
|10,000|0.113|11.3|
|100,000|1.370|13.7|
|1,000,000|13.5|13.5|

Around half this time (7.95 microseconds per order) is spend on matching, with the rest spent on filling the order book.

#### TODO:
Add cancel / amend functionality.
Add opening / closing auctions.
Add more order types.
