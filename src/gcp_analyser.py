from google.cloud import iam_v1, storage
import os
import csv

def get_all_iam_members(project_id):
    """Fetches all IAM members for a given GCP project."""
    client = iam_v1.IAMPolicyClient()
    policy = client.get_iam_policy(resource=project_id)
    return policy.bindings

def get_member_roles(member, bindings):
    """Fetches roles for a given IAM member."""
    roles = []
    for binding in bindings:
        if member in binding.members:
            roles.append(binding.role)
    return roles

def get_role_permissions(role_name):
    """Fetches permissions associated with a role."""
    # Placeholder: Fetch permissions associated with a role in GCP.
    return []

def run_analysis(project_id):
    print("Running GCP Analysis...")
    users_data = []

    bindings = get_all_iam_members(project_id)
    
    for binding in bindings:
        for member in binding.members:
            roles = get_member_roles(member, bindings)
            resources = set()

            for role in roles:
                role_permissions = get_role_permissions(role)
                resources.update(role_permissions)

            user_data = {
                'Name': member,
                'Accounts': project_id,  # This will list the project ID; consider replacing with a descriptive name if needed.
                'Policies': ', '.join(roles),
                'Resources': ', '.join(resources)
            }
            users_data.append(user_data)

    # Save to CSV
    output_path = os.path.join('outputs', 'gcp_users.csv')
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Name', 'Accounts', 'Policies', 'Resources']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for user_data in users_data:
            writer.writerow(user_data)

    print(f"Analysis completed. Results saved to {output_path}")

