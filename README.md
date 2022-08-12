# nitw-helper
Python script to simplify modifications of Night in the Woods phrazes

With help of NITW-Dialogue-Tool it is possible to extract all .yarn.txt files from the .assets Unity archived files. This script goes a little bit further and collects all names and phrazes of the characters from already extracted files in one file, simplifying the process of modifications and eliminating the need to see all the stuff behind the scenes.

`python ./main` to extract all the names and phrazes from the .yarn.txt files situated in "original" directory into "phrazes.txt" and copy its contents into "phrazes_translated.txt" after giving permission to rewrite it if already existed not to delete the progress of going on tranlsation accidentally. And to copy content of "original" directory to "not_patched" (`-r` for decipherement of originally substituted russian files) (`-e` for not translating original emoticons in Esperanto)
`python ./main -p" to patch the content of created on the previous step "not_patched" directory based on "phrazed_translated.txt"
