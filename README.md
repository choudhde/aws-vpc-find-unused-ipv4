## aws-vpc-find-unused-ipv4

#### Description:  
<p> This utility script finds all VPCs, subnets, & unused private IPv4 addresses of a subnet, of a given aws account, across all the regions that are enabled for the account, and writes to a csv file. This is useful when you want to check how many unused IPv4 addresses are leftover for you to allocate any more resources, or adjust your autoscaling group accordingly.</p>

<p>This script takes two input arguments 1. AWS profile name 2. File name. If there's only default profile please ensure you put "default" as an input parameter.</p>

<p>From the terminal - python3 vpc_finder.py -p dummy_profile -f dummy_file_out. </p>
<p>Requirements - Python 3.x runtime</p>
