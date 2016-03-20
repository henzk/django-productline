from __future__ import absolute_import
from __future__ import print_function
import os
import sys
import argparse


class CommandLineParser(object):
    """
    Wrapper around argsparse.ArgumentParser. Encapsulates
    arg parsing and the construction of variables, such as the djpl_install_args which
    may be the stable djple version from pypie or a specific commit.

    In fact this class encapsulates the variability originating from several script
    arguments to one common api. The installation routine thus only uses this
    api without bothering about python version for virtualenv or djpl version/commit id.
    """

    def __init__(self):
        """
        Initializes the argparser.
        """

        parser = argparse.ArgumentParser(description='Process some integers.')
        parser.add_argument(
            'ape_root_dir',
            type=str,
            help='Specifies the APE_ROOT_DIR. This is where your projects will live in.'
        )
        parser.add_argument(
            '--c', type=str,
            dest='commit_id',
            help='Use this option to install a specific commit of django productline'
        )
        parser.add_argument(
            '--v', type=str,
            dest='version',
            help='Use this option to install a specific version of django productline'
        )
        parser.add_argument(
            '--p',
            type=str,
            dest='python_executable',
            help='Use this option to pass a custom python executable. E.g. to use Python 3.'
        )

        self.arg_dict = parser.parse_args()

        if self.arg_dict.version and self.arg_dict.commit_id:
            raise VersionCommitIdClash()

    def get_webapps_dir(self):
        """
        Return sthe abs path to the webapps directory.
        :return:
        """
        return '%s/%s' % (os.getcwd(), self.arg_dict.ape_root_dir)

    def get_pyexec_arg(self):
        """
        Returns the commoand which must be further passed to the ape
        install script to use a specific python version.
        :return:
        """
        """
        :return:
        """
        if self.arg_dict.python_executable:
            return '--p %s' % self.arg_dict.python_executable
        else:
            return ''

    def get_djpl_install_cmd(self):
        """
        Returns an argument list for pip installation encapsulating the variability of
        user-specified version, commit id or latest stable.
        :return:
        """

        if self.arg_dict.commit_id:
            cmd_parts = [
                'pip',
                'install',
                '-e',
                'git+https://github.com/henzk/django-productline.git@%(commit_id)s#egg=django-productline' % dict(
                    commit_id=self.arg_dict.commit_id
                )
            ]
        elif self.arg_dict.version:
            cmd_parts = [
                'pip',
                'install',
                'django-productline==%(version)s' % dict(
                    version=self.arg_dict.version
                )
            ]
        else:
            cmd_parts = [
                'pip',
                'install',
                'django-productline'
            ]

        return ' '.join(cmd_parts)


def main(args):
    """
    :param args:
    :return:
    """

    cmd_parser = CommandLineParser()

    DJPL_INSTALL_CMD = cmd_parser.get_djpl_install_cmd()
    WEBAPPS_DIR = cmd_parser.get_webapps_dir()
    PYEXEC_ARG = cmd_parser.get_pyexec_arg()

    cmds = (
        #'wget -O -'
        #'https://raw.github.com/henzk/ape/master/bin/bootstrape | python -'
        ' python ape/bin/ape_install.py'
        ' %(ape_root)s'
        ' %(ape_pyexec)s;'
        ' cd %(ape_root)s;'
        ' . _ape/activape;'
        ' %(djpl_install_cmd)s; '
        % dict(
            ape_root=WEBAPPS_DIR,
            ape_pyexec=PYEXEC_ARG,
            djpl_install_cmd=DJPL_INSTALL_CMD
        )
    )

    print(cmds)


    os.system('bash -c "%s deactivape"; ' % cmds)
    # add initenv on ape container level
    with open('%s/initenv' % WEBAPPS_DIR, 'w+') as initenv:
        initenv.write('export APE_PREPEND_FEATURES="ape.container_mode django_productline"')


if __name__ == '__main__':
    main(sys.argv)
