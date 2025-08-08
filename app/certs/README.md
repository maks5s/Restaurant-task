```shell
# Generate an RSA private key, of size 2048
openssl genrsa -out jwt-private.pem 2048
```

```shell
# Extract the public key from the key pair, which can be used in certificate
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```

Run these commands to create secrets. You may be needed to install OpenSSL.

DO NOT SHOW THESE SECRETS IN PRODUCTION! EDUCATIONAL PURPOSE ONLY!