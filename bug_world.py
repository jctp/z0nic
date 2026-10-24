import sys
import traceback
import os

RED = "\033[31m"
ORANGE = "\033[38;5;208m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
CYAN = "\033[36m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
WHITE = "\033[37m"
RESET = "\033[0m"

BOLD = "\033[1m"
BLINK = "\033[5m"


def _print_banner(message, exc_traceback=None):
    os.system("clear")

    out = sys.stderr
    print(f"{RED}={RESET}" * 80, file=out)
    print(
        f"{BOLD}{BLINK}{GREEN}O-{CYAN}^v^v^{GREEN}-{RED} WELCOME TO BUG WORLD {GREEN}-{CYAN}^v^v^{GREEN}-O{RESET}",
        file=out,
    )
    print(f"{BLUE}Z0NIC{RESET} couldn't hack it anymore, and died.")
    print(f"{RED}-{RESET}" * 80, file=out)
    print(f"{BOLD}{RED}BLAME THIS:{RESET} {message}.", file=out)
    print(f"{BLUE}={RESET}" * 80, file=out)
    if exc_traceback is not None:
        traceback.print_tb(exc_traceback)
    else:
        traceback.print_stack(sys._getframe(2))
    print(f"{BLUE}-{RESET}" * 80, file=out)


def enter_bug_world(message):
    # Called by the CPU and I/O layers when emulation cannot continue.
    _print_banner(message)
    raise SystemExit(1)


def bug_world_excepthook(exc_type, exc_value, exc_traceback):
    # Installed as sys.excepthook: prints the banner and returns, so Python exits with status 1.
    if issubclass(exc_type, SystemExit):
        return
    _print_banner(f"{exc_type.__name__}: {exc_value}", exc_traceback)


def install_excepthook():
    sys.excepthook = bug_world_excepthook
