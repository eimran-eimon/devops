import paramiko

urls = [lines.strip() for lines in open('url_input.txt').readlines()]
server_ips = [lines.strip() for lines in open('server_ip.txt').readlines()]

suffix = '.io'
corrected_urls = [url + suffix for url in urls]

curl_commands = ['curl ' + corrected_url for corrected_url in corrected_urls]

for server_ip in server_ips:

	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	hostname = server_ip.split(', ')[0]
	username = server_ip.split(', ')[1]
	# password = server_ip.split(', ')[2]
	key = paramiko.RSAKey.from_private_key_file("/home/eimon/.ssh/id_rsa")

	client.connect(hostname=hostname, username=username, pkey=key)

	for command in curl_commands:
		print("=" * 50, command, "=" * 50)
		stdin, stdout, stderr = client.exec_command(command)
		print('Output from the remote server: \n' + stdout.read().decode())

	client.close()
