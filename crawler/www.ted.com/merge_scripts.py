#!/usr/bin/python

import os
import json

# get the list of script filenames
OUT_FILENAME = 'ted.json'
SCRIPT_DIR = 'scripts/'
script_names = sorted(os.listdir(SCRIPT_DIR));

print("Merging {} script files...".format(len(script_names)))

parcors = []

count = 0
synced_list_count = 0;
while count < len(script_names):
	script_en_name = script_names[count]
	count += 1
	script_ko_name = script_names[count]

	#Check whether two script file names accord with each other
	#script_en_name = 'xxxx-en.json'
	#script_ko_name = 'xxxx-ko.json'
	if script_en_name[:-8] != script_ko_name[:-8]:
		continue
	else:
		count += 1

		with open(SCRIPT_DIR + script_en_name, 'r') as fd:
			ens = json.load(fd)
		with open(SCRIPT_DIR + script_ko_name, 'r') as fd:
			kos = json.load(fd)

		# Read only when two scripts are in time syncs
		time_synced = True
		if len(ens) != len(kos):
			time_synced = False
		else:
			for i in range(len(ens)):
				en_data_time = ens[i]['data_time']
				ko_data_time = kos[i]['data_time']
				if en_data_time != ko_data_time:
					time_synced = False
					break

		if time_synced:
			synced_list_count += 1
			for i in range(len(ens)):
				en = ens[i]['en']
				ko = kos[i]['ko']
				parcors.append({'en':en, 'kr':ko})

print("{} script files({} lectures) merged".format(synced_list_count * 2, synced_list_count))
print("{} sentences in parcors".format(len(parcors)))
print("Dump into json file({})".format(OUT_FILENAME))

data = dict()
data['source'] = 'ted'
data['type'] = 'sentence'
data['values'] = parcors

with open(OUT_FILENAME, 'w') as fd:
	json.dump(data, fd, indent=2)

