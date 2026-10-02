#!/usr/bin/env python3
"""
Moteur d'évaluation déterministe pour agents IA (Agent Evals Runner).
Valide des scénarios d'ingénierie logicielle contre des règles de conformité et des vérifications automatisées.
Usage:
    python3 scripts/run-evals.py [--verbose]
"""

import os
import sys
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)

class EvalScenario:
    def __init__(self, scenario_id: str, title: str, category: str):
        self.scenario_id = scenario_id
        self.title = title
        self.category = category
        self.checks = []

    def add_check(self, description: str, check_fn):
        self.checks.append((description, check_fn))

    def run(self, verbose: bool = False) -> bool:
        print(f"\n[SCENARIO {self.scenario_id}] {self.title} ({self.category})")
        passed = True
        for desc, fn in self.checks:
            try:
                ok, err = fn()
                if ok:
                    print(f"  [PASS] {desc}")
                else:
                    print(f"  [FAIL] {desc} -> {err}")
                    passed = False
            except Exception as e:
                print(f"  [ERROR] {desc} -> Exception: {e}")
                passed = False
        return passed

# Fonctions de Vérification Déterministe

def check_anti_slop():
    cmd = [sys.executable, os.path.join(ROOT_DIR, "scripts", "audit-slop.py"), "core/RULES.md", "README.md", "DESIGN.md"]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.returncode == 0, res.stdout + res.stderr

def check_fintech_money():
    path = os.path.join(ROOT_DIR, "stacks", "fintech.md")
    with open(path, "r", encoding="utf-8") as f:
        c = f.read().lower()
    return "unités mineures" in c and "float" in c, "Règles sur les unités mineures absentes"

def check_fintech_ledger():
    path = os.path.join(ROOT_DIR, "stacks", "fintech.md")
    with open(path, "r", encoding="utf-8") as f:
        c = f.read().lower()
    return "double-entry ledger" in c and "immuabilité" in c, "Principes du grand livre à double entrée absents"

def check_fintech_idempotence():
    path = os.path.join(ROOT_DIR, "stacks", "fintech.md")
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    return "Idempotency-Key" in c, "Clé d'idempotence absente"

def check_fintech_hmac():
    path = os.path.join(ROOT_DIR, "stacks", "fintech.md")
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    return "timingSafeEqual" in c and "HMAC" in c, "Vérification HMAC en temps constant absente"

def check_semgrep_sqli():
    path = os.path.join(ROOT_DIR, ".semgrep.yml")
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    return "forbid-raw-sql-concatenation" in c, "Règle Semgrep d'injection SQL absente"

def check_semgrep_jwt():
    path = os.path.join(ROOT_DIR, ".semgrep.yml")
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    return "forbid-hardcoded-jwt-secrets" in c, "Règle Semgrep de secrets JWT absente"

def check_security_handbook_owasp():
    path = os.path.join(ROOT_DIR, "guides", "security-handbook.md")
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    return "BOLA" in c and "SSRF" in c and "IDOR" in c, "Principes BOLA, SSRF et IDOR absents"

def check_phase0_onboarding():
    path = os.path.join(ROOT_DIR, "guides", "onboard-codebase.md")
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    return "CODEMAP.md" in c and "tests de caractérisation" in c.lower(), "Protocole d'onboarding incomplet"

def check_test_lifecycle():
    path = os.path.join(ROOT_DIR, "guides", "testing-strategy.md")
    with open(path, "r", encoding="utf-8") as f:
        c = f.read().lower()
    return "quand en ajouter" in c and "quand en supprimer" in c, "Directives de cycle de vie des tests absentes"

def check_adapters_sync():
    cmd = [sys.executable, os.path.join(ROOT_DIR, "scripts", "build-adapters.py"), "--check"]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.returncode == 0, res.stdout + res.stderr

def build_eval_suite():
    suite = []

    # 1. Sécurité Applicative OWASP
    s1 = EvalScenario("SEC-01", "Défenses Statiques et Prévention OWASP", "Sécurité")
    s1.add_check("Détection statique des concaténations SQL vulnérables", check_semgrep_sqli)
    s1.add_check("Interdiction des secrets JWT codés en dur", check_semgrep_jwt)
    s1.add_check("Couverture documentaire BOLA, IDOR et SSRF", check_security_handbook_owasp)
    suite.append(s1)

    # 2. Rigueur Fintech & Transactions
    s2 = EvalScenario("FIN-01", "Intégrité Financière & Mobile Money", "Fintech")
    s2.add_check("Interdiction des floats et manipulation en unités mineures", check_fintech_money)
    s2.add_check("Architecture de grand livre immuable à double entrée", check_fintech_ledger)
    s2.add_check("Garantie d'idempotence sur les endpoints critiques", check_fintech_idempotence)
    s2.add_check("Validation HMAC en temps constant sur les webhooks", check_fintech_hmac)
    suite.append(s2)

    # 3. Posture d'Ingénierie & Méthode
    s3 = EvalScenario("ENG-01", "Cycle de Vie des Tests & Onboarding", "Méthode")
    s3.add_check("Protocole d'Onboarding Phase 0 (CODEMAP, caractérisation)", check_phase0_onboarding)
    s3.add_check("Gouvernance d'arbitrage des tests (ajout et suppression)", check_test_lifecycle)
    suite.append(s3)

    # 4. Architecture & Parité des Adapters
    s4 = EvalScenario("ARC-01", "Cohérence et Pureté du Core", "Architecture")
    s4.add_check("Parité déterministe des adapters IA avec core/RULES.md", check_adapters_sync)
    s4.add_check("Pureté stylistique et absence de remplissage (anti-slop)", check_anti_slop)
    suite.append(s4)

    return suite

def main():
    verbose = "--verbose" in sys.argv
    suite = build_eval_suite()

    total_scenarios = len(suite)
    passed_scenarios = 0

    print("=====================================================")
    print("      Lancement du Banc d'Évaluation des Agents      ")
    print("=====================================================")

    for scenario in suite:
        if scenario.run(verbose=verbose):
            passed_scenarios += 1

    print("\n-----------------------------------------------------")
    print(f"Résultats finaux : {passed_scenarios}/{total_scenarios} scénarios validés avec succès.")

    if passed_scenarios == total_scenarios:
        print("Verdict Global : SUCCÈS - L'Agent OS respecte l'ensemble des standards.")
        sys.exit(0)
    else:
        print("Verdict Global : ÉCHEC - Des régressions ont été constatées.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
