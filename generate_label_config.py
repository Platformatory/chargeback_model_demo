import yaml
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--chargecode_file_path", dest="chargecode_file_path", type=str)
parser.add_argument("-m", "--chargeback_file_path", dest="chargeback_file_path", type=str)

args = parser.parse_args()

## Read the chargecode details
chargecode_file_path = args.chargecode_file_path

with open(chargecode_file_path, "r") as f:
    chargecode_yaml_config = f.read()

chargecode_config = yaml.safe_load(chargecode_yaml_config)

## Read the chargeback model details
chargeback_file_path = args.chargeback_file_path

with open(chargeback_file_path, "r") as f:
    chargeback_yaml_config = f.read()

chargeback_config = yaml.safe_load(chargeback_yaml_config)

# print(chargecode_config)

metric_label_str = """
    metric_relabel_configs:
"""

metric_label_template = """
      - source_labels: ['cluster', '$resource']
        separator: '_'
        target_label: chargecode
        regex: '$regex'
        replacement: '$chargecode'
"""


for cluster in chargeback_config.get('clusters', []):
    for cluster_config_key in cluster.keys():
        cluster_details = cluster[cluster_config_key]
        for chargecode in chargecode_config.get('chargecodes', []):
            chargecode_name = chargecode["chargecode_name"]
            target_cluster = chargecode["target_cluster"]
            match_config_list = chargecode["match_config"]

            if target_cluster == cluster_details["cluster_name"]:
                if cluster_details["chargeback_model"] == "usage_based":
                    resource = "topic"
                    for match_config in match_config_list:
                        if match_config["entity"] == resource:
                            if match_config["match_type"] == "literal":
                                regex = "^{0}_{1}$".format(target_cluster, match_config["match_expression"])
                            elif match_config["match_type"] == "prefix":
                                regex = "^{0}_{1}(.*)$".format(target_cluster, match_config["match_expression"])
                            elif match_config["match_type"] == "regex":
                                regex = "^{0}_{1}$".format(target_cluster, str(match_config["match_expression"]).replace("^", "").replace("$", ""))
                            metric_label = metric_label_template.replace("$resource", resource).replace("$regex", regex).replace("$chargecode", chargecode_name)
                            metric_label_str = metric_label_str + metric_label
                elif cluster_details["chargeback_model"] == "cost_center":
                    resource = "topic"
                    for match_config in match_config_list:
                        if match_config["entity"] == resource:
                            if match_config["match_type"] == "literal":
                                regex = "^{0}_{1}$".format(target_cluster, match_config["match_expression"])
                            elif match_config["match_type"] == "prefix":
                                regex = "^{0}_{1}(.*)$".format(target_cluster, match_config["match_expression"])
                            elif match_config["match_type"] == "regex":
                                regex = "^{0}_{1}$".format(target_cluster, str(match_config["match_expression"]).replace("^", "").replace("$", ""))
                            metric_label = metric_label_template.replace("$resource", resource).replace("$regex", regex).replace("$chargecode", chargecode_name)
                            metric_label_str = metric_label_str + metric_label
                elif cluster_details["chargeback_model"] == "client_usage_based":
                    resource = "client_id"
                    for match_config in match_config_list:
                        if match_config["entity"] == resource:
                            if match_config["match_type"] == "literal":
                                regex = "^{0}_{1}$".format(target_cluster, match_config["match_expression"])
                            elif match_config["match_type"] == "prefix":
                                regex = "^{0}_{1}(.*)$".format(target_cluster, match_config["match_expression"])
                            elif match_config["match_type"] == "regex":
                                regex = "^{0}_{1}$".format(target_cluster, str(match_config["match_expression"]).replace("^", "").replace("$", ""))
                            metric_label = metric_label_template.replace("$resource", resource).replace("$regex", regex).replace("$chargecode", chargecode_name)
                            metric_label_str = metric_label_str + metric_label

print(metric_label_str)

