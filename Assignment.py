import paramiko
import sys

servers = ['10.100.117.123']
root_password = ['abcdef']

def change_sshd_config(ftp):
	file=ftp.file('/etc/ssh/sshd_config', "r")
	
	# creating new file by changing required line
	new_file = ''
	old_line = ''
	allowed_users = ''

	lines = file.readlines()
	for line in lines:
		if(line.startswith('AllowUsers')):
			old_line = line
		else :
			new_file = new_file + line

	if(old_line!=''):
	    allowed_users = old_line.split()

	new_line = 'AllowUsers'

	for user in allowed_users:
		if(user!='AllowUsers'):
			new_line = new_line + ' ' + user

	if('root' not in new_line):
		new_line = new_line + ' root'

	if(username not in new_line):
		new_line = new_line + ' ' + username

	new_file = new_file + new_line
	file.flush()

	file=ftp.file('/etc/ssh/sshd_config', "w")
	file.write(new_file)
	file.flush()

	print('file changed successfully')
    


def enable_ssh():

	for i in range(len(servers)):

		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(servers[i], username='root', password=root_password[i])

        # using sftp to write to a remote file
		ftp = ssh.open_sftp()
		new_file = change_sshd_config(ftp)
		ftp.close()

		# Restarting the sshd service.
		stdin, stdout, stderr = ssh.exec_command('systemctl restart sshd.service')
		ssh.close()



if __name__ == '__main__':

	# No Command Line argument.
    if len (sys.argv) != 2 :
        print("Usage: python Assignment.py <Username>")
        sys.exit (1)

    # Saving command line argumemt in python.
    username = sys.argv[1]

    enable_ssh()
