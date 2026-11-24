# Test coverage
`pytest -q tests` exercises YAML structural checks, port collisions, peer IP assignment, six-node rendering, and deterministic output. It is not equivalent to an EOS integration test. Run `ansible-playbook --syntax-check` and a Containerlab test pipeline before approving production use.
