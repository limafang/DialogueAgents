from cssa.utils import read_json_file, get_script

text_batches, speakers = get_script("example_data.json")
print(text_batches)
print(speakers)
