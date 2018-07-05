#!/usr/bin/env python
import os
import shutil


BASE_PATH = os.path.dirname(os.path.abspath(__file__))

STRUCTURE = {
    'getting_started': ['overview',
                        '10min',
                        'tutorials',
                        'cookbook',
                        'dsintro',
                        'basics'],
    'user_guide': ['text',
                   'options',
                   'indexing',
                   'advanced',
                   'computation',
                   'missing_data',
                   'groupby',
                   'merging',
                   'reshaping',
                   'timeseries',
                   'timedeltas',
                   'categorical',
                   'visualization',
                   'style',
                   'io',
                   'enhancingperf',
                   'sparse',
                   'gotchas'],
    'ecosystem': ['comparison_with_r',
                  'comparison_with_sas',
                  'comparison_with_sql',
                  'comparison_with_stata',
                  'r_interface',
                  'ecosystem'],
    'developers': ['contributing',
                   'contributing_docstring',
                   'developer',
                   'internals',
                   'extending'],
}


def change_rst_structure(pandas_path, structure):
    """
    Move rst files into subdirectories of the source directory.
    """
    source_path = os.path.join('doc', 'source')

    for dirname, fnames in structure.items():
        dirname = os.path.join(source_path, dirname)
        os.makedirs(os.path.join(pandas_path, dirname), exist_ok=True)

        sources = []
        for fname in fnames:
            source = os.path.join(source_path, fname + '.rst')
            target = os.path.join(dirname, fname + '.rst')
            try:
                os.rename(os.path.join(pandas_path, source),
                          os.path.join(pandas_path, target))
            except FileNotFoundError:
                pass
            sources.append(source)

        print('git add {}'.format(dirname))
        print('git rm {}'.format(' '.join(sources)))


def add_dependencies(pandas_path):
    """
    Adding the new theme to the dependencies.
    """
    fname = os.path.join('ci', 'environment-dev.yaml')
    with open(os.path.join(pandas_path, fname), 'a') as f:
        f.write('  - sphinx_bootstrap_theme\n')

    print('git add {}'.format(fname))


def update_conf(pandas_path):
    """
    Make changes to the documentation configuration file to use the new theme
    with the desired settings.
    """
    fname = os.path.join(pandas_path, 'doc', 'source', 'conf.py')

    content = []
    with open(os.path.join(pandas_path, fname)) as f:
        for line in f:
            if line == 'import warnings\n':
                line = 'import warnings\n'
                line += 'import sphinx_bootstrap_theme\n'
            if line == "html_theme = 'nature_with_gtoc'\n":
                line = "html_theme = 'bootstrap'\n"
            elif line == "# html_theme_options = {}\n":
                line = 'html_theme_options = {\n'
                line += '}\n'
            elif line == "html_theme_path = ['themes']\n":
                line = 'html_theme_path = '
                line += 'sphinx_bootstrap_theme.get_html_theme_path()\n'
            content.append(line)

    with open(os.path.join(pandas_path, fname), 'w') as f:
        for line in content:
            f.write(line)

    print('git add {}'.format(fname))


def remove_old_theme(pandas_path):
    """
    Remove the old theme. Do it by removing the whole themes directory, as the
    new theme is installed as a dependency.
    """
    themes_dir = os.path.join('doc', 'source', 'themes')
    shutil.rmtree(themes_dir)

    print('git rm {}'.format(themes_dir))


def main(pandas_path):
    change_rst_structure(pandas_path, STRUCTURE)
    add_dependencies(pandas_path)
    update_conf(pandas_path)
    remove_old_theme(pandas_path)


if __name__ == '__main__':
    # TODO replace by path to pandas, not this repo, when ready to refactor it
    pandas_path = BASE_PATH
    main(pandas_path)