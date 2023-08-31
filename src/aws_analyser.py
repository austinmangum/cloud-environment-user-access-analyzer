import boto3
import csv
import os

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

def get_policy_resources(policy_arn):
    """Fetches resources and permissions for a given policy."""
    iam = boto3.client('iam')
    policy = iam.get_policy_version(
        PolicyArn=policy_arn,
        VersionId='v1'  # This is a placeholder; actual version may vary.
    )
    # TODO: Extract resources and permissions from the policy document.
    return []

def run_analysis():
    print("Running AWS Analysis...")
    users_data = []

    users = get_all_iam_users()
    for user in users:
        username = user['UserName']
        
        # Fetch policies
        policies = get_user_policies(username)
        policy_names = []
        resources = set()

        for policy in policies:
            policy_name = policy['PolicyName']
            policy_arn = policy['PolicyArn']

            policy_names.append(policy_name)

            # Fetch resources
            policy_resources = get_policy_resources(policy_arn)
            resources.update(policy_resources)

        user_data = {
            'Name': username,
            'Accounts': 'Main-Account',  # Placeholder. Actual logic to fetch account name(s) should replace this.
            'Policies': ', '.join(policy_names),
            'Resources': ', '.join(resources)
        }
        users_data.append(user_data)

    # Save to CSV
    output_path = os.path.join('outputs', 'aws_users.csv')
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Name', 'Accounts', 'Policies', 'Resources']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for user_data in users_data:
            writer.writerow(user_data)

    print(f"Analysis completed. Results saved to {output_path}")
