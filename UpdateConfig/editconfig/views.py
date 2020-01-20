from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages

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

def home(request):
    import  mysql.connector

    my_db = mysql.connector.connect(host="192.168.1.74", user="root", password="password", database="deploy")
    mycursor = my_db.cursor()
    select_data = "select * from deploy.deploy_serverlist order by id desc limit 1"
    mycursor.execute(select_data)
    records = mycursor.fetchall()
    for row in records:
        env = (row[1])
    print(env)
    return render(request, 'home.html')

def setdata(request):
    import mysql.connector
    filename = request.GET.get('filename')
    print(filename)
    my_db = mysql.connector.connect(host="192.168.1.74", user="root", password="password", database="deploy")
    mycursor = my_db.cursor()
    insert_data = "insert into deploy_serverlist (env_file) value ( %s ) "
    recordTuple = (filename,)
    mycursor.execute(insert_data, recordTuple)
    my_db.commit()
    return redirect('http://192.168.1.104:7001/')


def upload3ds(request):
    import paramiko, mysql.connector
    from configparser import ConfigParser
    configur = ConfigParser()
    configur.read('/home/anand/ENV/config.ini')
    my_db = mysql.connector.connect(host="192.168.1.74", user="root", password="password", database="deploy")
    mycursor = my_db.cursor()
    select_data = "select * from deploy.deploy_serverlist order by id desc limit 1"
    mycursor.execute(select_data)
    records = mycursor.fetchall()
    for row in records:
        envs = (row[1])
    print(envs)
    hostip = configur.get(envs,'HOSTIP_3DS')
    user = configur.get(envs, 'USERSSH')
    password = configur.get(envs, 'PASSWORD')
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
    import paramiko, mysql.connector
    from configparser import ConfigParser
    configur = ConfigParser()
    configur.read('/home/anand/ENV/config.ini')
    my_db = mysql.connector.connect(host="192.168.1.74", user="root", password="password", database="deploy")
    mycursor = my_db.cursor()
    select_data = "select * from deploy.deploy_serverlist order by id desc limit 1"
    mycursor.execute(select_data)
    records = mycursor.fetchall()
    for row in records:
        envs = (row[1])
    print(envs)
    hostip = configur.get(envs,'HOSTIP_PREPARATORY')
    user = configur.get(envs, 'USERSSH')
    password = configur.get(envs, 'PASSWORD')
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


