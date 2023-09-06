import boto3
import csv
import os

def get_account_alias():
    """Fetches the account alias of the AWS account."""
    iam = boto3.client('iam')
    account_aliases = iam.list_account_aliases()
    if account_aliases['AccountAliases']:
        return account_aliases['AccountAliases'][0]
    else:
        return "Unknown_Account"

def get_all_iam_users():
    """Fetches all IAM users."""
    iam = boto3.client('iam')
    users = iam.list_users()
    return users.get('Users', [])

def get_user_policies(username):
    """Fetches attached policies for a given IAM user."""
    iam = boto3.client('iam')
    policies = iam.list_attached_user_policies(UserName=username)
    return policies.get('AttachedPolicies', [])

def get_group_policies(group_name):
    """Fetches attached policies for a given IAM group."""
    iam = boto3.client('iam')
    policies = iam.list_attached_group_policies(GroupName=group_name)
    return policies.get('AttachedPolicies', [])

def get_user_groups(username):
    """Fetches groups for a given IAM user."""
    iam = boto3.client('iam')
    groups = iam.list_groups_for_user(UserName=username)
    return [group['GroupName'] for group in groups.get('Groups', [])]

def get_policy_details(policy_arn):
    """Fetches details and permissions for a given policy."""
    try:
        iam = boto3.client('iam')
        policy_version = iam.get_policy(PolicyArn=policy_arn)['Policy']['DefaultVersionId']
        policy_document = iam.get_policy_version(PolicyArn=policy_arn, VersionId=policy_version)['PolicyVersion']['Document']

        permissions = []
        if 'Statement' in policy_document:
            for statement in policy_document['Statement']:
                if 'Action' in statement:
                    if isinstance(statement['Action'], list):
                        permissions.extend(statement['Action'])
                    else:
                        permissions.append(statement['Action'])

        return permissions
    except Exception as e:
        return str(e)

def run_analysis():
    print("Running AWS Analysis...")
    users_data = []
    account_alias = get_account_alias()
    users = get_all_iam_users()
    for user in users:
        username = user['UserName']
        user_policies = get_user_policies(username)
        groups = get_user_groups(username)

        details = []

        for policy in user_policies:
            policy_name = policy['PolicyName']
            policy_arn = policy['PolicyArn']
            policy_details = get_policy_details(policy_arn)
            
            if isinstance(policy_details, list):
                details.extend([f"{policy_name}:{detail}" for detail in policy_details])

        for group in groups:
            group_policies = get_group_policies(group)
            
            for group_policy in group_policies:
                group_policy_arn = group_policy['PolicyArn']
                group_policy_details = get_policy_details(group_policy_arn)

                if isinstance(group_policy_details, list):
                    details.extend([f"{group}:{detail}" for detail in group_policy_details])

        user_data = {
            'Name': username,
            'Account': account_alias,
            'Groups': ', '.join(groups),
            'Policies': ', '.join([policy['PolicyName'] for policy in user_policies]),
            'Details': ', '.join(details)
        }
        users_data.append(user_data)

    # Save to CSV
    output_path = os.path.join('outputs', f'{account_alias}_aws_users.csv')
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Name', 'Account', 'Groups', 'Policies', 'Details']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for user_data in users_data:
            writer.writerow(user_data)

    print(f"Analysis completed. Results saved to {output_path}")

# Make sure the 'outputs' directory exists
if not os.path.exists('outputs'):
    os.makedirs('outputs')

run_analysis()
