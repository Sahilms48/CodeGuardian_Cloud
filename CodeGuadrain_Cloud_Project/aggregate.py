import os
import shutil

def aggregate(result=""):
    report_dir = "reports"
    output_file = "document.md"

    # Check if report directory exists
    if not os.path.exists(report_dir):
        print(f"The directory '{report_dir}' does not exist.")
        return result

    # Walk through the directory tree and read .md files
    for root, dirs, files in os.walk(report_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as md_file:
                        result += md_file.read() + "\n\n"
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")

    # Write the aggregated result to document.md
    try:
        with open(output_file, 'w', encoding='utf-8') as output_md:
            output_md.write(result)
        print(f"Aggregated content written to '{output_file}'")
    except Exception as e:
        print(f"Error writing to '{output_file}': {e}")

    return result

import os
import shutil

def delete_results():
    report_dir = "reports"
    files_to_delete = ["document.md", "final_report.md"]

    # Delete the report directory if it exists
    if os.path.exists(report_dir):
        try:
            shutil.rmtree(report_dir)
            print(f"Deleted '{report_dir}' folder.")
        except Exception as e:
            print(f"Error deleting '{report_dir}': {e}")
    else:
        print(f"'{report_dir}' folder does not exist.")

    # Delete specified files if they exist
    for file_name in files_to_delete:
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
                print(f"Deleted '{file_name}'.")
            except Exception as e:
                print(f"Error deleting '{file_name}': {e}")
        else:
            print(f"'{file_name}' does not exist.")


