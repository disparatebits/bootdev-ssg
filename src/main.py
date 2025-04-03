import os
import shutil

from helper import generate_page, copy_static_files, generate_pages_recursive


def main():
    src = 'static'
    dst = 'public'
    template_path = 'template.html'
    shutil.rmtree(dst, ignore_errors=True)
    copy_static_files(src, dst)

    generate_pages_recursive('content', template_path, dst)
    # generate_page('content/index.md', template_path, os.path.join(dst, 'index.html'))


if __name__ == '__main__':
    main()
