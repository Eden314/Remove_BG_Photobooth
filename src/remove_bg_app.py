"""Remove_BG-only entry point; interactive directory watching is Photobooth-only."""

from remove_background import main


if __name__ == "__main__":
    raise SystemExit(main(allow_watch=False))
