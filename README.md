# MatchingEngines
A project to write matching engines, potentially in multiple languages.

## Python

A simple matching engine. For each instrument an OrderBook is created and orders are matched internally.
Mutability is leaned on heavily here. We match multiple instruments with random prices + quantities.

Performance of matching limit and market orders:
| Number Of Orders | Total Time (s) | Time Per Order (&mu;s) | Percentage Matched |
|------------------|----------------|------------------------| ---------- |
|10,000|0.11|11.3| 99.67%
|100,000|1.20|12.0| 99.85%
|1,000,000|14.28|14.3| 99.94%
|5,000,000|74.02|14.8| 99.97%


These times include filling each order book.
The matching engine has all orders pre-loaded into a list, but dispatches them to the relevant order book when "turned on". We 
measure the time from when it was turned on.


Performance of cancelling orders:
| Number Of Orders | Number Of Cancels | Total Time (s) | Time Per Order-Cancel pair (&mu;s) | Est time per Cancel (&mu;s) | Percentage Cancelled |
|------------------|----------------|----------------|------------------------| ---------- |---------- |
|10,000|10,000|0.33|32.5|21.2| 80.13%
|100,000|100,000|3.37|33.7|21.27| 80.20%
|1,000,000|1,000,000|35.66|35.66|21.36| 80.17%

By this point the limitations of my pure python implementation are becoming clear.
