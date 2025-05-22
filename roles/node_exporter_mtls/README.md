Node_exporter_mtls
=========
This role configures [Prometheus Node Exporter](https://github.com/prometheus/node_exporter) with **mutual TLS (mTLS)** support using a custom Certificate Authority (CA).

It includes tasks for:

- Creating a local CA
- Generating and signing node certificates
- Optionally generating a Prometheus client certificate
- Configuring Node Exporter to require client certificates

Requirements
------------

This role depends on:

- `community.crypto` collection for TLS handling
- `prometheus.prometheus` main prometheus ollection

Install with:

```bash
ansible-galaxy install -r requirements.yml
```

Role Variables
--------------

This role expects all variables to be defined externally, typically in group_vars or host_vars. This includes:
- Certificate subject fields (country, organization, common name, etc.)
- TLS certificate and key paths
- CA settings
- Any other environment-specific options

This design choice keeps the role clean and allows full control and customization by the user. There are no default variables inside the role.

Examples can be found by the [Link](https://github.com/Timych84/ansible_node_exporter/tree/master/inventory)


Example Playbook
----------------

```yaml
- name: Intalll node_exporter_mtls
  hosts: all
  pre_tasks:
    - name: Load required collections from requirements.yml
      ansible.builtin.include_vars:
        file: requirements.yml
        name: required_collections

    - name: Get the list of installed collections
      delegate_to: localhost
      ansible.builtin.command:
        cmd: ansible-galaxy collection list
      register: collection_list
      changed_when: false

    - name: Check for required collections
      delegate_to: localhost
      ansible.builtin.assert:
        that:
          - item.name in collection_list.stdout
        fail_msg: "Collection '{{ item.name }}' is not installed"
        success_msg: "Collection '{{ item.name }}' is installed"
      loop: "{{ required_collections.collections }}"

  tasks:
    - name: Install node_exporter_mtls role
      become: true
      ansible.builtin.import_role:
        name: node_exporter_mtls
      vars:
        install_ca_cert: false
        install_node_exporter: true
        install_prometheus_cert: false
        install_node_exporter_with_tls: true
        install_snmp_exporter: false
```


License
-------

MIT License

Author Information
------------------

Timur Alekseev
