"""Photobooth-only entry point; keeps one model session alive for the session."""

from remove_background import main


if __name__ == "__main__":
    raise SystemExit(main(force_watch=True))
