import os
import re
import json
import shutil
import argparse


PHRASES = []
PHRASE_ADDRESSES = []
APPROVE_NUM = 1



with open("emoticons_table.json", "r", encoding="utf-8") as f:
    emoticons_table = json.load(f)


with open("chars_table.json", "r", encoding="utf-8") as f:
    chars_table = json.load(f)


def reload(filesys_obj, mode="dir"):
    if mode == "dir":
        if os.path.exists(filesys_obj):
            shutil.rmtree(filesys_obj)
        os.mkdir(filesys_obj)
    elif mode == "file":
        if os.path.exists(filesys_obj):
            os.remove(filesys_obj)
        os.touch(filesys_obj)



def load(source, dest, mode="dir"):
    if mode == "dir":
        if os.path.exists(dest):
            shutil.rmtree(dest)
        shutil.copytree(source, dest)
    elif mode == "file":
        if os.path.exists(dest):
            os.remove(dest)
        shutil.copyfile(source, dest)


def sub_in_line(line, idx, jdx, look_up_table):
    line_nofix_pre = line[0:idx]
    line_fix = line[idx:jdx]
    line_nofix_post = line[jdx:]
    for key, value in look_up_table.items():
        line_fix = re.sub(key, value, line_fix)
    fixed_line = line_nofix_pre + line_fix + line_nofix_post
    return fixed_line, line_fix


def get_name_and_span(re_special, re_basic):
    name = None
    span = (None, None)
    if re_special is not None:
        span = re_special.span("PHRASE")
    elif re_basic is not None:
        span = re_basic.span("PHRASE")
        name = re_basic.group("NAME")
    if name is None:
        name = "Not Stated"
    return name, span


def extract_named_phrases(decipher_russification, translate_emoticons):
    global PHRASES
    global PHRASE_ADDRESSES
    reload("not_patched", mode="dir")
    re_special_search_str = r"\[\[(?:\{.*?\})?(?P<PHRASE>.*?)(?:\{.*?\})?\|(?:.*?)\]\]\s*#line"
    re_basic_search_str = r"\s*(?:(?P<NAME>\w*?)(?:\:))?(?:->)?\s*(?:\{.*?\})*(?:\[.*?\])*\s*(?P<PHRASE>.*?)(?:\{.*?\})?(?:\[\/.*?\])?\s*#line"
    re_special_search = re.compile(re_special_search_str)
    re_basic_search = re.compile(re_basic_search_str)
    print(f"Following regex expressions have been used for compilation:")
    print(f"re_special_search: {re_special_search_str}")
    print(f"re_basic_search: {re_basic_search_str}")
    total_line_num = 0
    for filename in os.listdir("original"):
        with open(os.path.join("original", filename), "r", encoding="utf-8") as original_file:
            lines = original_file.readlines()
            lines = [line.rstrip() for line in lines]
            new_lines = []
            for i, line in enumerate(lines):
                if translate_emoticons:
                    for key, value in emoticons_table.items():
                        line = re.sub(re.escape(key), value, line)
                re_special = re.search(re_special_search, line)
                re_basic = re.search(re_basic_search, line)
                name, span = get_name_and_span(re_special, re_basic)
                if span != (None, None):
                    total_line_num += 1
                    idx, jdx = span
                    if decipher_russification:
                        line, phrase = sub_in_line(line, idx, jdx, chars_table)
                    else:
                        phrase = line[idx:jdx]
                    PHRASES.append(f"{total_line_num}:{name}:{phrase}")
                    PHRASE_ADDRESSES.append(f"{total_line_num}/{filename}/" + \
                    f"{i + 1}/{idx}/{idx + len(phrase)}")  # len() if changed
                lines[i] = line
            text = "\n".join(lines)
            with open(os.path.join("not_patched", filename), "w+", encoding="utf-8") as not_patched_file:
                not_patched_file.write(text + "\n")


def collect_named_phrases():
    global PHRASES
    global PHRASE_ADDRESSES
    global APPROVE_NUM
    answers = []
    name_pre = "phrases_collected.txt"
    name_post = "phrases_translated.txt"
    approve = "{}/{} approve"
    question = f"Next step will rewrite \"{name_post}\" based on \"{name_pre}\". " + \
    "Do you agree? (y/n): "
    answer = ["N"]
    name_post_exists = True
    with open(name_pre, "w+", encoding="utf-8") as f:
        text = "\n".join(PHRASES)
        f.write(text)
    with open("phrase_addresses.txt", "w+", encoding="utf-8") as f:
        text = "\n".join(PHRASE_ADDRESSES)
        f.write(text)
    if not os.path.exists(name_post):
        name_post_exists = False
    else:
        for i in range(APPROVE_NUM):
            approve_question = f"{approve} | {question}"
            answers.append(input(approve_question.format(i + 1, APPROVE_NUM)))
    try:
        if not name_post_exists or all([answer[0].capitalize() == "Y" for answer in answers]):
            load(name_pre, name_post, mode="file")
            print(f"Successfully (re)writed \"{name_post}\"!")
        else:
            print(f"Did't rewrite \"{name_post}\" because of ambigue answers. Abort.")
    except IndexError:
        print("You've answered nothing once or more times! Abort!")


def patch_based_on_translated_named_phrases():
    reload("patched", mode="dir")
    with open("phrases_translated.txt", "r", encoding="utf-8") as translation_file, \
         open("phrase_addresses.txt", "r", encoding="utf-8") as address_file:
        phrases_translated = translation_file.readlines()
        phrases_translated = [line.rstrip() for line in phrases_translated]
        phrases_translated = [re.split(":", line) for line in phrases_translated]
        phrases_translated = ["".join(phrase).lstrip() for (total_line_num, name, *phrase) in phrases_translated]
        phrase_addresses = address_file.readlines()
        phrase_addresses = [line.rstrip() for line in phrase_addresses]
        phrase_addresses = [line.split("/") for line in phrase_addresses]
        occs = {}
        for filename in os.listdir("not_patched"):
            occs[filename] = [i for i, phrase_address in enumerate(phrase_addresses) if phrase_address[1] == filename]
        for filename in os.listdir("not_patched"):
            with open(os.path.join("not_patched", filename), "r", encoding="utf-8") as not_patched_file, \
                 open(os.path.join("patched", filename), "w", encoding="utf-8") as patched_file:
                lines = not_patched_file.readlines()
                lines = [line.rstrip() for line in lines]
                for occ in occs[filename]:
                    total_line_num, filename, actual_line_num, idx, jdx = phrase_addresses[occ]
                    line_i = int(actual_line_num) - 1
                    idx, jdx = int(idx), int(jdx)
                    phrase_translated = phrases_translated[occ]
                    line_translated = f"{lines[line_i][:idx]}" + \
                    f"{phrase_translated}{lines[line_i][jdx:]}"
                    lines[line_i] = line_translated
                text = "\n".join(lines)
                patched_file.write(text + "\n")


def main():
    HELP_MSGS = [
        "replace the original content with new version",
        "specify only if original content is in Russian and needs decipherment",
        "specify only if want to translate emoticons in Esperanto (one-way)",
    ]
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--patch", dest="patch",
                        help=HELP_MSGS[0], action="store_true", default=False)
    parser.add_argument("-r", "--rus", dest="decipher_russification",
                        help=HELP_MSGS[1], action="store_true", default=False)
    parser.add_argument("-e", "--emoticons", dest="translate_emoticons",
                        help=HELP_MSGS[2], action="store_true", default=False)
    args = parser.parse_args()

    if args.patch:
        patch_based_on_translated_named_phrases()
    else:
        extract_named_phrases(args.decipher_russification, args.translate_emoticons)
        collect_named_phrases()


if __name__ == "__main__":
    main()
