import re


def print_summary(title):

    return f"<summary>{title.strip()}</summary>\n"


file_name = "/tmp/python-diff"
file = open(file_name, "r")
lines = file.readlines()

res_index = -1
resources = []
char_count = 0

details_header = "<details>\n"
details_footer = "</details>\n"
diff_header = "\n```diff\n"
diff_footer = "```\n"

for line in lines:
    if re.match("=====.+======", line):
        res_index += 1
        resources.append({"title": "", "body": ""})
        resources[res_index]["title"] += line
    else:
        resources[res_index]["body"] += line

comment = ""
part_number = 1

for resource in resources:
    candidate_res = (
        details_header
        + print_summary(resource["title"])
        + diff_header
        + resource["body"]
        + diff_footer
        + details_footer
    )
    if len(candidate_res) > 65000:
        # print(f'resource {resource["title"]} is too large with size {len(candidate_res)}')
        continue
    if len(comment) + len(candidate_res) > 65000:
        with open(f"{file_name}-part{part_number}", "w") as writer:
            writer.writelines(comment)
        comment = ""
        part_number += 1
    else:
        comment += candidate_res

with open(f"{file_name}-part{part_number}", "w") as writer:
    writer.writelines(comment)
