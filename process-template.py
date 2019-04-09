#!/usr/bin/env python
import argparse
import jinja2
import os
import platform
import re
import shutil
import six
import stat
import sys

__tht_root_dir = os.path.dirname(os.path.dirname(__file__))


def _shutil_copy_if_not_same(src, dst):
    """Copy with shutil ignoring the same file errors."""
    if hasattr(shutil, 'SameFileError'):
        try:
            shutil.copy(src, dst)
        except shutil.SameFileError:
            pass
    else:
        try:
            shutil.copy(src, dst)
        except Exception as ex:
            if 'are the same file' in six.text_type(ex):
                pass
            else:
                raise


def parse_opts(argv):
    parser = argparse.ArgumentParser(
        description='Configure jinja2 templates according to added arguments.')
    parser.add_argument('--OS', metavar='OS',
                        help="""Choose Mellanox nic . (choices: %(choices)s) (default: %(default)s)""",
                        choices=['RHEL', 'SLES'],
                        default='RHEL')
    parser.add_argument('-p', '--base_path', metavar='BASE_PATH',
                        help="""base path of templates to process. (default: %(default)s)""",
                        default='.')
    parser.add_argument('-o', '--output-dir', metavar='OUTPUT_DIR',
                        help="""Output dir for all the templates. (default: %(default)s)""",
                        default='')
    opts = parser.parse_args(argv[1:])

    return opts


def _j2_render_to_file(j2_template, j2_data, outfile_name=None):
    yaml_f = outfile_name or j2_template.replace('.j2.yaml', '.yaml')
    amend = 'rendering'
    print('{0} j2 template to file: {1}'.format(amend, outfile_name))

    # Search for templates relative to the current template path first
    template_base = os.path.dirname(yaml_f)
    j2_loader = jinja2.loaders.FileSystemLoader(
        [template_base, __tht_root_dir])

    try:
        # Render the j2 template
        template = jinja2.Environment(loader=j2_loader).from_string(
            j2_template)
        r_template = template.render(**j2_data)
    except jinja2.exceptions.TemplateError as ex:
        error_msg = ("Error rendering template {0} : {1}".format(yaml_f,
                                                                 six.text_type(
                                                                     ex)))
        print(error_msg)
        raise Exception(error_msg)
    with open(outfile_name, 'w') as out_f:
        out_f.write(r_template)


def process_templates(template_path, output_dir, opts):
    if output_dir and not os.path.isdir(output_dir):
        if os.path.exists(output_dir):
            raise RuntimeError(
                'Output dir {0} is not a directory'.format(output_dir))
        os.mkdir(output_dir)

    if os.path.isdir(template_path):
        for subdir, dirs, files in os.walk(template_path):
            dirs[:] = [d for d in dirs if not d[0] == '.']
            files = [f for f in files if not f[0] == '.']
            out_dir = subdir
            if output_dir:
                out_dir = os.path.join(output_dir, subdir)
                if not os.path.exists(out_dir):
                    os.mkdir(out_dir)
            for f in files:
                if f.endswith('.j2') and output_dir:
                    _shutil_copy_if_not_same(os.path.join(subdir, f), out_dir)
            for f in files:
                file_path = os.path.join(subdir, f)
                if f.endswith('.j2.yaml'):
                    print("jinja2 rendering normal template {0}".format(f))
                    with open(file_path) as j2_template:
                        template_data = j2_template.read()
                        j2_data = {'params': opts}
                        out_f = os.path.basename(f).replace('.j2.yaml',
                                                            '.yaml')
                        out_f_path = os.path.join(out_dir, out_f)
                        _j2_render_to_file(template_data, j2_data, out_f_path)
                elif f.endswith(('.j2.sh')):
                    print("jinja2 rendering normal template {0}".format(f))
                    with open(file_path) as j2_template:
                        template_data = j2_template.read()
                        j2_data = {'params': opts}
                        out_f = os.path.basename(f).replace('.j2.sh', '.sh')
                        out_f_path = os.path.join(out_dir, out_f)
                        _j2_render_to_file(template_data, j2_data, out_f_path)
                        st = os.stat(out_f_path)
                        os.chmod(out_f_path, st.st_mode | stat.S_IEXEC)
                elif f.endswith(('.j2.txt')):
                    print("jinja2 rendering normal template {0}".format(f))
                    with open(file_path) as j2_template:
                        template_data = j2_template.read()
                        j2_data = {'params': opts}
                        out_f = os.path.basename(f).replace('.j2.txt', '.txt')
                        out_f_path = os.path.join(out_dir, out_f)
                        _j2_render_to_file(template_data, j2_data, out_f_path)
                elif f.endswith(('.j2.py')):
                    print("jinja2 rendering normal template {0}".format(f))
                    with open(file_path) as j2_template:
                        template_data = j2_template.read()
                        j2_data = {'params': opts}
                        out_f = os.path.basename(f).replace('.j2.py', '.py')
                        out_f_path = os.path.join(out_dir, out_f)
                        _j2_render_to_file(template_data, j2_data, out_f_path)
                elif output_dir:
                    _shutil_copy_if_not_same(os.path.join(subdir, f), out_dir)
'
process_templates(opts.base_path, opts.output_dir, opts)
