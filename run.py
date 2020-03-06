from typing import List

import argparse
import string
import subprocess
import sys


def main(argv: List[str]) -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("script")
    parser.add_argument("cpg_file")
    parser.add_argument("--joern_path", default="./joern")

    args = parser.parse_args(argv)

    script_scala_path = args.script + ".scala"
    txt_script_to_scala(args.script, script_scala_path)

    command = "{joern_path} --script {script} --params payload={cpg_file}".format(
        joern_path=args.joern_path, script=script_scala_path, cpg_file=args.cpg_file,
    ).split(" ")

    print(" ".join(command))

    subprocess.run(command, check=True)


def txt_script_to_scala(txt_script_path: str, scala_script_path: str) -> None:
    with open(txt_script_path, "r") as input_stream:
        txt_script = "\n".join(
            (line for line in input_stream if not line.strip().startswith("#"))
        )

    template = string.Template(
        "\n".join(
            [
                "@main def exec(payload: String) = {",
                "\tloadCpg(payload)",
                "\t$script",
                "}",
            ]
        )
    )

    with open(scala_script_path, "w") as output_stream:
        output_stream.write(template.substitute({"script": txt_script}))


if __name__ == "__main__":
    main(sys.argv[1:])
