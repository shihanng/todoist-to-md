import json
import os
import re
import string
import unicodedata

import click
from jinja2 import Environment, FileSystemLoader, select_autoescape

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
char_limit = 252


def slugify(value, allow_unicode=True):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")[:char_limit]


@click.command()
@click.argument("input")
@click.argument("output")
def main(input, output):
    with open(input, "r") as f:
        data = json.load(f)

    env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
    t = env.get_template("template.md")

    os.makedirs(output, exist_ok=True)

    for d in data:
        render = t.render(d)

        fn = slugify(d["content"])

        with open(os.path.join(output, f"{fn}.md"), "w") as f:
            f.write(render)


if __name__ == "__main__":
    main()
