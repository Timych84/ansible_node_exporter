import os
import yaml
import getpass
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.x509 import SubjectAlternativeName, DNSName
from datetime import datetime, timedelta

# Load YAML configuration
with open("gen_certs.yaml", "r") as f:
    config = yaml.safe_load(f)

ca_cert_path = config["ca"]["cert_path"]
ca_key_path = config["ca"]["key_path"]
organization = config["organization"]
servers = config["servers"]
cert_validity_days = config["cert"]["cert_validity"]

# Load CA certificate and key
with open(ca_cert_path, "rb") as f:
    ca_cert = x509.load_pem_x509_certificate(f.read())


def load_private_key_with_password(file_path):
    # Read the PEM file
    with open(file_path, "rb") as f:
        key_data = f.read()

    # Try to load without a password first
    try:
        private_key = load_pem_private_key(key_data, password=None)
        print("Private key is not password-protected.")
        return private_key
    except TypeError:
        print("Private key is password-protected.")

    # Prompt the user for a password
    while True:
        try:
            password = getpass.getpass("Enter password for the private key: ")
            private_key = load_pem_private_key(
                key_data,
                password=password.encode()
            )
            print("Private key loaded successfully.")
            return private_key
        except ValueError:
            print("Incorrect password. Please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")
            break


# Helper to generate a key pair
def generate_key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


# Helper to write PEM files
def write_pem(data, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(data)


ca_key = load_private_key_with_password(ca_key_path)
# Generate certificates for each server
for server in servers:
    key = generate_key()
    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, organization["country"]),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, organization["state"]),
        x509.NameAttribute(NameOID.LOCALITY_NAME, organization["locality"]),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization["organization_name"]),
        x509.NameAttribute(NameOID.COMMON_NAME, server["cn"]),
    ])
    san = SubjectAlternativeName([DNSName(name) for name in server["san"]])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(ca_cert.subject)
        .public_key(key.public_key())
        .add_extension(san, critical=False)
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=cert_validity_days))
        .sign(ca_key, hashes.SHA256())
    )
    # Write certificate and key to files
    write_pem(cert.public_bytes(serialization.Encoding.PEM), os.path.join(config["cert"]["cert_dir"], server["name"], "windows_exporter_cert.pem"))
    write_pem(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ), os.path.join(config["cert"]["cert_dir"], server["name"], "windows_exporter_key.pem"))

print("Certificates and keys generated successfully.")
