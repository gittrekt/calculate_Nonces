#!/usr/bin/python3
import os
import sys
import subprocess
from glob import glob

VERSION = "0.0.3"

SECTOR_SIZE = 512
SHABAL256_HASH_SIZE = 32
SCOOP_SIZE = SHABAL256_HASH_SIZE * 2
SCOOPS_IN_NONCE = 4096
NONCE_SIZE = SCOOP_SIZE * SCOOPS_IN_NONCE
MB = 1024 * 1024
GB = 1024 * MB
TB = 1024 * GB

def getDiskSize(dev):
    return int(open(f"/sys/block/{os.path.basename(dev)}/size").read()) * SECTOR_SIZE

def get_diskinfo(loc):
    df_output_lines = [s.split() for s in os.popen(f"df {path} -P").read().splitlines()]
    disk = df_output_lines[1][0]
    mount = df_output_lines[1][5]
    size = getDiskSize(df_output_lines[1][0]) - 2 * SECTOR_SIZE
    calc = MB
    text = 'MB'
    if size >= TB:
        calc = TB
        text = 'TB'
    elif size >= GB:
        calc = GB
        text = 'GB'
    statvfs = os.statvfs(df_output_lines[1][5])
    total_blocks = statvfs.f_frsize * statvfs.f_blocks
    free_blocks = statvfs.f_frsize * statvfs.f_bfree
    available_blocks = statvfs.f_frsize * statvfs.f_bavail
    print(f"""
Disk           : {disk} 
Mount          : {mount}
Disk size      : {size / calc:,.2f}{text}
Avaliable size : {available_blocks / calc:,.2f}{text}
Total nonces   : {size // NONCE_SIZE:,}
Free nonces    : {available_blocks // NONCE_SIZE:,}\n""")

if __name__ == "__main__":
    print(f"{sys.argv[0].split('.')[0]} V{VERSION}")
    if len(sys.argv) < 2:
        for path in glob('/dev/sd*'):
            if any(char.isdigit() for char in path): pass
            else:
                try:
                    get_diskinfo(path)
                except: pass
    else:
        try:
            path = sys.argv[1]
            get_diskinfo(path)
        except Exception as e:
            print(f'{path} cannot be listed to due to {e}')
            exit(0)