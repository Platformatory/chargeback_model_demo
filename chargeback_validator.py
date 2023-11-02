import yaml
import argparse

# Define a sample YAML configuration with multiple clusters
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--chargeback_file_path", dest="chargeback_file_path", type=str)

args = parser.parse_args()


## Read the chargeback model details
chargeback_file_path = args.chargeback_file_path

def validate_cluster_config(cluster_config):
    """
    Validate an individual cluster configuration.
    """
    # Check if 'cluster_name' and 'cluster_id' exist and are non-empty
    if 'cluster_name' in cluster_config and cluster_config['cluster_name'] and 'cluster_id' in cluster_config and cluster_config['cluster_id']:
        print(f"Validating cluster: {cluster_config['cluster_name']} ({cluster_config['cluster_id']})")

        ## Check if 'currency_mode' is present
        if not 'currency_code' in cluster_config:
            print("Missing 'currency_code' in cluster config.")

        ## Check if 'throughput_units' is present
        if 'throughput_units' in cluster_config:
            if isinstance(cluster_config['throughput_units'], str) and cluster_config['throughput_units'] in ['records', 'bytes']:
                print(f"Valid 'throughput_units' value")
            else:
                print(f"Invalid 'throughput_units' value. Has to be one of 'records' or 'bytes'")
        else:
            print("Missing 'throughput_units' in cluster config.")

        # Check for 'total_capacity' and 'chargeback_model'
        if 'total_capacity' in cluster_config and 'chargeback_model' in cluster_config and 'chargeback_config' in cluster_config:
            total_capacity = cluster_config['total_capacity']
            chargeback_model = cluster_config['chargeback_model']
            chargeback_config = cluster_config["chargeback_config"]

            # Check the chargeback model type and validate accordingly
            if chargeback_model == 'cost_center':
                ## Check if 'total_costs' is present
                if not 'total_costs' in cluster_config:
                    print("Missing 'total_costs' in cluster config.")
                validate_cost_center_model(total_capacity, chargeback_config)
            elif chargeback_model == 'fair_share':
                validate_fair_share_model(total_capacity, chargeback_config)
            elif chargeback_model == 'usage_based':
                validate_usage_based_model(total_capacity, chargeback_config)
            elif chargeback_model == 'client_usage_based':
                validate_client_usage_based_model(total_capacity, chargeback_config)
            else:
                print("Invalid chargeback_model type.")
        else:
            print("Missing 'total_capacity' or 'chargeback_model' or 'chargeback_config' in cluster config.")
    else:
        print("Missing 'cluster_name' or 'cluster_id' in cluster config.")

def validate_chargeback_config(chargeback_config):
    """
    Validate chargeback model within a cluster.
    """
    if isinstance(chargeback_config, dict):
        
        # Check for required parameters based on usage_model
        throughput_unit_rate = chargeback_config.get('throughput_unit_rate')
        partition_unit_rate = chargeback_config.get('partition_unit_rate')
        storage_unit_rate = chargeback_config.get('storage_unit_rate')
        
        if isinstance(throughput_unit_rate, float):
            print(f"Valid 'throughput_unit_rate' value")
        else:
            print("Invalid 'throughput_unit_rate' value")
        
        if isinstance(partition_unit_rate, float):
            print(f"Valid 'partition_unit_rate' value")
        else:
            print("Invalid 'partition_unit_rate' value")

        if isinstance(storage_unit_rate, float):
            print(f"Valid 'storage_unit_rate' value")
        else:
            print("Invalid 'storage_unit_rate' value")
        
        return True

    else:
        return False


def validate_cost_center_model(total_capacity, chargeback_config):
    """
    Validate "cost_center" chargeback model within a cluster.
    """
    if isinstance(total_capacity, dict):
        # Cost Center model does not require additional validation
        if 'throughput_tps' in total_capacity and isinstance(total_capacity['throughput_tps'], int):
            print(f"Valid 'throughput_tps' value")
        else:
            print(f"Invalid 'throughput_tps' value")
        
        if 'partitions_max' in total_capacity and isinstance(total_capacity['partitions_max'], int):
            print(f"Valid 'partitions_max' value")
        else:
            print(f"Invalid 'partitions_max' value") 
        
        if 'storage' in total_capacity and isinstance(total_capacity['storage'], int):
            print(f"Valid 'storage' value")
        else:
            print(f"Invalid 'storage' value") 
    
    valid = validate_chargeback_config(chargeback_config)
    if not valid:
        print("Invalid 'chargeback_config' value in 'cost_center' model.")

def validate_fair_share_model(total_capacity, chargeback_config):
    """
    Validate "fair_share" chargeback model within a cluster.
    """
    valid = validate_chargeback_config(chargeback_config)
    if not valid:
        print("Invalid 'chargeback_config' value in 'fair_share' model.")

def validate_usage_based_model(total_capacity, chargeback_config):
    """
    Validate "usage_based" chargeback model within a cluster.
    """
    valid = validate_chargeback_config(chargeback_config)
    if not valid:
        print("Invalid 'chargeback_config' value in 'usage_based' model.")

def validate_client_usage_based_model(total_capacity, chargeback_config):
    """
    Validate "client_usage_based" chargeback model within a cluster.
    """
    if isinstance(chargeback_config, dict):
        
        # Check for required parameters based on usage_model
        usage_model = chargeback_config.get('usage_model')
        throughput_in_unit_rate = chargeback_config.get('throughput_in_unit_rate')
        throughput_out_unit_rate = chargeback_config.get('throughput_out_unit_rate')
        
        if usage_model in ['producer_pays', 'consumer_pays', 'producer_consumer_pays']:
            # Depending on the usage_model, additional parameters may be required
            if usage_model == 'producer_pays':
                
                if isinstance(throughput_in_unit_rate, float):
                    print(f"Valid 'client_usage_based' model with usage_model: {usage_model}")
                else:
                    print("Invalid 'throughput_in_unit_rate' value.")
            
            elif usage_model == 'consumer_pays':
                if isinstance(throughput_out_unit_rate, float):
                    print(f"Valid 'client_usage_based' model with usage_model: {usage_model}")
                else:
                    print("Invalid 'throughput_out_unit_rate' value.")
            
            else:
                if isinstance(throughput_out_unit_rate, float) and isinstance(throughput_in_unit_rate, float):
                    print(f"Valid 'client_usage_based' model with usage_model: {usage_model}")
                else:
                    print("Invalid 'throughput_in_unit_rate' or/and 'throughput_out_unit_rate' values.")
        else:
            print("Invalid 'usage_model' value in 'client_usage_based' model.")
    else:
        print("Invalid 'chargeback_config' value in 'client_usage_based' model.")



with open(chargeback_file_path, "r") as f:
    yaml_config = f.read()

# Load the YAML configuration
config = yaml.safe_load(yaml_config)
# pprint(config)


# Iterate through clusters and validate each one
for cluster in config.get('clusters', []):
    for cluster_config_key in cluster.keys():
        validate_cluster_config(cluster[cluster_config_key])

    