#!/bin/bash
# mount Box.com on Amazon Linux 2 instance
# sudo yum update -y
sudo amazon-linux-extras install epel -y
sudo yum install davfs2 -y
mkdir /home/ec2-user/box.com
chown ec2-user:ec2-user /home/ec2-user/box.com
sudo sed -i s/"use_locks       1"/"use_locks       0"/ /etc/davfs2/davfs2.conf
sudo usermod -a -G davfs2 ec2-user
sudo echo "https://dav.box.com/dav /home/ec2-user/box.com davfs rw,user,noauto 0 0" >> /etc/fstab
sleep 3
echo "---"
echo "Relogin and run 'mount box.com' to connect to Box"
echo "If there is a permission error: run 'chmod 600 /home/ec2-user/.davfs2/secrets'"
echo "use 'umount box.com' to unmount"
