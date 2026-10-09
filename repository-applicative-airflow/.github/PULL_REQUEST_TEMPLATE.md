# Title

## Motivations
<!-- Briefly describe the purpose of this DAG or why the changes were made -->

---

### ✅ Checklist

#### DAG Integrity & Syntax
- [ ] **No Import Errors:** Ran `python <dag_file>.py` locally without errors.
- [ ] **Unique DAG ID:** Ensured `dag_id` follows team naming conventions and is unique.
- [ ] **Static Analysis:** Code passes linting/formatting (`flake8`, `black`, `ruff`, etc.).

#### Execution & Testing
- [ ] **Tested Locally / Staging:** Successfully triggered and ran a backfill/test run in Airflow.
- [ ] **Task Dependencies:** Visually verified the task dependency graph in the Airflow UI.
- [ ] **Idempotency:** Confirmed re-running execution dates won't produce duplicate or corrupted data.

#### Configuration & Security
- [ ] **No Hardcoded Credentials:** Connections, API keys, and sensitive vars use Airflow Connections, Variables, or a Secret Manager.
- [ ] **Alerts & Owners:** `default_args` contains valid `owner`, `email_on_failure`, or SLA notifications.

#### Documentation
- [ ] **DAG Docstrings:** Added or updated `doc_md` or module docstrings for the DAG and complex tasks.
- [ ] **Rules:** Added or documented any business rules or technical expectations implemented.
