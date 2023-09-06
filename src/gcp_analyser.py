from googleapiclient import discovery
from google.auth import default
import csv
import os
# I am struggling to pull my project ID from default. meed to stroubleshoot more
def get_project_id():
    creds, project_id = default()
    project_id = "url-mapper"
    print(f"Project ID: {project_id}")  # Add this line to debug
    print(f"creds: {creds}")  # Add this line to debug
    return project_id
#project_id = 'url-mapper'

#def get_current_project():
#    """Fetches the current GCP project ID."""
#    creds, project_id = default()
#    return project_id

def get_all_gcp_users(project_id, creds):
    """Fetches all GCP IAM members."""
    service = discovery.build('cloudresourcemanager', 'v1', credentials=creds)
    policy = service.projects().getIamPolicy(resource= project_id, body={}).execute()
    return [binding['members'] for binding in policy['bindings']]

def get_user_policies(username, project_id, creds):
    """Fetches attached policies for a given GCP IAM member."""
    service = discovery.build('cloudresourcemanager', 'v1', credentials=creds)
    policy = service.projects().getIamPolicy(resource= project_id, body={}).execute()
    user_policies = [binding for binding in policy['bindings'] if username in binding['members']]
    return user_policies

def get_project_name(project_id, creds):
    """Fetches the project name using project ID."""
    service = discovery.build('cloudresourcemanager', 'v1', credentials=creds)
    project = service.projects().get(projectId=project_id).execute()
    return project['name']

def run_analysis():
    print("Running GCP Analysis...")
    #project_id = get_project_id()  # Add this line to get the project ID
    users_data = []
    creds, project_id = default()
    project_name = get_project_name(project_id, creds)

    users = get_all_gcp_users(project_id, creds)
    for user_list in users:
        for user in user_list:
            username = user

            user_policies = get_user_policies(username, project_id, creds)
            details = []

            for policy in user_policies:
                policy_details = policy['role']
                details.append(f"{policy['role']}:{', '.join(policy['members'])}")

            user_data = {
                'Name': username,
                'Projects': project_name,
                'Policies': ', '.join([policy['role'] for policy in user_policies]),
                'Details': ', '.join(details)
            }
            users_data.append(user_data)

    # Save to CSV
    output_path = os.path.join('outputs', 'gcp_users.csv')
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Name', 'Projects', 'Policies', 'Details']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for user_data in users_data:
            writer.writerow(user_data)

    print(f"Analysis completed. Results saved to {output_path}")

# Make sure the 'outputs' directory exists
if not os.path.exists('outputs'):
    os.makedirs('outputs')

run_analysis()
