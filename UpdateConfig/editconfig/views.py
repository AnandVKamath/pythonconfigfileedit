from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def update(request):
    config_var = request.GET['uvar']
    config_val = request.GET['uval']
    fn = '/tmp/config.txt'
    f = open(fn)
    output = []
    for line in f:
        if not line.startswith(config_var):
            output.append(line)
    f.close()
    f = open(fn, 'w')
    f.writelines(output)
    f.close()
    file = open("/tmp/config.txt", "a")
    file.write(config_var)
    file.write(': ')
    file.write(' "')
    file.write(config_val)
    file.write('"')
    file.writelines("\n")
    file.close()
    messages.success(request, 'Updated key to config file successfully!')
    return redirect('http://192.168.1.104:7001/')


def add(request):
    config_var = request.GET['avar']
    config_val = request.GET['aval']
    file = open("/tmp/config.txt", "a")
    file.write(config_var)
    file.write(': ')
    file.write('"')
    file.write(config_val)
    file.write('"')
    file.writelines("\n")
    file.close()
    messages.success(request, 'Added new key to config file successfully!')
    return redirect('http://192.168.1.104:7001/')

def delete(request):
    config_var = request.GET['uvar']
    fn = '/tmp/config.txt'
    f = open(fn)
    output = []
    for line in f:
        if not line.startswith(config_var):
            output.append(line)
    f.close()
    f = open(fn, 'w')
    f.writelines(output)
    f.close()
    messages.success(request, 'Deleted Key values from config file successfully!')
    return redirect('http://192.168.1.104:7001/')



def upload3ds(request):
    import paramiko, os, mysql.connector
    from dotenv import load_dotenv
    dotenv_path = '/home/anand/Documents/Scripts/Python/.envssh'
    load_dotenv(dotenv_path)
    hostip = os.getenv('HOSTIP_3DS')
    user = os.getenv('USERSSH')
    password = os.getenv('PASSWORD')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostip, port=22, username=user, password=password)
    sftp = ssh.open_sftp()
    print('SSH Connection Established')
    print('Uploading')
    sftp.put('/tmp/config.txt', '/tmp/config.txt')
    print('Uploaded Config File')
    sftp.close()
    return redirect('http://192.168.1.104:7001/')

def uploadprep(request):
    import paramiko, os, mysql.connector
    from dotenv import load_dotenv
    dotenv_path = '/home/anand/Documents/Scripts/Python/.envssh'
    load_dotenv(dotenv_path)
    hostip = os.getenv('HOSTIP_PREPARATORY')
    user = os.getenv('USERSSH')
    password = os.getenv('PASSWORD')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostip, port=22, username=user, password=password)
    sftp = ssh.open_sftp()
    print('SSH Connection Established')
    print('Uploading')
    sftp.put('/tmp/config.txt', '/tmp/config.txt')
    print('Uploaded Config File')
    sftp.close()
    return redirect('http://192.168.1.104:7001/')

def deploy(request):
    return redirect('http://192.168.1.104:7000/')