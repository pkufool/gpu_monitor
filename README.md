# GPU Monitor
This is a simple tool that monitoring the occupation of GPU cards. With this tool, you won't have to login to your servers to check whether there are free cards one by one. It is a simple web page looks like the picture below.  
The picture displays GPU memory occupation for several servers, the green rows mean that the memory usage of these cards is less than 1/3, the orange rows mean that the memory usage is between 1/3 and 2/3, the red rows mean that the memory usage is more than 2/3.

![screen](/static/img/screen.png)

## How this works
### Collect memory occupation info
We use `nvidia-smi` command to get GPU cards' info.
```
$ nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv

index, name, memory.used [MiB], memory.total [MiB], utilization.gpu [%]
0, Tesla V100-SXM2-32GB, 21339 MiB, 32510 MiB, 100 %
1, Tesla V100-SXM2-32GB, 27 MiB, 32510 MiB, 0 %
2, Tesla V100-SXM2-32GB, 20934 MiB, 32510 MiB, 99 %
3, Tesla V100-SXM2-32GB, 3 MiB, 32510 MiB, 0 %
```
Run `nvidia-smi --help-query-gpu` for more details.


### Get the infos from other servers
To get the infos from other servers, `ssh` with `-t` option will be used. The line below could excute commands on the remote server without logining to it.
```
$ ssh -t user@host commands
```

To run this command without typing password, you should generate a passphraseless SSH key and push it to your remote server. Just hit `Enter` for the key and both passphrases:
```
$ ssh-keygen -t rsa -b 2048
Generating public/private rsa key pair.
Enter file in which to save the key (/home/username/.ssh/id_rsa): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/username/.ssh/id_rsa.
Your public key has been saved in /home/username/.ssh/id_rsa.pub.
```
Copy your keys to the target server:
```
$ ssh-copy-id user@server
user@server's password: 
```

## Set up
* Install requirements
```
pip install -r requirements.txt
```

* Generate a passphraseless SSH key and push it to each of your target server, and make sure you could login to the target server without typing your password.

* Edit the config.yaml accordingly, there are only three items, one is the server name (for displaying purpose), one is the user name (could login to the server without password), the last one is the ip of the server you want get its info.
```
servers:
  -
    name: server-one
    user: pkufool
    ip: 127.0.0.1
  -
    name: server-two
    user: pkufool
    ip: 127.0.0.2
```
* Run the flask application (could change the listening port if you like)
```
bash ./run.sh
```
Type http://ip:port on your browser, you should see the page similar to the screen shot above. 

## Acknowledgement
Flask: https://github.com/pallets/flask  
Vue: https://github.com/vuejs/vue  
Element UI: https://element.eleme.cn  

## License
gpu_monitor is MIT-licensed, as found in the [LICENSE](LICENSE) file.
