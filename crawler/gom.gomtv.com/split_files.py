import os
import shutil
import argparse

parser = argparse.ArgumentParser(description="Split files in a dir into multiple dirs")
parser.add_argument("--in_dir", help="Input dir")
parser.add_argument("--split", help="Split #")
parser.add_argument("--out_prefix", help="Output dir prefix")
args = parser.parse_args()

in_dir = "subtitle"
if args.in_dir is not None:
    in_dir = args._in_dir
split = 4
if args.split is not None:
    split = int(args.split)
out_prefix = "subtitle_"
if args.out_prefix is not None:
    out_prefix = args.out_prefix

# Load all files
print 'Load all files'
file_list = os.walk(in_dir).next()[2]

# Generate out dirs
print 'Generate out dirs'
out_dir_list = []
for i in range(split):
    dirname = out_prefix + str(i + 1)
    out_dir_list.append(dirname)
    os.mkdir(dirname)

# Split files into $(split) lists
print 'Split files into ' + str(split) + ' lists'
for i, filename in enumerate(file_list):
    shutil.copy(os.path.join(in_dir, filename), os.path.join(out_dir_list[i % split], filename))

print 'done!'
