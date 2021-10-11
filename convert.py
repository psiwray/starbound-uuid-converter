from sys import argv, exit
from getopt import getopt, error
from os import walk, rename
from os.path import join, abspath
from subprocess import run, CalledProcessError
from re import finditer

def execute():
	dump_program = None
	pack_program = None
	source_folder = None
	search_uuid = None
	replace_uuid = None

	try:
		args, values = getopt(argv[1:], ["d:f:u:r:p:"], ["dump=", "folder=", "uuid=", "replace-uuid=", "pack="])

		for current_arg, current_value in args:
			if current_arg in ("-d", "--dump"):
				dump_program = abspath(current_value)
			elif current_arg in ("-f", "--folder"):
				source_folder = abspath(current_value)
			elif current_arg in ("-u", "--uuid"):
				search_uuid = current_value
			elif current_arg in ("-r", "--replace-uuid"):
				replace_uuid = current_value
			elif current_arg in ("-p", "--pack"):
				pack_program = abspath(current_value)
	except error as err:
		print("Error parsing arguments.")
		exit(-1)

	for arg in [dump_program, pack_program, source_folder, search_uuid, replace_uuid]:
		if arg is None:
			print("Missing required arguments.")
			exit(-1)

	print(f"Using dump program in: <{dump_program}>.")
	print(f"Using pack program in: <{pack_program}>.")
	print(f"Finding all files in folder <{source_folder}> and all its subfolders.")
	print(f"Searching for UUID {search_uuid} and replacing them with {replace_uuid}.")

	# First convert all files to JSON. Notify which files failed to convert.
	print("Converting the files to JSON.")
	for (path, directories, files) in walk(source_folder):
		print(f"Currently inside <{path}>.")
		for file in files:
			if file.endswith(".json"): # Skip JSON files that are the output of this program.
				continue

			print(f"Processing file <{file}>... ", end="")
			result = run([dump_program, join(path, file), join(path, f"{file}.json")], capture_output=True)
			if result.returncode == 0:
				print("done.")
			else:
				print("failed.")
	
	# Then find the occurrences of the UUID inside all the converted files.
	print("Finding UUIDs inside the converted files.")
	for (path, directories, files) in walk(source_folder):
		print(f"Currently inside <{path}>.")
		for file in files:
			if not file.endswith(".json"): # Skip non-JSON files.
				continue

			print(f"Processing file <{file}>... ", end="")
			new_content = None
			# Print all occurrences just as a reference.
			with open(join(path, file), mode="r") as f:
				content = f.read()

				# Create a memory reference of the text with the replaced occurrences.
				new_content = content.replace(search_uuid, replace_uuid)

			# Write the memory occurrences to the original file.
			with open(join(path, f"{file}.new"), mode="w") as f:
				f.write(new_content)
			print("done.")

	# Now convert all new files back to the original ones.
	print("Converting back to original.")
	for (path, directories, files) in walk(source_folder):
		print(f"Currently inside <{path}>.")
		for file in files:
			if not file.endswith(".new"): # Skip non-converted files.
				continue

			print(f"Processing file <{file}>... ", end="")
			result = run([pack_program, join(path, file), join(path, file.replace(".json.new", ""))], capture_output=True)
			if result.returncode == 0:
				print("done.")
			else:
				print("failed.")

	# Rename all old UUID file names with the new one.
	print("Updating the file names.")
	for (path, directories, files) in walk(source_folder):
		print(f"Currently inside <{path}>.")
		for file in files:
			if search_uuid in file:
				rename(join(path, file), join(path, file.replace(search_uuid, replace_uuid)))
				print(f"Updated name for <{file}>.")

if __name__ == '__main__':
	execute()
