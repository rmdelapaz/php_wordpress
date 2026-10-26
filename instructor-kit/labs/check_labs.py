#!/usr/bin/env python3
"""Run every lab of the PHP and WordPress Development instructor kit on a real WordPress 7.1 site; PASS/FAIL.

For each labs/module-NN/ folder (one folder per 3-hour session) this installs and runs, on a FRESH copy of the
site at the state the lab declares:

  * every  *_starter.php / *_starter.sh    must run without any PHP or WordPress message exactly as handed out
                                           (TODOs and all) and print what its "// expect:" lines say;
  * every  *_solution.php / *_solution.sh  must run without any message and print its "// expect:" lines;
  * every  debug_*.php / debug_*.sh        a deliberately broken handout: it MUST produce messages, and only the
                                           kinds its header declares ("// expect-error: Deprecated, Warning");
  * every  test_*.php / test_*.sh          the test of a FOLDER lab: the checker installs <name>_starter/ (then
                                           <name>_solution/) as a plugin, must-use plugin or theme, and runs the
                                           test once per folder (see FOLDER LABS);
  * every  check_*.php / check_*.sh        support tools (check_environment.sh: "# host: compose", see below);
and lints (php -l) every other .php file (includes, the files of a folder lab).

HOW A LAB RUNS (the same way a learner runs it, Lesson 1.2's health-check pattern)
  A .php file is copied into the WordPress root (the learner's wordpress/ folder = /var/www/html in the containers)
  and run with   wp eval-file --use-include <file>   (WordPress loaded; --use-include makes PHP's messages
  name the file itself, not WP-CLI's "eval()'d code"; "// user: admin" adds --user=admin, "// args: a b" passes
  arguments). A .sh file is copied there too and run with  sh <file>  in the WP-CLI container (cwd = the WordPress
  root; wp, curl and the usual tools are there; http://localhost:8080 is the site). Both run in a fake terminal,
  so WP-CLI draws its +----+ tables as on the learner's screen. The copied file is removed afterwards.

HEADER LINES (comments in the first 25 lines: //, #, or " * " inside a docblock)
    // state: fresh             the site the lab starts from: fresh (= the end of Lesson 1.2) or after:lesson_NN
                                (the state run_wp_blocks.py saved when that lesson PASSed). WARN when missing.
    // expect: All checks passed.      (repeatable) text the output must contain. Starters: what they print AS
                                SHIPPED (a TODO line); solutions: the answer. WARN when a starter/solution has none.
    // expect-starter: ... / // expect-solution: ...    (test files) the same, per installed folder
    // expect-error: Deprecated, Warning    (debug_* only, or a test of a debug_ folder) the message kinds it must
                                produce: PHP levels (Warning, Notice, Deprecated, Fatal error, Parse error), uncaught
                                exception classes (TypeError ...), doing_it_wrong (WordPress's "called incorrectly"),
                                Error (a WP-CLI "Error: ..." line)
    // serve: store_notice      (test_* only) the folder pair store_notice_starter/ + store_notice_solution/ (or one
                                folder named exactly store_notice/) next to the test
    // install: mu-plugin | plugin [slug] | theme [slug]      (test_* only) how the folder is installed: its files go
                                into wp-content/mu-plugins/, or the folder becomes wp-content/plugins/<slug>/ (then
                                wp plugin activate) or wp-content/themes/<slug>/ (then wp theme activate). The slug
                                defaults to the pair name with - for _ (store_notice -> store-notice).
    // user: admin   // args: --dry-run      eval-file options / script arguments
    # host: compose             (check_* .sh only) runs on the HOST in a Docker Compose project folder (see below)

WHAT FAILS A FILE
  * any PHP or WordPress message (Warning, Notice, Deprecated, Fatal error, Parse error, an uncaught exception,
    "called incorrectly") or a WP-CLI "Error:" line, in the output or newly written to wp-content/debug.log, unless
    it is a debug handout that declared exactly those kinds; a debug handout that produces none, or an undeclared one;
  * a non-zero exit status outside debug handouts; a timeout (default 120 s); a missing "// expect:" text;
  * LEFT FILES BEHIND: a lab that creates or changes files anywhere in the WordPress tree (other than its own copy,
    its installed folder and debug.log) fails: learners run these on their course site;
  * without running: a "$ " prompt line in a .sh file (learners would copy the $), shell_exec/exec/system/passthru/
    popen/proc_open or backticks in PHP outside check_* files.
  Database changes are not compared (every file runs on a fresh copy); labs that change content say in their
  README how to undo it, or undo it themselves.

FOLDER LABS. A plugin, must-use plugin or theme the learner writes: <name>_starter/ and its twin <name>_solution/
next to a test_<name>.php (wp eval-file; it can request pages with wp_remote_get( home_url( '/' ) )) or a
test_<name>.sh (curl http://localhost:8080/..., wp commands). Learners copy the folder into wp-content (the
README gives the commands), activate it, and run the test the same way as any lab file.

WHERE IT RUNS (first match wins)
  1. WP_LABS_COMPOSE=~/pagesco-dev   YOUR Lesson 1.2 project (buyers, instructors): every lab runs on your site
     through  docker compose run --rm wpcli ... . Before each file the checker saves your database
     (wp db export into wordpress/.wp-labs-snapshot.sql), installs the lab, runs it, removes what it installed and
     imports the snapshot again, so the site is left as it was. Your site must be at the state the lab declares
     (the checker prints it); a lab that needs "after:lesson_13" on a fresh site may fail for that reason alone.
     Labs marked "# host: compose" run in your project folder too (they are meant to).
  2. The course author's runner (~/projects/_kit_tools/php_wordpress/wpkit.py + Docker): a fresh throwaway site per
     file at the declared state (the same images and settings as pagesco-dev: WordPress 7.1.3, PHP 8.5, MySQL 9.7,
     WP-CLI 2.12, Mailpit), containers wpc-web-k<NN>-* / wpc-cli-k<NN>-*. "# host: compose" files get a real
     throwaway Compose project built from the course's downloads/pagesco-dev/ (project wpc-k<NN>-env, other host
     ports; removed with down -v afterwards; --no-host skips them). WP_LABS_PHP=8.4 runs on PHP 8.4.
  Output is normalized the way the lessons show it: the runner's per-run database name prints as "wordpress",
  the checker's host ports as 8080 / 8025.

Usage (from anywhere; system python3 3.8+, standard library only):
    python3 labs/check_labs.py                 # all sessions
    python3 labs/check_labs.py module-01       # one session (also 01 or 1; several allowed)
    python3 labs/check_labs.py module-01 -v    # also show what each file printed
    python3 labs/check_labs.py --file labs/module-01/l1_2-local-environment/site_report_solution.sh -v
    python3 labs/check_labs.py --no-host       # skip "# host: compose" files (they take about a minute)
    python3 labs/check_labs.py --strict        # all sessions; a session with no labs is a failure
Exit code: 0 when everything passed, 1 otherwise.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from argparse import Namespace
from pathlib import Path

LABS = Path(__file__).resolve().parent
KIT = LABS.parent
COURSE_DIR = KIT.parent
COURSE_TOOLS = Path.home() / "projects" / "_kit_tools" / "php_wordpress"
WP_ROOT = "/var/www/html"
DEFAULT_TIMEOUT = 120
IGNORE_DIRS = {"_lib", "_fixtures", "__pycache__", "tmp", "node_modules"}
RUN_EXT = (".php", ".sh")

HEAD_KEYS = ("state", "expect", "expect-starter", "expect-solution", "expect-error", "serve", "install", "user",
             "args", "host")
HEAD_RE = re.compile(r"^\s*(?://|#|\*)\s*(" + "|".join(re.escape(k) for k in sorted(HEAD_KEYS, key=len, reverse=True))
                     + r")\s*:\s*(.*?)\s*(?:\*/)?\s*$", re.I)
DIAG_RE = re.compile(r"^\s*(?:\[[^\]]*\]\s*)?(?:PHP )?(Fatal error|Parse error|Warning|Deprecated|Notice|"
                     r"Recoverable fatal error):\s+(?:Uncaught ([\w\\]+))?")
LOGSTAMP_RE = re.compile(r"\[\d\d-[A-Z][a-z]{2}-\d{4} \d\d:\d\d:\d\d [A-Z]{2,5}\]")
FORBIDDEN_PHP = [
    (re.compile(r"(?<![\w>$:])(shell_exec|exec|system|passthru|popen|proc_open)\s*\("), "runs shell commands"),
    (re.compile(r"(?m)^[^'\"\n]*`[^`\n]+`"), "uses the backtick operator (deprecated in 8.5, and it runs shell commands)"),
]
PROMPT_RE = re.compile(r"(?m)^\s*\$ \S")
# A saved site (the base install, a lesson's state) ages: its scheduled tasks (update checks ...) fall due, and the
# first request then runs them in the background (network calls, "Automatic updates starting..." in debug.log,
# files in wp-content/upgrade/). A learner's site, used every day, has none overdue. So the runner moves every
# overdue event one hour into the future before a lab runs (order kept, nothing run, nothing removed).
SETTLE_CRON = ("wp eval '$c = _get_cron_array(); $now = time(); $new = array(); $i = 0; "
               "foreach ( $c as $ts => $hooks ) { $t = $ts < $now + 600 ? $now + 3600 + ( $i++ ) : $ts; "
               "$new[ $t ] = isset( $new[ $t ] ) ? array_merge( $new[ $t ], $hooks ) : $hooks; } "
               "ksort( $new ); _set_cron_array( $new ); delete_transient( \"doing_cron\" );'")


# ------------------------------------------------------------------------------------------------ headers
def header(text: str) -> dict:
    """{key: value} from the first 25 lines; 'expect*' keys collect every line as a list."""
    h: dict = {}
    for ln in text.splitlines()[:25]:
        m = HEAD_RE.match(ln)
        if not m:
            continue
        k, v = m.group(1).lower(), m.group(2).strip()
        if k.startswith("expect") and k != "expect-error":
            h.setdefault(k, []).append(v)
        elif k not in h:
            h[k] = v
    return h


def kind_of(path: Path) -> str:
    n = path.name
    if path.suffix not in RUN_EXT:
        return "other"
    if n.startswith("debug_"):
        return "debug"
    if n.startswith("test_"):
        return "test"
    if n.startswith("check_"):
        return "support"
    if path.stem.endswith("_starter"):
        return "starter"
    if path.stem.endswith("_solution"):
        return "solution"
    return "include"


def diagnostics(text: str, cli: bool = True) -> list[tuple[str, str, str]]:
    """(level, exception class or '', line) for every PHP/WordPress message (CLI output, a page, or debug.log)."""
    plain = re.sub(r"<br\s*/?>", "\n", text)
    plain = re.sub(r"</?(b|strong|code)>", "", plain)
    plain = plain.replace("&quot;", '"').replace("&#039;", "'").replace("&amp;", "&").replace("&gt;", ">").replace("&lt;", "<")
    out = []
    for ln in plain.splitlines():
        ln2 = LOGSTAMP_RE.sub("", ln).strip()
        m = DIAG_RE.match(ln2)
        if m:
            level = m.group(1)
            if level == "Notice" and "was called incorrectly" in ln2:
                level = "doing_it_wrong"
            out.append((level, (m.group(2) or "").rsplit("\\", 1)[-1], ln2))
        elif cli and ln2.startswith("Error: "):
            out.append(("Error", "", ln2))
    return out


def diag_key(d) -> str:
    return re.sub(r"^(PHP )?[A-Za-z ]+:\s+", "", d[2]).strip()


def lesson_of(path: Path) -> Path:
    """labs/module-NN/<lesson>/ that holds this file."""
    rel = path.resolve().relative_to(LABS)
    return LABS / rel.parts[0] / rel.parts[1] if len(rel.parts) > 2 else path.parent


def session_tag(path: Path) -> str:
    m = re.match(r"module-(\d+)", path.resolve().relative_to(LABS).parts[0])
    return f"k{int(m.group(1)):02d}" if m else "kxx"


def snapshot(root: Path) -> dict:
    res = {}
    for dirpath, dirnames, filenames in os.walk(root):
        for f in filenames:
            p = Path(dirpath) / f
            try:
                st = p.stat()
            except OSError:
                continue
            res[str(p.relative_to(root))] = (st.st_size, st.st_mtime_ns)
    return res


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _q(s: str) -> str:
    return "'" + str(s).replace("'", "'\\''") + "'"


# ------------------------------------------------------------------------------------------------ backends
class Backend:
    """Where a lab runs. prepare(state) -> a fresh site; run(cmd) in the WP root; root = the WordPress folder."""
    name = ""
    root: Path

    def prepare(self, state: str) -> None:
        raise NotImplementedError

    def run(self, cmd: str, timeout: float) -> tuple[int, str]:
        raise NotImplementedError

    def log_size(self) -> int:
        p = self.root / "wp-content" / "debug.log"
        return p.stat().st_size if p.exists() else 0

    def log_since(self, size: int) -> str:
        p = self.root / "wp-content" / "debug.log"
        if not p.exists():
            return ""
        with open(p, "rb") as fh:
            fh.seek(size)
            return fh.read().decode("utf-8", "replace")

    def normalize(self, out: str) -> str:
        return out

    def cleanup_after(self) -> None:
        pass

    def close(self) -> None:
        pass


class RunnerSite(Backend):
    """A throwaway site from wpkit.py (the lesson runner's machinery): a copy of the base install or of a state."""

    def __init__(self, tag: str, ver: str):
        sys.path.insert(0, str(COURSE_TOOLS))
        import wpkit  # noqa: E402
        import run_wp_blocks  # noqa: E402
        self.wk, self.rpb, self.ver, self.tag = wpkit, run_wp_blocks, ver, tag
        self.site = None
        self.cur_state = None
        self.run_id = f"{tag}-labs-{os.getpid() % 100000}-{int(time.time() * 1000) % 10000}"
        self.db = "wpc_" + re.sub(r"[^a-z0-9]", "_", self.run_id)
        self.root = wpkit.WORK_ROOT / self.run_id
        self.args = Namespace(quiet=True, jobs=1, timeout=120.0, fill=False, no_save=False, keep=False, out=None)
        self.name = (f"the course runner (WordPress 7.1, PHP {ver}, MySQL 9.7, WP-CLI 2.12; "
                     f"containers wpc-web-{self.run_id}, wpc-cli-{self.run_id})")

    def _state_dir(self, state: str) -> Path:
        lr = self.rpb.LessonRun(self.wk.REPO / "lesson_01.html", self.args, self.ver)
        return lr.resolve_state(None if state == "fresh" else state)

    def prepare(self, state: str) -> None:
        src = self._state_dir(state)
        if self.site is None:
            self.wk.ensure_base(self.ver, lambda s: None)
            self.wk.copy_tree(src / "root", self.root)
            self.wk.create_db(self.db, src / "db.sql")
            self.site = self.wk.Site(self.run_id, self.ver, self.root, self.db)
            self.site.start()
        else:
            self.wk.restore(self.site, src)
        self.cur_state = state
        code, out = self.site.sh(SETTLE_CRON)
        if code:
            raise RuntimeError(f"could not settle the site's cron schedule: {out[-300:]}")

    def run(self, cmd: str, timeout: float) -> tuple[int, str]:
        code, out = self.site.sh(cmd, timeout=timeout, tty=True)
        return code, out

    def normalize(self, out: str) -> str:
        return out.replace(self.db, "wordpress")

    def close(self) -> None:
        if self.site:
            self.site.close()
        self.wk.drop_db(self.db)
        self.wk.clear_dir(self.root)


class ComposeSite(Backend):
    """Your own Lesson 1.2 project (WP_LABS_COMPOSE): docker compose run --rm wpcli ..., snapshot + restore."""

    def __init__(self, project: Path, env: dict | None = None):
        self.project = project
        if not (project / "compose.yaml").is_file():
            raise SystemExit(f"WP_LABS_COMPOSE={project}: no compose.yaml there (point it at your pagesco-dev folder)")
        self.root = project / "wordpress"
        self.env = dict(os.environ, **(env or {}))
        self.name = f"your Compose project {project} (docker compose run --rm wpcli)"
        self.snap = None

    def _compose(self, args: list[str], timeout: float = 300, tty: bool = False) -> tuple[int, str]:
        argv = ["docker", "compose", "--progress", "quiet"] + args
        try:
            if tty and shutil.which("script"):
                cmd = " ".join(_q(a) for a in argv)
                r = subprocess.run(["script", "-qec", cmd, "/dev/null"], cwd=self.project, capture_output=True,
                                   timeout=timeout, env=self.env, stdin=subprocess.DEVNULL)
            else:
                r = subprocess.run(argv, cwd=self.project, capture_output=True, timeout=timeout, env=self.env,
                                   stdin=subprocess.DEVNULL)
        except subprocess.TimeoutExpired as e:
            return 124, (e.stdout or b"").decode("utf-8", "replace") + f"\n[timed out after {timeout:.0f} s]"
        out = (r.stdout + r.stderr).decode("utf-8", "replace").replace("\r\n", "\n").replace("\r", "")
        out = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]", "", out)
        if out.startswith("^@"):
            out = out[2:]
        return r.returncode, out

    def prepare(self, state: str) -> None:
        code, out = self._compose(["run", "--rm", "-T", "wpcli", "wp", "db", "export", ".wp-labs-snapshot.sql", "--quiet"])
        if code:
            raise RuntimeError(f"could not save your database first (is the project running? docker compose up -d): {out[-300:]}")
        self.snap = self.root / ".wp-labs-snapshot.sql"

    def run(self, cmd: str, timeout: float) -> tuple[int, str]:
        return self._compose(["run", "--rm", "wpcli", "sh", "-c", cmd], timeout=timeout, tty=True)

    def cleanup_after(self) -> None:
        if self.snap and self.snap.exists():
            code, out = self._compose(["run", "--rm", "-T", "wpcli", "wp", "db", "import", ".wp-labs-snapshot.sql", "--quiet"])
            self.snap.unlink(missing_ok=True)
            if code:
                raise RuntimeError(f"could not restore your database from wordpress/.wp-labs-snapshot.sql: {out[-300:]}")
        self.snap = None


# ------------------------------------------------------------------------------------------------ host compose labs
class HostProject:
    """A throwaway, REAL copy of the learner's Lesson 1.2 project (downloads/pagesco-dev), for '# host: compose'
    files: started as Compose project wpc-k<NN>-env on free host ports, WordPress installed exactly as Lesson 1.2
    does, the Mailpit mu-plugin copied in. close() runs down -v and deletes the folder."""

    def __init__(self, tag: str, work: Path, ver: str = "8.5"):
        self.tag, self.ver = tag, ver
        self.dir = work / "pagesco-dev"
        self.name = f"wpc-{tag}-env"
        self.web_port, self.mail_port = free_port(), free_port()
        self.env = dict(os.environ, COMPOSE_PROJECT_NAME=self.name, PAGESCO_PORT=str(self.web_port),
                        PAGESCO_MAILPIT_PORT=str(self.mail_port))
        self.up = False

    def _dc(self, *args, timeout=600, check=True):
        r = subprocess.run(["docker", "compose", "--progress", "quiet", *args], cwd=self.dir, capture_output=True,
                           text=True, timeout=timeout, env=self.env, stdin=subprocess.DEVNULL)
        if check and r.returncode:
            raise RuntimeError(f"docker compose {' '.join(args)[:80]} failed: {(r.stdout + r.stderr)[-600:]}")
        return r.returncode, r.stdout + r.stderr

    def start(self) -> None:
        src = COURSE_DIR / "downloads" / "pagesco-dev"
        if not (src / "compose.yaml").is_file():
            raise RuntimeError(f"{src}/compose.yaml not found: the host labs use the course's starter project")
        shutil.copytree(src, self.dir)
        uid, gid = os.getuid(), os.getgid()
        (self.dir / ".env").write_text(f"PAGESCO_UID={uid}\nPAGESCO_GID={gid}\n")
        img = "wordpress:7.1-php8.4-apache" if self.ver == "8.4" else "wordpress:7.1-php8.5-apache"
        cli_base = "wordpress:cli-php8.4" if self.ver == "8.4" else "wordpress:cli-php8.5"
        # Lesson 1.2's Linux/WSL file (config/compose.linux.yaml) + the checker's own ports and image tag
        override = (self.dir / "config" / "compose.linux.yaml").read_text()
        override = override.replace("  wordpress:\n", f"  wordpress:\n    image: {img}\n    ports: !override\n"
                                    f"      - \"{self.web_port}:8080\"\n", 1)
        override = override.replace("  wpcli:\n", f"  wpcli:\n    image: wpc-{self.tag}-wpcli:{self.ver}\n    build:\n"
                                    f"      args:\n        BASE: {cli_base}\n", 1)
        override += f"  mailpit:\n    ports: !override\n      - \"{self.mail_port}:8025\"\n"
        (self.dir / "compose.override.yaml").write_text(override)
        (self.dir / "wordpress").mkdir()
        self.up = True
        self._dc("up", "-d", "--wait", timeout=900)
        for _ in range(240):                      # the image's entrypoint copies WordPress in on the first start
            if (self.dir / "wordpress" / "wp-config.php").is_file() and (self.dir / "wordpress" / "wp-settings.php").is_file():
                break
            time.sleep(0.5)
        time.sleep(1)
        run = ["run", "--rm", "-T", "wpcli", "wp"]
        self._dc(*run, "core", "install", "--url=http://localhost:8080", "--title=Pages & Co.", "--admin_user=admin",
                 "--admin_password=password", "--admin_email=wordpress@example.com", "--skip-email", timeout=600)
        self._dc(*run, "rewrite", "structure", "/%postname%/")
        mu = self.dir / "wordpress" / "wp-content" / "mu-plugins"
        mu.mkdir(exist_ok=True)
        shutil.copy(self.dir / "config" / "mailpit-smtp.php", mu / "mailpit-smtp.php")

    def normalize(self, out: str) -> str:
        return (out.replace(f"localhost:{self.web_port}", "localhost:8080").replace(f"localhost:{self.mail_port}", "localhost:8025")
                .replace(f"{self.name}-", "pagesco-"))

    def close(self) -> None:
        if self.up:
            self._dc("down", "-v", "--remove-orphans", timeout=300, check=False)
            self.up = False
        if self.dir.exists():
            r = subprocess.run(["rm", "-rf", str(self.dir)], capture_output=True)
            if r.returncode and self.dir.exists():
                subprocess.run(["docker", "run", "--rm", "-v", f"{self.dir.parent}:/p", "wordpress:cli-php8.5",
                                "sh", "-c", f"rm -rf /p/{self.dir.name}"], capture_output=True)


# ------------------------------------------------------------------------------------------------ one file
def static_problems(path: Path, text: str, kind: str, h: dict) -> tuple[list, list]:
    fails, warns = [], []
    if path.suffix == ".php" and kind != "support":
        code_only = re.sub(r"(?s)/\*.*?\*/", "", text)
        code_only = re.sub(r"(?m)(^|\s)(//|#(?!\[))[^\n]*$", "", code_only)
        for rx, why in FORBIDDEN_PHP:
            if rx.search(code_only):
                fails.append(f"not run: the file {why}")
    if path.suffix == ".sh" and PROMPT_RE.search(text):
        fails.append("not run: a line starts with '$ ' (learners would copy the prompt)")
    st = h.get("state", "fresh")
    if not re.fullmatch(r"fresh|after:lesson_\d\d", st):
        fails.append(f"'// state: {st}' must be fresh or after:lesson_NN")
    if kind in ("starter", "solution", "debug", "test") and "state" not in h and "host" not in h:
        warns.append("no '// state: fresh|after:lesson_NN' line in the header (treated as fresh)")
    if kind == "debug" and not h.get("expect-error"):
        fails.append("a debug handout needs '// expect-error: Warning, Deprecated ...' in its header")
    if kind not in ("debug", "test") and h.get("expect-error"):
        fails.append("'// expect-error' only belongs in debug_* files (or the test of a debug_ folder)")
    if kind in ("starter", "solution") and not h.get("expect"):
        warns.append("no '// expect:' line (what the file prints: a TODO line for a starter, the answer for a solution)")
    if kind == "starter" and "TODO" not in text:
        warns.append("starter has no TODO")
    if kind == "test":
        if not h.get("serve"):
            fails.append("a test_* file needs '// serve: <folder pair name>' in its header")
        inst = (h.get("install") or "").split()
        if not inst or inst[0] not in ("plugin", "mu-plugin", "theme"):
            fails.append("a test_* file needs '// install: mu-plugin | plugin [slug] | theme [slug]'")
    if h.get("host") and (h["host"] != "compose" or kind != "support" or path.suffix != ".sh"):
        fails.append("'# host: compose' is only for check_*.sh files")
    return fails, warns


def judge(kind: str, wanted_errors: str, diags, code: int, out: str, expects: list) -> tuple[bool, list]:
    problems = []
    ok = True
    if "[timed out after" in out:
        return False, ["timed out (waiting for input? an endless loop?)"]
    if wanted_errors:
        wanted = [w.strip() for w in wanted_errors.split(",") if w.strip()]
        if not diags:
            ok = False
            problems.append(f"expected {', '.join(wanted)}, but it ran without a message")
        else:
            bad = [d for d in diags if d[0] not in wanted and d[1] not in wanted]
            if bad:
                ok = False
                problems.append("undeclared message: " + bad[0][2][:160])
            missing = [w for w in wanted if not any(w in (d[0], d[1]) for d in diags)]
            if missing:
                ok = False
                problems.append(f"declared {', '.join(missing)} never happened")
    else:
        if diags:
            ok = False
            problems.append("said: " + diags[0][2][:180])
        elif code != 0:
            ok = False
            problems.append(f"exit status {code}")
    for e in expects:
        if e not in out:
            ok = False
            problems.append(f"expected text not printed: {e!r}")
    return ok, problems


def install_folder(backend: Backend, folder: Path, how: list[str], pair: str) -> tuple[list[Path], str]:
    """Copy a lab folder into wp-content; returns (installed paths, activation command or '')."""
    wpc = backend.root / "wp-content"
    kind = how[0]
    slug = how[1] if len(how) > 1 else pair.replace("_", "-")
    if kind == "mu-plugin":
        dest = wpc / "mu-plugins"
        dest.mkdir(parents=True, exist_ok=True)
        placed = []
        for p in sorted(folder.iterdir()):
            if p.name in ("tmp", "__pycache__", "README.md"):
                continue
            target = dest / p.name
            if target.exists():
                raise RuntimeError(f"wp-content/mu-plugins/{p.name} already exists on this site")
            (fresh_tree if p.is_dir() else fresh_copy)(p, target)
            placed.append(target)
        return placed, ""
    base = wpc / ("plugins" if kind == "plugin" else "themes")
    target = base / slug
    if target.exists():
        raise RuntimeError(f"wp-content/{base.name}/{slug} already exists on this site")
    fresh_tree(folder, target)
    return [target], (f"wp plugin activate {slug}" if kind == "plugin" else f"wp theme activate {slug}")


_last_stamp = [0.0]


def fresh_copy(src: Path, dst: Path) -> None:
    """Copy a file and give it a NEW modification time: OPcache (revalidate_freq 0) compares mtimes in whole
    seconds, so a solution copied over a starter written in the same second would otherwise run stale code."""
    shutil.copy(src, dst)
    t = max(time.time(), _last_stamp[0] + 1.0)
    _last_stamp[0] = t
    os.utime(dst, (t, t))


def fresh_tree(src: Path, dst: Path) -> None:
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("tmp", "__pycache__", "node_modules"), copy_function=fresh_copy)


def remove_paths(paths) -> None:
    for p in paths:
        if p.is_dir():
            shutil.rmtree(p, ignore_errors=True)
        elif p.exists() or p.is_symlink():
            p.unlink()


def run_command_for(path: Path, h: dict, name: str) -> str:
    args = h.get("args", "")
    if path.suffix == ".php":
        user = f" --user={_q(h['user'])}" if h.get("user") else ""
        return f"wp eval-file --use-include {_q(name)}{user}" + (f" {args}" if args else "")
    return f"sh {_q(name)}" + (f" {args}" if args else "")


def run_lab(path: Path, backend_for, args) -> list[tuple]:
    """[(ok, verdict, output)] for one lab file (a test gives one result per installed folder).
    backend_for(kind) returns the Backend (or HostProject) to use; ok is None for SKIP."""
    text = path.read_text(encoding="utf-8")
    kind = kind_of(path)
    h = header(text)
    fails, warns = static_problems(path, text, kind, h)
    if fails:
        return [(False, " · ".join(fails), "")]
    state = h.get("state", "fresh")
    timeout = getattr(args, "timeout", DEFAULT_TIMEOUT)

    if h.get("host") == "compose":
        if getattr(args, "no_host", False):
            return [(None, "SKIP: runs on the host in a Compose project (--no-host)", "")]
        hp = backend_for("host")
        t0 = time.perf_counter()
        if Path(hp.dir).resolve() in path.resolve().parents:      # your own project: run it where it is
            rel = path.resolve().relative_to(Path(hp.dir).resolve())
        else:
            copy = hp.dir / "labs" / path.resolve().relative_to(LABS).parent
            copy.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, copy / path.name)
            rel = (copy / path.name).relative_to(hp.dir)
        try:
            r = subprocess.run(["bash", str(rel)] + h.get("args", "").split(), cwd=hp.dir, capture_output=True,
                               text=True, timeout=max(timeout, 300), env=hp.env, stdin=subprocess.DEVNULL)
            code, out = r.returncode, r.stdout + r.stderr
        except subprocess.TimeoutExpired as e:
            code, out = 124, (e.stdout or "") + "\n[timed out]"
        out = hp.normalize(out)
        ok, problems = judge(kind, "", diagnostics(out, cli=False), code, out, h.get("expect", []))
        verdict = f"{time.perf_counter() - t0:5.1f}s [host: Compose project {hp.name}]" + (
            " · " + " · ".join(problems + ["WARN " + w for w in warns]) if problems or warns else "")
        return [(ok, verdict, out)]

    backend = backend_for("site")
    results = []

    def one(variant: str, install: Path | None, expects: list, wanted_errors: str):
        t0 = time.perf_counter()
        backend.prepare(state)
        placed: list[Path] = []
        problems: list[str] = []
        out_parts = []
        code = 0
        try:
            before = snapshot(backend.root)
            size = backend.log_size()
            if install is not None:
                how = (h.get("install") or "").split()
                pair = re.sub(r"_(starter|solution)$", "", install.name)
                placed, act = install_folder(backend, install, how, pair)
                if act:
                    c, o = backend.run(act, timeout)
                    out_parts.append(o)
                    if c:
                        code = c
            target = backend.root / path.name
            fresh_copy(path, target)
            placed.append(target)
            c, o = backend.run(run_command_for(path, h, path.name), timeout)
            out_parts.append(o)
            code = code or c
            log = backend.log_since(size)
            out = backend.normalize("".join(out_parts))
            diags = diagnostics(out)
            seen = {diag_key(d) for d in diags}
            from_log = [d for d in diagnostics(log, cli=False) if diag_key(d) not in seen]
            for d in from_log:
                diags.append((d[0], d[1], "(debug.log) " + d[2]))
                seen.add(diag_key(d))
            if from_log:      # a message that only reached the log (a page request, a cron job): show the log
                out = out.rstrip("\n") + "\n[new lines in wp-content/debug.log]\n" + backend.normalize(log).rstrip("\n") + "\n"
            ok, problems = judge(kind, wanted_errors, diags, code, out, expects)
            remove_paths(placed)
            after = snapshot(backend.root)
            placed_rel = {str(p.relative_to(backend.root)) for p in placed}
            changed = sorted(k for k in after if before.get(k) != after[k]
                             and k != "wp-content/debug.log" and not any(k == pr or k.startswith(pr + "/") for pr in placed_rel))
            if changed:
                ok = False
                problems.append("left files behind (labs run on the learner's course site): " + ", ".join(changed[:5]))
        finally:
            remove_paths(placed)
            backend.cleanup_after()
        label = f" [{variant}]" if variant else ""
        verdict = f"{time.perf_counter() - t0:5.1f}s [{state}]{label}" + (
            " · " + " · ".join(problems + ["WARN " + w for w in warns]) if problems or warns else "")
        results.append((ok, verdict, out))

    if kind == "test":
        name = h["serve"].strip().rstrip("/")
        folders = [path.parent / name] if (path.parent / name).is_dir() else [path.parent / f"{name}_starter", path.parent / f"{name}_solution"]
        folders = [f for f in folders if f.is_dir()]
        if not folders:
            return [(False, f"// serve: {name}: no folder {name}/ or {name}_starter/ + {name}_solution/ next to the test", "")]
        for folder in folders:
            which = "starter" if folder.name.endswith("_starter") else ("solution" if folder.name.endswith("_solution") else "")
            exp = h.get(f"expect-{which}", []) if which else h.get("expect", [])
            if which and not exp:
                warns.append(f"no '// expect-{which}:' line")
            one(folder.name + "/", folder, exp, h.get("expect-error", ""))
        return results
    one("", None, h.get("expect", []), h.get("expect-error", "") if kind == "debug" else "")
    return results


def lint_file(path: Path, compose: Path | None = None) -> tuple[bool, str, str]:
    """php -l in the course's PHP 8.5 WP-CLI image (your pagesco-wpcli:php8.5 with WP_LABS_COMPOSE)."""
    img = "pagesco-wpcli:php8.5" if compose else "wordpress:cli-php8.5"
    name = f"wpc-{session_tag(path)}-lint-{os.getpid() % 100000}"
    r = subprocess.run(["docker", "run", "--rm", "--name", name, "--entrypoint", "php", "-v", f"{path.parent}:/lab:ro",
                        img, "-l", f"/lab/{path.name}"], capture_output=True, text=True)
    out = r.stdout + r.stderr
    ok = r.returncode == 0 and "No syntax errors" in out
    return ok, "php -l (PHP 8.5)" + ("" if ok else " · " + (out.strip().splitlines() or ["?"])[0][:160]), out


# ------------------------------------------------------------------------------------------------ driver
def lab_files(mod: Path):
    run, lint = [], []
    for p in sorted(mod.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(mod)
        if any(part in IGNORE_DIRS for part in rel.parts):
            continue
        k = kind_of(p)
        lesson_level = len(rel.parts) == 2          # module-NN/<lesson>/<file>
        if k in ("starter", "solution", "debug", "test", "support") and lesson_level:
            run.append(p)
        elif p.suffix == ".php":
            lint.append(p)
    return run, lint


def pairs_problems(mod: Path, files):
    have = set(files)
    out = []
    for f in files:
        for a, b in (("_starter", "_solution"), ("_solution", "_starter")):
            if f.stem.endswith(a) and f.with_name(f.stem[: -len(a)] + b + f.suffix) not in have:
                out.append(f"{f.relative_to(mod)} has no partner {f.stem[: -len(a)] + b}{f.suffix}")
    for d in sorted(p for p in mod.glob("*/*") if p.is_dir()):
        for a, b in (("_starter", "_solution"), ("_solution", "_starter")):
            if d.name.endswith(a) and not d.with_name(d.name[: -len(a)] + b).is_dir():
                out.append(f"{d.relative_to(mod)}/ has no partner folder {d.name[: -len(a)] + b}/")
    return out


def runner_available() -> bool:
    return (COURSE_TOOLS / "wpkit.py").is_file() and shutil.which("docker") is not None


class Backends:
    """Lazily creates one site backend (and one host project) per session tag; closes them all."""

    def __init__(self, ver: str):
        self.ver = ver
        self.sites: dict = {}
        self.hosts: dict = {}
        self.work = Path(tempfile.mkdtemp(prefix="kitlabs_"))
        compose = os.environ.get("WP_LABS_COMPOSE")
        self.compose = Path(compose).expanduser().resolve() if compose else None
        if not self.compose and not runner_available():
            raise SystemExit("No way to run WordPress labs: set WP_LABS_COMPOSE to your Lesson 1.2 project folder "
                             "(for example ~/pagesco-dev, with docker compose up -d running).")

    def describe(self) -> str:
        if self.compose:
            return f"your Compose project {self.compose} (docker compose run --rm wpcli; database saved and restored per lab)"
        return f"the course runner (wpkit.py: WordPress 7.1.3, PHP {self.ver}, MySQL 9.7, WP-CLI 2.12, a fresh site per lab)"

    def for_file(self, path: Path):
        tag = session_tag(path)

        def get(kind):
            if kind == "host":
                if self.compose:
                    hp = Namespace(dir=self.compose, env=dict(os.environ), name=self.compose.name, normalize=lambda s: s)
                    return hp
                if tag not in self.hosts:
                    sys.path.insert(0, str(COURSE_TOOLS))
                    import wpkit  # noqa: E402
                    lock = wpkit.file_lock(f"kit-{tag}-env")
                    lock.__enter__()
                    hp = HostProject(tag, self.work, self.ver)
                    hp._lock = lock
                    self.hosts[tag] = hp
                    hp.start()
                return self.hosts[tag]
            if self.compose:
                if "compose" not in self.sites:
                    self.sites["compose"] = ComposeSite(self.compose)
                return self.sites["compose"]
            if tag not in self.sites:
                self.sites[tag] = RunnerSite(tag, self.ver)
            return self.sites[tag]
        return get

    def close(self) -> None:
        for b in self.sites.values():
            try:
                b.close()
            except Exception as e:                       # noqa: BLE001
                print(f"note: closing {b.name}: {e}")
        for hp in self.hosts.values():
            try:
                hp.close()
            finally:
                hp._lock.__exit__(None, None, None)
        shutil.rmtree(self.work, ignore_errors=True)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Run every WordPress lab of the kit and report PASS/FAIL.")
    ap.add_argument("sessions", nargs="*", help="module-03, 03 or 3 (default: all)")
    ap.add_argument("--file", action="append", default=[], help="check one file (repeatable)")
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--no-host", action="store_true", help="skip '# host: compose' files")
    args = ap.parse_args(argv)

    mods = sorted(p for p in LABS.glob("module-*") if p.is_dir())
    if args.sessions:
        want = []
        for s in args.sessions:
            m = re.fullmatch(r"(?:module-)?(\d{1,2})", s)
            if not m:
                raise SystemExit(f"Not a session: {s!r} (use module-03, 03 or 3)")
            want.append(LABS / f"module-{int(m.group(1)):02d}")
        mods = want
    failures, runs, lints = 0, [], []
    for f in args.file:
        p = Path(f).expanduser().resolve()
        if not p.is_file():
            raise SystemExit(f"no such file: {f}")
        (runs if kind_of(p) not in ("include", "other") else lints).append(p)
    if not args.file:
        for mod in mods:
            if not mod.is_dir():
                print(f"FAIL {mod.name}: folder does not exist")
                failures += 1
                continue
            r, li = lab_files(mod)
            if not r:
                msg = f"{mod.name}: no lab files"
                if args.sessions or args.strict:
                    print("FAIL " + msg)
                    failures += 1
                else:
                    print("skip " + msg)
            if not (mod / "README.md").is_file():
                print(f"FAIL {mod.name}: README.md is missing")
                failures += 1
            for msg in pairs_problems(mod, r):
                print(f"FAIL {mod.name}: {msg}")
                failures += 1
            runs += r
            lints += li
    if not runs and not lints:
        print(f"\n0 files checked · {failures} failure(s)")
        return 1 if failures else 0

    ver = os.environ.get("WP_LABS_PHP", "8.5")
    backends = Backends(ver)
    passed = skipped = 0
    print(f"Labs run on {backends.describe()}")
    try:
        for p in runs:
            rel = p.relative_to(KIT) if KIT in p.parents else p
            try:
                res = run_lab(p, backends.for_file(p), args)
            except (RuntimeError, SystemExit, OSError) as e:
                res = [(False, f"could not run: {e}", "")]
            for ok, verdict, out in res:
                word = "SKIP" if ok is None else ("PASS" if ok else "FAIL")
                print(f"{word} {rel}  {verdict}", flush=True)
                if args.verbose or (ok is False and out):
                    lines = out.rstrip("\n").splitlines()
                    for ln in (lines[-80:] if args.verbose else lines[-30:]):
                        print("      " + ln)
                if ok is None:
                    skipped += 1
                elif ok:
                    passed += 1
                else:
                    failures += 1
        for p in lints:
            rel = p.relative_to(KIT) if KIT in p.parents else p
            ok, verdict, out = lint_file(p, backends.compose)
            print(f"{'PASS' if ok else 'FAIL'} {rel}  {verdict}")
            passed += ok
            failures += not ok
    finally:
        backends.close()
    print(f"\n{passed} passed, {failures} failed" + (f", {skipped} skipped" if skipped else ""))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
