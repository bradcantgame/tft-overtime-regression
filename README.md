# TFT combat simulator · Overtime regression

I built a Python combat simulator to test decisions I was making in Teamfight Tactics. While adding overtime, I needed to check what happened when a spell resolved on the same tick that the healing and shielding penalty began. I implemented the reduction at effect resolution and added a regression test to check that both effects use the stack active on that tick.

This standalone example recreates that case with one synthetic cast and an integer clock. The cast requests 5 HP of healing and a 100-point shield. The fixture gives the target enough missing health for the full heal, so a smaller heal comes from overtime.

| Cast resolves at | Overtime stacks | Healing applied | Shield granted |
| --- | ---: | ---: | ---: |
| 1,499,999 µs | 0 | 5 | 100 |
| 1,500,000 µs | 1 | 4.5 | 90 |
| 1,500,001 µs | 1 | 4.5 | 90 |

The test passes each resolution timestamp directly to `resolve_cast` to check when the penalty starts. The 1.5-second onset is a setting for this synthetic fixture. A full combat-engine test would start the cast before overtime and let it resolve on the onset tick. That would catch a bug where the engine uses the stack from the start of the cast.

## Run the regression

From this directory, run the following with Python 3.13. The example uses only the standard library.

```sh
python -m unittest -v
```

Expect one passing test with three timestamp checks. If the first stack starts one tick late, the middle case fails because the heal and shield come through at full strength. If it starts early, the first case fails. The GitHub Actions workflow runs the same command on pushes and pull requests.

Run `python overtime.py` to print the requested and applied amounts as a three-line JSON trace.
