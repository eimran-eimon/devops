# _*_ coding: utf-8 _*_
import paramiko

urls = [lines.strip() for lines in open('url_input.txt').readlines()]
server_ips = [lines.strip() for lines in open('server_ip.txt').readlines()]
# just input one IP in the text file, If multiple separate by newline
# example format:
# 192.168.0.108(ipAddress), eimon(username)

suffix = '.uk'
corrected_urls = [url + suffix for url in urls]

curl_commands = [
	'sudo docker exec -ti `sudo docker ps --filter="Name=test_varnish" --no-trunc -q` ' \
	'curl -X PURGE http://localhost:80/'
	+ corrected_url
	for corrected_url in corrected_urls]

for server_ip in server_ips:

	server = paramiko.SSHClient()
	server.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	hostname = server_ip.split(', ')[0]
	username = server_ip.split(', ')[1]

	key = paramiko.RSAKey.from_private_key_file("/home/eimon/.ssh/id_rsa")
	server.connect(hostname=hostname, username=username, pkey=key)

	stdin, stdout, stderr = server.exec_command('cat ~/Desktop/sample.txt')
	# I am assuming this command will return list of ipAddresses and separated by newline.
	# 192.168.0.1
	# 192.168.0.2

	container_ips = [lines.strip() for lines in stdout.read().decode("utf-8").strip().split("\n")]

	for container_ip in container_ips:

		container = paramiko.SSHClient()
		container.set_missing_host_key_policy(paramiko.AutoAddPolicy())

		# I am assuming the container's username and private keys are the same as the server.
		container.connect(hostname=container_ip, username=username, pkey=key)
		print ("Executing Command for Container IP:\n " + container_ip)

		for command in curl_commands:
			print("=" * 50, command, "=" * 50)
			stdin, stdout, stderr = container.exec_command(command)
			print('Output from the remote server: \n' + stdout.read().decode())

		container.close()

	server.close()
