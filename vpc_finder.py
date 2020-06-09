__author__ = 'Deborshi Choudhury'

import boto3
import sys
import csv
import argparse
from termcolor import colored

"""
Utility script - Find all vpcs, subnets & number of unused private IPv4 addresses of the subnet within a given AWS account, & write it to a csv file.
If the count of unused private IPv4 addresses of the subnet is less then 30, termcolor will highlight it with red.

This program takes two input arguments 1. AWS profile 2. File Name.

To Run this script please ensure you've got python3.6 & above
This script will take AWS profile & a file name as an argument and run through each regions. 

If there's only default profile please ensure you put "default" as an input parameter.

E.g. python3 vpc_finder.py -p dummyprofile -f dummy_file_out

"""


#########################
# Describe all regions
#########################
def describe_regions(session):
    try:
        aws_regions = []
        ec2_client = session.client('ec2')
        response_regions = ec2_client.describe_regions()['Regions']
        for region in response_regions:
            aws_regions.append(region['RegionName'])
        return aws_regions
    except Exception:
        print("Unexpected error:", sys.exc_info()[0])


#####################
# List all VPCs
#####################
def describe_vpc(ec2,aws_region,writer,profile_name):
    try:
        response_vpc = ec2.describe_vpcs()['Vpcs']
        for vpc in response_vpc:
            print('=' * 50)
            print(f"Found VPC in Region {aws_region}")
            count = 0
            filters = [
                {'Name': 'vpc-id',
                 'Values': [vpc['VpcId']]}
            ]
            print("Account:{}".format(vpc['OwnerId']))
            print("VpcId:{}, VpcCidr:{}, Region:{} ".format(vpc['VpcId'], vpc['CidrBlock'], aws_region))
            response_subnets = ec2.describe_subnets(Filters=filters)['Subnets']

            for subnets in response_subnets:
                if subnets['AvailableIpAddressCount'] < 30:
                    print("{} - Subnet:{}, SubnetId:{}, AvailableIPv4:{}, AvailabilityZone:{},".format(count,subnets['CidrBlock'],
                          colored(subnets['SubnetId'],"red", attrs=["bold"]),
                          colored(subnets['AvailableIpAddressCount'],"red", attrs=["bold"]),
                          subnets['AvailabilityZone']))
                else:
                    print("{} - Subnet:{}, SubnetId:{}, AvailableIPv4:{}, AvailabilityZone:{},".format(count,subnets['CidrBlock'],
                          colored(subnets['SubnetId'], "blue", attrs=["bold"]),
                          colored(subnets['AvailableIpAddressCount'],"blue", attrs=["bold"]),
                          subnets['AvailabilityZone']))
                count += 1

                writer.writerow({"Account": profile_name, "VpcId": vpc['VpcId'], "VpcCidr": vpc['CidrBlock'], "Region": aws_region,
                            "Subnet": subnets['CidrBlock'], "SubnetId": subnets['SubnetId'], "AvailableIPv4": subnets['AvailableIpAddressCount'],
                            "AvailabilityZone": subnets['AvailabilityZone']})
            print('='*50)
    except Exception:
        print("Unexpected error:", sys.exc_info()[0])


#####################
# Main Function
#####################
def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-p', '--profile', help="AWS profile name is required as an argument to run this command.")
        parser.add_argument("-f", "--filename", help="Please provide a file name without '.csv' extension.")
        if len(sys.argv) < 5:
            parser.print_help()
            sys.exit(0)
        args = parser.parse_args()

        session = boto3.session.Session(
            profile_name=args.profile
        )
        file_name = args.filename
        profile_name = args.profile
        with open(file_name + ".csv", "w", newline="") as csvfile:
            fieldnames = [
                "Account", "VpcId",
                "VpcCidr", "Region",
                "Subnet", "SubnetId",
                "AvailableIPv4",
                "AvailabilityZone"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            aws_regions = describe_regions(session)
            for aws_region in aws_regions:
                ec2 = session.client('ec2', region_name=aws_region)
                """ :type: pyboto3.ec2 """
                print("Scanning region: {}".format(aws_region))
                describe_vpc(ec2,aws_region, writer, profile_name)

    except Exception:
        print("Unexpected error:", sys.exc_info()[0])
        raise


if __name__ == "__main__":
    main()