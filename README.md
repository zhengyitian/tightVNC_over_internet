# tightVNC_over_internet


To make it work, install tightvnc on the computers at your home and in your company, change the ip parts in the files, run runOnRemoteServer.py on your server with a publish ip, run runOnCompany.py on your company computer, run runOnHome.py on your home computer. On your home computer, open tightvnc Viewer, connect to the ip::port used in runOnHome.py(in my case 127.0.0.1::9999), then your can remote control your company computer not in your LAN.


Based on (python)tornado, tightvnc. Tested on my company computer(win10 64bit,tightvnc-2.8.11 64bit), my home computer(win8 64bit,tightvnc-2.8.11 64bit), my remote server(ubuntu18), all with python 2.7.15. Of course, you can test it using one computer, with a few changes in the ip parts in the files.


A few words about the coming of this. A few days ago, I came to know vultr.com and rent a server in Seattle with $5/month. The network speed is ok for me, and I wanted to make more of it than just being a shadowsock server(I live in Beijing, you know :-)). I stared to use tightvnc a few months ago because teamviewer free version went crippy, but it lacks the over-internet funtion. I think the few hours at work and the all night at home working on this are worth of it, at least it makes myself happy.
