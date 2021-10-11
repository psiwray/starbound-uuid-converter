# Starbound UUID Converter

Use this script if you want to change the UUID of a savegame, for example
because you're restoring the save game of a friend and wish to play with him
again. Normally this wouldn't be possible, because you'd have the same UUID as
your friend. This tool converts all occurrences of the old UUID with a new one,
which you have to generate using an external tool or a website. It also renames
the occurrences in the file names.

**ALWAYS REMEMBER TO MAKE A BACKUP OF ALL YOUR `player` AND `universe` FOLDERS
BEFORE PROCEEDING.**

## Command-line usage

The `<Starbound>` folder indicates the Steam's game folder. All parameters are
required.

+ `-d, --dump`: the absolute or relative path of `dump_versioned_json.exe`. You
  can find this tool under the `<Starbound>\win32\` folder.
+ `-f, --folder`: the folder where all the player and universe files are stored,
  usually this is `<Starbound>\storage\`.
+ `-u, --uuid`: the old UUID to be replaced.
+ `-r, --replace-uuid`: the new UUID to replace every old occurrence with.
+ `-p, --pack`: the absolute or relative path of `make_versioned_json.exe`. You
  can find this tool under the `<Starbound>\win32\` folder.

### Example usage

```
python.exe .\convert.py^
  --dump=.\..\win32\dump_versioned_json.exe^
  --pack=.\..\win32\make_versioned_json.exe^
  --folder=.\^
  --uuid=4d9a7c2f9f11499772d1e27ea7f4231c^
  --replace-uuid=7d8981a66c904b68b6e2a95b6a88765b^
```
