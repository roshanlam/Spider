def save(folder, filename, info):
  try:
    folder = pathlib.Path("{}".format(folder))
    folder.mkdir(parents=True)
    filename = "{}.txt".format(filename)
    filepath = folder / filename
  except FileExistsError:
    folder = pathlib.Path("{}".format(folder))
    filename = "{}.txt".format(filename)
    filepath = folder / filename
  
  try:
    with filepath.open("a+", encoding ="utf-8") as f:
        f.write(str(info))
  except FileExistsError:
    print("File {}".format(filename) + " already exists")
