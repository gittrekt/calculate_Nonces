#!/usr/bin/python3
import os
import sys
from glob import glob

VERSION = "0.0.2"

SECTOR_SIZE = 512
SHABAL256_HASH_SIZE = 32
SCOOP_SIZE = SHABAL256_HASH_SIZE * 2
SCOOPS_IN_NONCE = 4096
NONCE_SIZE = SCOOP_SIZE * SCOOPS_IN_NONCE
MB = 1024 * 1024
GB = 1024 * MB

def getDiskSize(dev):
    return int(open(f"/sys/block/{os.path.basename(dev)}/size").read()) * SECTOR_SIZE

def form(i):
    return format(int(i), ",d")

if __name__ == "__main__":
    print(f"{sys.argv[0].split('.')[0]} V{VERSION}")
    if len(sys.argv) < 2:
        for path in glob('/dev/sd*'):
            if any(char.isdigit() for char in path): pass # Show entire disks only
            else:
                try:
                    df_output_lines = [s.split() for s in os.popen(f"df {path} -P").read().splitlines()]
                    size = getDiskSize(df_output_lines[1][0]) - 2 * SECTOR_SIZE
                    statvfs = os.statvfs(df_output_lines[1][5])
                    total_blocks = statvfs.f_frsize * statvfs.f_blocks
                    free_blocks = statvfs.f_frsize * statvfs.f_bfree
                    available_blocks = statvfs.f_frsize * statvfs.f_bavail
                    print(f"""
Path           : {path}
Disk size      : {form(size // MB)}MB
Avaliable size : {form(available_blocks//MB)}MB
Total nonces   : {form(size // NONCE_SIZE)}
Free nonces    : {form(available_blocks//NONCE_SIZE)}""")
                except: pass
    else:
        try: 
            dev = sys.argv[1]
            df_output_lines = [s.split() for s in os.popen(f"df {dev} -P").read().splitlines()]
            size = getDiskSize(df_output_lines[1][0]) - 2 * SECTOR_SIZE
            statvfs = os.statvfs(df_output_lines[1][5])
            total_blocks = statvfs.f_frsize * statvfs.f_blocks
            free_blocks = statvfs.f_frsize * statvfs.f_bfree
            available_blocks = statvfs.f_frsize * statvfs.f_bavail
            print(f"""Disk size      : {form(size // MB)}MB
Avaliable size : {form(available_blocks//MB)}MB
Total nonces   : {form(size // NONCE_SIZE)}
Free nonces    : {form(available_blocks//NONCE_SIZE)}""")
        except Exception as e:
            print(f'{dev} cannot be listed to due to {e}')