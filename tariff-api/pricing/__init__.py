"""Server-side port of the tariff pricing engine previously implemented only
in customer.html JavaScript (see SECURITY_REMEDIATION_PLAN_customer_data_exposure.md).

Every module here is a direct, numerically-faithful port of its JS
counterpart, with all global/DOM-state coupling replaced by explicit
parameters. Do not change the math without re-running the diff-testing
harness in scripts/diff_test_pricing.py against the still-present JS in
customer.html.
"""
