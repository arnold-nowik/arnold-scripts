#!/bin/sh
# Perform a btrfs scrub on the root filesystem

echo "Scrub started on /home at $(date -Ins)." >> /home/factor828_admin/Desktop/btrfs-scrub-log
btrfs scrub start -c 2 -n 7 -B /home >> /home/factor828_admin/Desktop/btrfs-scrub-log
chown factor828_admin /home/factor828_admin/Desktop/btrfs-scrub-log
