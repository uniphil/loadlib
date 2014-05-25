
import os
import json
import glob
import shutil
import markdown


get_src = lambda *p: os.path.join('src', *p)
get_dest = lambda *p: os.path.join('data', *p)


def copy(what, src='', dest=''):
    src_prefix = get_src(src)
    dest_folder = get_dest(dest)

    if not os.path.isdir(dest_folder):
        os.makedirs(dest_folder)

    copied = []
    for w in what:

        what_src = get_src(src, w)
        for globbed in glob.glob(what_src):

            name = globbed[len(src_prefix):]

            dest_parts = os.path.split(name)
            if dest_parts[0] != '':
                dest_path = os.path.join(dest_folder, dest_parts[0])
                if not os.path.exists(dest_path):
                    os.makedirs(dest_path)
                else:
                    print('folder already exists')

            final_dest = os.path.join(dest_folder, name)

            if os.path.isdir(globbed):
                shutil.copytree(globbed, final_dest)
            elif os.path.isfile(globbed):
                shutil.copy(globbed, final_dest)
            else:
                raise ValueError('not a file or dir? {}'.format(src))
            copied.append(final_dest[len('data/'):])
    return copied


def each_dir(root, src=''):
    r = get_src(src, root)
    for dir_ in os.listdir(r):
        rdir = os.path.join(r, dir_)
        if not os.path.isdir(rdir):
            raise ValueError('expected directories in {}. '
                             '{} is not a directory :('.format(r, rdir))
        in_dir = os.listdir(rdir)
        files = filter(lambda p: os.path.isfile(os.path.join(rdir, p)), in_dir)
        src_path = os.path.join(root, dir_)
        yield src_path + '/', dir_, files


def load_markdown(fname, src=''):
    with open(get_src(src, fname)) as f:
        src = f.read()
        rendered = markdown.markdown(src)
    return rendered


def load_json(fname, src=''):
    with open(get_src(src, fname)) as f:
        data = json.load(f)
    return data


def write_json(obj, dest):
    with open(get_dest(dest), 'wb') as f:
        json.dump(obj, f, indent=2)
