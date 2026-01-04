"""
Entry point shim for ChainCredit.
Delegates to cli.main for backward-compatible `python main.py` usage.
"""
from cli.main import main


if __name__ == "__main__":
    main()
