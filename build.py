from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin("python.pydev")
use_plugin("python.pycharm")

name = "elk_mongo"
default_task = "publish"


@init
def set_properties(project):
    pass
