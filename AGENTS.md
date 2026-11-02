# AGENTS.md

Guidance for AI agents working in this repository.

## What this repository is

This is the **IFSC/DistintiveLab Brazilian fork** of the Helios end-to-end verifiable
voting system (`origin` = DistintiveLab/helios-server, `upstream` = benadida/helios-server).
Python 3.13, Django 5.2, Celery, uv as package manager.

Fork-specific customizations that MUST be preserved when merging upstream:

- pt-BR UI (`locale/pt_BR/`), Bootstrap-based templates
- `heliosinstitution` app (institution admin delegation) and `helioslog` app — both in
  `INSTALLED_APPS` alongside upstream's `helios`, `helios_auth`, `server_ui`
- HTML-only emails with hardcoded pt-BR bodies (see "Email pipeline" below)
- `voters_list.html` gates the "Who can vote?" eligibility text behind `openreg`;
  when `openreg=False` it shows "Only the voters listed here" instead of upstream's
  unconditional `pretty_eligibility` rendering
- `castvote.html` deliberately omits upstream's hidden `<textarea>` raw-ballot dump

`CLAUDE.md` also exists (came from upstream). Trust this file over CLAUDE.md for
fork-specific facts: CLAUDE.md says the broker is RabbitMQ, but this fork defaults to
`redis://127.0.0.1:6379` (settings.py), and CLAUDE.md assumes bare `uv` on PATH.

## Commands

`uv` lives at `~/.local/bin/uv` — always use the full path; bare `uv` is not on PATH.

```bash
# Install dependencies
~/.local/bin/uv sync

# Run the full test suite (sqlite settings, see below). ~3s, 289 tests.
# CRITICAL: the unittest summary ("Ran N tests ... OK") goes to STDERR, not stdout.
DJANGO_SETTINGS_MODULE=settings_sqlite ~/.local/bin/uv run python manage.py test \
  > /tmp/test-out.txt 2>/tmp/test-err.txt
# failures are FAIL:/ERROR: lines in /tmp/test-err.txt

# Single app / class / method
DJANGO_SETTINGS_MODULE=settings_sqlite ~/.local/bin/uv run python manage.py test helios.tests.ElectionBlackboxTests
DJANGO_SETTINGS_MODULE=settings_sqlite ~/.local/bin/uv run python manage.py test helios.test_csrf_smoke

# Sanity checks / migrations
DJANGO_SETTINGS_MODULE=settings_sqlite ~/.local/bin/uv run python manage.py check
DJANGO_SETTINGS_MODULE=settings_sqlite ~/.local/bin/uv run python manage.py migrate

# Translations (regenerate .po, then compile; .mo is gitignored, only .po is tracked)
DJANGO_SETTINGS_MODULE=settings_sqlite ~/.local/bin/uv run python manage.py makemessages -l pt_BR
DJANGO_SETTINGS_MODULE=settings_sqlite ~/.local/bin/uv run python manage.py compilemessages -l pt_BR

# Dev server / celery worker (need real Postgres + Redis per settings.py)
~/.local/bin/uv run python manage.py runserver
~/.local/bin/uv run celery --app helios worker --events --beat --concurrency 1
```

There is no separate lint/typecheck config; `manage.py check` is the closest thing.

`python-ldap` builds from source. If the uv cache is lost and the build fails on
missing sasl headers, rebuild with:
`CPATH=/tmp/sasl-dev/usr/include LIBRARY_PATH=/tmp/sasl-dev/usr/lib/x86_64-linux-gnu ~/.local/bin/uv sync`
(with the cache warm, plain `uv sync` works).

## The sqlite test settings file (deliberately uncommitted)

`settings.py` **forces** the PostgreSQL engine (settings.py:58-74), and no local
Postgres server exists. All local testing therefore runs through
`DJANGO_SETTINGS_MODULE=settings_sqlite`. That file is **gitignored on purpose** — it
is local-only and contains:

- sqlite `DATABASES` at `/tmp/helios-dev.db`
- `HELIOS_ADMIN_ONLY = False` (fork prod restricts election creation to institution
  admins; upstream test fixtures assume plain users can create elections)
- `LANGUAGE_CODE = 'en-us'` (the inherited test suite asserts on English UI strings;
  without this the pt-BR catalog translates them and tests fail)
- `FEATURE_ELECTION = True`
- `CELERY_TASK_EAGER_PROPAGATES = True` — essential: without it, exceptions inside
  eagerly-executed celery tasks are silently swallowed and broken code passes tests.

If it's missing, recreate it from this list; do not commit it.

## Gotchas

- **Test output goes to stderr** (see command above). Reading only stdout looks like
  the suite produced nothing.
- **Celery eager mode still needs the `redis` package.** settings.py sets
  `CELERY_TASK_ALWAYS_EAGER = True` when `'test' in sys.argv` (a deliberate hack at
  settings.py:11), but celery 5's eager path still resolves the broker transport,
  and kombu's redis transport imports `redis` at module load. `redis>=5.0.0` is in
  pyproject.toml for this reason — without it every `apply_async` crashes even with
  no broker running.
- **`lock_row` (helios/utils.py) must stay sqlite-aware.** It appends raw
  `FOR UPDATE` only when `connection.vendor != 'sqlite'` (sqlite locks the whole
  database on write and rejects the syntax). Upstream's version is unconditional
  because its CI runs Postgres — do not "simplify" this back.
- **`MergeDuplicateUsersTests` is skipped on sqlite** (`@unittest.skipIf`) because its
  setUp drops a case-insensitive unique constraint via a schema editor, which sqlite
  cannot do.
- **Emails are HTML-only**: `send_mail(subject, '', ..., html_message=body)` with an
  empty plaintext body — see tests like `test_plaintext_email_is_not_html_escaped`
  asserting `message.body == ''` and content in `alternatives[0][0]`.
- **Fixture election has `openreg=False`** (`helios/fixtures/election.json`), which
  drives the voters-page wording assertions.
- **`.mo` files are gitignored** (`*.mo`); after `compilemessages` only the `.po` is
  committed. Obsolete `#~` entries with `#, fuzzy` in the .po are dead entries —
  `msgfmt` confirms no active fuzzy.
- Tooling note: after editing a file outside the editor tool (e.g. sed), re-read it
  before using exact-match edits.

## Email pipeline (fork divergence from upstream)

- Templates live in `helios/templates/email/*.txt` but are **full HTML documents**,
  hardcoded pt-BR, despite the `.txt` names. They are sent via
  `send_mail(..., html_message=body)` (`helios_auth/auth_systems/password.py:133`
  is the canonical example: empty plaintext body).
- Rendering helpers in `helios/view_utils.py`:
  - `render_template` — full page render (views)
  - `render_template_raw` — engine defaults, **autoescape ON**; used for fork HTML
    email bodies (`helios/tasks.py` `single_voter_email`, `single_voter_notify`).
    Upstream's `render_text_template` (autoescape OFF) on these bodies is a
    **security regression** (voter-controlled values → HTML injection); this was
    introduced by a merge once — keep `render_template_raw` for bodies.
  - `render_text_template` — Context with autoescape=False; correct for **subjects**
    only (subjects must be raw text).

## Architecture notes

- Apps: `helios` (core election system: models, views, crypto, forms),
  `helios_auth` (multi-backend auth: google, github, LDAP, CAS, password, ...),
  `server_ui` (public/admin web UI), `heliosbooth` + `heliosverifier` (JS voting
  booth / ballot verifier), plus fork apps `heliosinstitution`, `helioslog`,
  `anymail`, `django_celery_results`, `django_celery_beat`.
- Celery app: `helios/celery_app.py`, `config_from_object('django.conf:settings',
  namespace='CELERY')`. Broker default `redis://127.0.0.1:6379`.
- Election admin authorization: `helios/security.py` — `@election_view(frozen=...)`,
  `@election_admin()` decorators; `user_can_admin_election(user, election)` =
  `user.admin_p or election.admin == user or election.admins.filter(...)`.
  Mismatches raise `PermissionDenied` (403). POST handlers call
  `check_csrf(request)`; failure → `SuspiciousOperation` → 400.
- VoterFile processing (`helios/models.py`): `add_voters_file` decodes BOM_UTF16 /
  utf-8-sig / latin-1 and strips NULs; `itervoters` streams the file;
  `lock_row` serializes processing.
- Settings pattern: `get_from_env('VAR', default)` (settings.py). Key vars:
  `DEBUG`, `SECRET_KEY`, `DATABASE_URL`, `CELERY_BROKER_URL`,
  `AUTH_ENABLED_AUTH_SYSTEMS`.

## Testing approach

- Django `TestCase` + django-webtest; fixtures in `helios/fixtures/`;
  `ElectionBlackboxTests` is the big end-to-end suite (setUp: `self.user` =
  ben@adida.net/google, `self.adminUser` = mccio@github.com).
- **When upstream tests conflict with fork product behavior, adapt the tests**, not
  the product. Established adaptations: logout marker, HTML-only email assertions,
  voters-page wording (`"Only the voters listed here"` for openreg=False), no
  raw-ballot dump on the cast-vote page.
- Complete-election tests (`test_do_complete_election*`) must create the election as
  the default ben@adida.net user (no `admin=True` in `_setup_complete_election`),
  because `_do_tally` logs in as ben and must pass `user_can_admin_election`.
- Expected baseline after the Django 5.2 / Python 3.13 upstream merge:
  `Ran 289 tests — OK (skipped=18)`.

## Merging upstream

Strategy proven in the Django 5.2 merge (see `git log 1e4d1c3`, `b5758b6`):

1. Take upstream security/CSRF/functional fixes; keep fork pt-BR/Bootstrap/IFSC
   customizations and the divergences listed at the top of this file.
2. After the merge, run the full suite and diagnose: merge artifacts (half-merged
   code), fork-vs-upstream test expectation drift, and environment issues
   (sqlite-isms, celery eager) are the three usual failure classes.
3. Environment-aware guards in code get a brief "why" comment; test-environment
   constraints belong in `settings_sqlite.py`, not the committed tree.
4. Useful refs: compare against `git show upstream/master:<file>` and the pre-merge
   fork tip `git show d420d7e:<file>`.

## Code style (from CLAUDE.md, verified)

- 2-space indentation in Python
- Booleans: `_p` suffix (`private_p`, `frozen_p`, `admin_p`); datetimes: `_at` suffix
- Domain models inherit `HeliosModel` with `class Meta: app_label = 'helios'`
- Views: `render_template(request, name, vars)` / `render_json({...})` from
  `helios.views`; `@transaction.atomic`, `select_related()`, `get_or_create()`
- Sanitize user HTML with `nh3.clean()` (see `description_bleached`); never store
  plaintext passwords
