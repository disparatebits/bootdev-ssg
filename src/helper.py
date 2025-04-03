import os
import shutil

from blocks import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith('#'):
            return line[2:].strip()
    raise Exception("no title found")


def copy_static_files(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst)
    src_contents = os.listdir(src)
    for filename in src_contents:
        src_path = os.path.join(src, filename)
        dst_path = os.path.join(dst, filename)
        print(f"Copying {src_path} to {dst_path}")
        if os.path.isdir(src_path):
            try:
                copy_static_files(src_path, dst_path)
            except Exception as e:
                print(f"Failed to copy {filename}: {e}")
        elif os.path.isfile(src_path):
            try:
                shutil.copy(src_path, dst)
            except Exception as e:
                print(f"Failed to copy {filename}: {e}")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from: {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        contents = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template_contents = f.read()
    html_string = markdown_to_html_node(contents)
    html = html_string.to_html()
    title = extract_title(contents)
    modified_template = template_contents
    modified_template = modified_template.replace('{{ Title }}', title)
    modified_template = modified_template.replace('{{ Content }}', html)
    modified_template = modified_template.replace('href="/', f'href="{basepath}')
    modified_template = modified_template.replace('src="/', f'src="{basepath}')
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(modified_template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    dir_contents = os.listdir(dir_path_content)
    with open(template_path, "r", encoding="utf-8") as f:
        template_contents = f.read()
    for filename in dir_contents:
        full_path = os.path.join(dir_path_content, filename)

        if os.path.isdir(full_path):
            new_dest_dir = os.path.join(dest_dir_path, filename)
            os.makedirs(new_dest_dir, exist_ok=True)

            generate_pages_recursive(full_path, template_path, new_dest_dir, basepath)
        elif filename.endswith(".md"):
            with open(full_path, "r", encoding="utf-8") as f:
                contents = f.read()
                html_string = markdown_to_html_node(contents)
                html = html_string.to_html()
                title = extract_title(contents)

                modified_template = template_contents
                modified_template = modified_template.replace('{{ Title }}', title)
                modified_template = modified_template.replace('{{ Content }}', html)
                modified_template = modified_template.replace('href="/', f'href="{basepath}')
                modified_template = modified_template.replace('src="/', f'src="{basepath}')
                output_filename = filename.replace(".md", ".html")
                output_path = os.path.join(dest_dir_path, output_filename)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(modified_template)
