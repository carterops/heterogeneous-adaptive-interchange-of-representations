# Project instructions

This repository provides inspectable representation contracts for human-intent
interpretation and specialist communication. The current public package is v0.2.0.
The broader intent-driven Factory runtime lives outside this repository.

- Keep native specialist artifacts and recipient renderings distinct.
- H-A-I-R carries an authority reference but never grants or expands authority.
- Acknowledgement records the recipient's actual reading; it is not proof of truth.
- Separate hypothesis, experiment, observation, and measured result.
- Never confuse a software test pass with semantic alignment or product quality.
- Preserve regression cases for discovered interpretation and protocol failures.
- Keep historical v0.1.1 evaluation fixtures intact and labeled as authored cases.
- Mark scripted behavior explicitly; never present it as general understanding.
- Treat confidence and RTSF as uncalibrated unless human evidence supports them.
- Keep public artifacts free of private user history, secrets, and machine paths.
- Add dependencies or orchestration only for a demonstrated capability gap. Prefer a
  small portable contract that an owning runtime can adopt.
- Update the README, protocol documentation, and examples when the wire format changes.
- Before delivery run `python -m unittest discover -s tests -v`,
  `python -m hairbridge`, `python -m hairbridge.eval`, and both examples.
