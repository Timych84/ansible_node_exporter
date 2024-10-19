# Ansible Playbook: Install and Configure node_exporter

This repository contains an Ansible playbook that installs and configures `node_exporter` on target hosts. It also handles the creation of TLS certificates for secure communication using OpenSSL.

## Features
- Creates a directory for `node_exporter` configuration.
- Generates a self-signed certificate and private key using OpenSSL.
- Installs and configures `node_exporter` using the official Prometheus role.

## Requirements

Before running the playbook, ensure that the following are available:
- Ansible installed on the control node.
- The `prometheus.prometheus.node_exporter` role installed via Ansible Galaxy:
  ```bash
  ansible-galaxy install prometheus.prometheus.node_exporter
