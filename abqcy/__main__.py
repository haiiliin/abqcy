import fire

from abqcy.cli import AbqcyCLI


def main():
    fire.core.Display = lambda lines, out: out.write("\n".join(lines) + "\n")
    fire.Fire(AbqcyCLI)


if __name__ == "__main__":
    main()
