import os
import sys
import shutil

from helper import generate_page, copy_static_files, generate_pages_recursive


def main():
    if len(sys.argv) < 1:
        basepath = sys.argv[1]
    else:
        basepath = '/'



    src = 'static'
    dst = 'docs'
    template_path = 'template.html'
    shutil.rmtree(dst, ignore_errors=True)
    copy_static_files(src, dst)

    generate_pages_recursive('content', template_path, dst, basepath)
    # generate_page('content/index.md', template_path, os.path.join(dst, 'index.html'), basepath)


if __name__ == '__main__':
    main()
