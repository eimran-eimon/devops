import paramiko

urls = [lines.strip() for lines in open('url_input.txt').readlines()]
server_ips = [lines.strip() for lines in open('server_ip.txt').readlines()]

suffix = '.io'
corrected_urls = [url + suffix for url in urls]

curl_commands = ['curl ' + corrected_url for corrected_url in corrected_urls]

for server_ip in server_ips:

	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	hostname = server_ip.split(',')[0]
	username = server_ip.split(',')[1]
	password = server_ip.split(',')[2]

	try:
		client.connect(hostname=hostname, username=username, password=password)
	except:
		print("[!] Cannot connect to the SSH Server")
		exit()

	for command in curl_commands:
		print("=" * 50, url, "=" * 50)
		stdin, stdout, stderr = client.exec_command(command)
		print('Output from the remote server: \n' + stdout.read().decode())
		err = stderr.read().decode()
		if err:
			print("Error --> " + err)
	client.close()
