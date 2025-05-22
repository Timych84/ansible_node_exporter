# Ansible Node Exporter with mTLS

This repository provides an Ansible playbook and role to install and configure [Prometheus Node Exporter](https://github.com/prometheus/node_exporter) **with mutual TLS authentication (mTLS)**.

- Uses [prometheus.prometheus.node_exporter](https://galaxy.ansible.com/prometheus/prometheus) collection to install the exporter.
- Includes a custom role to generate and distribute TLS certificates using `community.crypto`.
- Optionally supports manual certificate generation via `gen_certs.py`.


Role node_exporter_mtls will:

- Create a self-signed Certificate Authority (CA) at ca_control node
- Generate and sign certificates for each target(including cert for prometheus node)
- Configure Node Exporter to use mTLS

### Requirements

- Ansible 2.12+
- Python 3
- SSH access to target hosts
- Ansible Galaxy Collections

requirements.yml:
  ```yaml
  collections:
    - name: prometheus.prometheus
      version: "0.21.0"
    - name: community.crypto
      version: "2.22.1"
  ```
to install:
```bash
ansible-galaxy collection install -r requirements.yml
```

### Directory Structure
```
ansible_node_exporter/
├── inventory/
│   └── hosts
├── roles/
│   └── node_exporter_mtls/        # Custom role for CA and TLS config
├── gen_certs.py                   # Optional: Python-based manual cert generator
├── gen_certs.yaml.example         # Example config for gen_certs.py
├── requirements.yml
├── site.yml                       # Main playbook
├── users.yml                      # Optional user config
└── README.md
```


# Getting Started
1. Clone the repository
```bash
git clone https://github.com/Timych84/ansible_node_exporter.git
cd ansible_node_exporter
```
2. Install required collections
```bash
ansible-galaxy collection install -r requirements.yml
```
3. Prepare Inventory
Edit inventory/hosts to list your target nodes and put them into proper node groups:
    ```yaml
    all:
      hosts:
        node1:
          ansible_host: 10.10.10.2
          ansible_user: root
        node2:
          ansible_host: 10.10.10.3
          ansible_user: admin
        ca_node:
          ansible_host: 10.10.10.4
          ansible_user: admin
        prom_node:
          ansible_host: 10.10.10.4
          ansible_user: admin
        snmp_node:
          ansible_host: 10.10.10.5
          ansible_user: admin
      children:
        node_exporter:
          hosts:
            ubu_node6:
            centos_node6:
        ca_control:
          hosts:
            ca_node:
        prometheus:
          hosts:
            prom_node:
        snmp_exporter:
          hosts:
            snmp_node:

    ```
4. Modify group_vars for host groups(if needed)\
You can set main certificate fields and configuration parameters for node_exporter

5. Run the playbook:
    ```bash
    ansible-playbook -i inventory/hosts site.yml
    ```

## Manual cettificate creation (via gen_certs.py)
You can manually generate certs using the provided Python script
1. Copy the config:
    ```bash
    cp gen_certs.yaml.example gen_certs.yaml
    ```
2. Install python requirements
    ```bash
    pip3 install -r requirements.txt
    ```
3. Edit gen_certs.yaml to define nodes and their SANs.
4. Run the script
    ```bash
    python3 gen_certs.py
    ```
This will generate certificates in the specified structure, which can be copied to the appropriate hosts.
