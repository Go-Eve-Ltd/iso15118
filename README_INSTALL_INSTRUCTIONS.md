ISO 15118 Installation Instructions

Note, this will work on any Linux that’s running Debian 11. That gives you python 3.9 out of the box and the possibility of openjdk 17. 
Any earlier Debian or any earlier derivative of Debian (Ubuntu, Mint, etc) will eventually work, but it’s a lot of work. Ubuntu 22 should work fine, or the latest Mint. 

This whole process takes up to a couple of hours on a Pi. Faster connection, faster machine, a lot less. This includes some steps that aren't included in the base install instructions. 

In the end it will NOT run properly on anything very low power like a Beagle Bone Black or an Olimex. Pi4 is fine. Rock 4 is fine. Any “normal” Linux box or Virtual Box will be fine. 

1. Install appropriate Armbian/Debian/Raspbian


  a. Finish install. Reboot.
  
  b. Log in as root (root, 1234 on Armbian),
  
  c. change root password to something useful,
  
  d. create new userid/password
  
  e. Install en utf8 locality if applicable
  
  f. Check python > 3.9  (python3 -V)
  
  g. Reboot and log in as user
  
  h. Install java 17  (sudo apt install openjdk-17-jre)
  
  i. Do sudo apt update, upgrade a few times.



2. Install pip and python dev and gcc


  a.	sudo apt install python3-pip

  b.	sudo apt-get install gcc python3-dev


3. Install Poetry

  a.	curl -sSL https://install.python-poetry.org | python3 –


4. Install make

  a.	sudo apt install make



5. Download ISO 15118 library


  a.	wget https://github.com/SwitchEV/iso15118/archive/refs/heads/master.zip
  
  b.	sudo apt install unzip
  
  c.	unzip master.zip
  
  d.	do the rest from here down https://github.com/SwitchEV/iso15118#1-generate-certificates
  
  e.	some of it is already done. 
  
  f.	For the .env file, don’t change any parameters, just make the .env file from the .env.dev.local and save as .env (use nano)


6. Run install instructions


7. Run
