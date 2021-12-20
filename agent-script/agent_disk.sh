#!/bin/bash -x

echo "-----------Preparing hard disks"
echo "hard disks info:"
lsblk -o NAME,HCTL,SIZE,MOUNTPOINT | grep -i "sd"

echo "creating partitions"
for disk in sdc sdd; do
  sudo parted /dev/${disk} --script mklabel gpt mkpart xfspart xfs 0% 100%
  sudo mkfs.xfs /dev/${disk}1
  sudo partprobe /dev/${disk}1
done

echo "creating a volume group"
sudo vgcreate VolGroup01 /dev/sdc1 /dev/sdd1

echo "creating a logical drive"
sudo lvcreate -l 100%FREE -n data VolGroup01

echo "activating logical drive"
sudo vgchange -ay VolGroup01

echo "creating merged partition"
sudo mkfs.ext3 /dev/VolGroup01/data

echo "mounting a volume"
sudo mkdir /mnt/data
sudo mount  /dev/VolGroup01/data /mnt/data
