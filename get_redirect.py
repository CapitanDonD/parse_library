

import requests


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def main():
    print()


if __name__ == '__main__':
    main()
