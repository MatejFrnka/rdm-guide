# main file: dmp_q_explained
import re

import pandas as pd

files = [
    "datasets_info",
    "sharing_reuse",
    "doc_metadata",
    "costs_sharing_reuse",
    "storage_during",
    "long_term",
    "responsibilities",
    "ethical_legal_issues",
    "other",
    "project_admin_info",
    "dmp_version_info",
]


def parse_file(file):
    with open(f"./pages/{file}.md", "r") as f:
        content = f.read()

        # Split sections clearly using a more specific approach to avoid mis-parsing
        sections = re.split(r"\n##\s", content)

        final_parsed_data = []

        for section in sections[1:]:  # Skip header part
            section_lines = section.splitlines()
            title = section_lines[0].strip()  # Section title

            # Extract Meaning
            meaning = None
            if "\n### Meaning" in section:
                meaning_part = re.search(r"### Meaning(.*?)### Example answers", section, re.DOTALL)
                if meaning_part:
                    meaning = meaning_part.group(1).strip()

            # Extract Example Answers
            example_answers = None
            if "\n### Example answers" in section:
                example_part = re.search(r"### Example answers(.*?)### Mapping among funders' DMP templates", section,
                                         re.DOTALL)
                if example_part:
                    example_answers = example_part.group(1).strip()

            # Extract and restructure Mapping
            mappings = []
            if "\n### Mapping among funders' DMP templates" in section:
                mapping_part = re.search(r"### Mapping among funders' DMP templates(.*?)(\n##|\Z)", section, re.DOTALL)
                if mapping_part:
                    mapping_table = mapping_part.group(1).strip()
                    table_lines = mapping_table.split("\n")
                    for line in table_lines[2:]:  # Skip header rows
                        cells = line.split("|")
                        if len(cells) >= 4:
                            funder = cells[1].strip()
                            dmp_section = cells[2].strip()
                            dmp_question = cells[3].strip()
                            if dmp_section.lower() != "na" and dmp_question.lower() != "na":
                                mappings.append((funder, dmp_section, dmp_question))

            # Append structured result, replicating rows for each mapping
            for mapping in mappings:
                final_parsed_data.append({
                    "File": file,
                    "Point": title,
                    "Meaning": meaning,
                    "Example Answers": example_answers,
                    "Funder": mapping[0],
                    "DMP Section": mapping[1],
                    "DMP Question": mapping[2],
                })

        # Convert the final structured data into a DataFrame
        return final_parsed_data


all = []

for file in files:
    result = parse_file(file)
    all += (result)
df = pd.DataFrame(all)
df.to_csv("parsed.csv", index=False)
