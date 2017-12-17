# Troubleshooting Guide
This guide helps you in troubleshooting common errors in DevSecOps Studio.

## Ansible Galaxy

1. If you get any error while installing roles using ansible-galaxy

	```bash
	$ ansible-galaxy install -r requirements.yml -p provisioning/roles
	```
	
	> downloading role 'pip', owned by geerlingguy
	
	> __ERROR!__ Unexpected Exception:
	> \<urlopen error ('_ssl.c:645: The handshake operation timed out',)>

	
	__Fix__: Try running the command again, it should resolve itself.

2. If download appears to be stuck.

	__Fix__: kill the command using Ctrl+C and re-run the command.

## Playbook (vagrant up)
1. If you encounter any errors while doing vagrant up, note down the role you are currently running.

The following snippet is shows that jenkins role is being executed at the moment.

> TASK [**jenkins**: Install Jenkins]


## Virtualbox

1. Virtualbox just crashes the guest machines with aborted status.
   Fix: Ensure you have enough memory (4B) free, if not close few programs and then run `vagrant up` from DevSecOps-Studio directory.


# Running the commands behind corporate proxy 

Certificate validation failed errors

Running ```ansible-galaxy``` and ```vagrant``` commands from terminal behind the corporate proxy would throw Certificate Validation failed error 
and command execution fails. The error is caused because the commands usually uses OpenSSL internally which doesn't recongnize the corporate 
root certificate

## Certificate validation error when running ansible-galaxy command

Run the following command - 

```bash 
$ ansible-galaxy
```
> __ERROR!__ SSL Certificate Validation failed

1. Acccess any https website from your browser (Chrome) and download the certificate by clicking on the lock icon in the address bar and save it as .pem file (corporate_root_certificate.pem)

2. Run following command to identify the path of openssl cacerts locations (its usuall /usr/local/etc/openssl/certs)

```bash 
$ brew info openssl 
```

3. Copy corporate_root_certificate.pem in /usr/local/etc/openssl/certs folder

4. Run the following command to include the corporate root certificate in openssl 

```bash
$ /usr/local/opt/openssl/bin/c_rehash
```

5. Open a new terminal window and execute ansible-galaxy command. 

This command should run smoothly now without any erros.

Follow the similar procedure for ```vagrant up``` command 

1. Go to Vagant home (/opt/vagrant)

2. Make a backup of cacert.pem

3. Open cacert.pem in any text editor and copy the conents of corporate_root_certificate.pem file at the end of cacert.pem file. Save the file.

   The content of corporate_root_certificate.pem file would look something like 

   ```
   -----BEGIN CERTIFICATE-----
   dfdfdfdfdfdfdfd some value
   -----END CERTIFICATE-----
   ``` 
4. Open new terminal and execute the ```vagrant up``` command
