#!/bin/sh

# a small packaging helper
# ref: https://packaging.python.org/en/latest/tutorials/packaging-projects/

function f_usage() {
    echo
    echo "Usage: $0 <subcommand>"
    echo "Subcommands:"
    echo "  build       build the latest distribution"
    echo "  test-upload upload a build to test pypi"
    echo "  upload      upload a build to pypi"
}

# parse commandline arguments
subcommand=$1
case $subcommand in
    "" | "usage" | "-h" | "--help")
        f_usage
        ;;
    "build")
        rm -Rf build/
        python -m build
        ;;
    "test-upload")
        python -m twine upload --repository testpypi dist/*
        ;;
    "upload")
        python -m twine upload --repository pypi dist/*
        ;;
    *)
        echo "unknown command. check usages."
        ;;
esac

