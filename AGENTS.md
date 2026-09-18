# Project instructions

This repository explores whether a Shared Bridge Representation (SBR) makes
interpretation assumptions visible and testable. Keep v0.1 limited to that question.

- Require evidence before claims. Separate hypothesis → experiment → result.
- Never confuse technical completion with semantic alignment.
- Preserve regression cases for previously discovered interpretation failures.
- Avoid unnecessary architecture, agents, orchestration, and heavy dependencies.
- Prefer falsifiable experiments; record what would disprove each interpretation.
- Update documentation and examples when terminology changes.
- Separate human-intent inference from product execution. An inference grants no authority to act.
- Current evidence overrides prior assumptions. Preserve ambiguity when context is missing.
- Mark fixture behavior explicitly; never present scripted output as semantic understanding.
- Treat confidence as uncalibrated unless calibration evidence exists.
- RTSF is an experimental human rating, not an established scientific metric.
- Keep public artifacts free of private user history, secrets, and machine-specific paths.
- Run `python -m unittest discover -s tests -v` and `python -m hairbridge` before delivery.
