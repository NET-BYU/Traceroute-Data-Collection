# Untitled

Created: November 18, 2022 10:35 PM
Last Updated: November 18, 2022 10:50 PM

# Change of Location Detection (CoLD)

This system can detect the difference between traceroute data taken from different locations.

## Traceroute Collection

To collect traceroute data from the system you are on to all of the IP addresses in Input.json run dataCollection/dataCollection.py

#ToDo: Explain this

## Analysis

In order to get a bunch of .csv files formatted like this:

|  | IP 1 | IP 2 | IP 3 | IP 4 | IP 5 |
| --- | --- | --- | --- | --- | --- |
| time 1 | % | % | % | % | % |
| time 2 | % | % | % | % | % |

The name of the IP address will let you know which IP address it is comparing against, the IP addresses in the rows are the IP addresses it is comparing from which time range. When the IP in the column heading is the same as the file name a perfect score would be 100%. When they are different a perfect score would be 0%.

#ToDo: make this so much better then it is. Also explain the rest of how everything works.