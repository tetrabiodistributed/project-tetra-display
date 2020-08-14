import sys

from server import Communicator


def main(message):
    Communicator().publish_message(message)


if "__main__" == __name__:
    main(sys.argv[2])
