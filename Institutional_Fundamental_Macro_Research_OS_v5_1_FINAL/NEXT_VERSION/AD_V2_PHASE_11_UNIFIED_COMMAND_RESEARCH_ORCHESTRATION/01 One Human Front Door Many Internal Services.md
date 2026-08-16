# One front door

The user should not need to know R2 prompt IDs, P02/P03/P04/P05 phase names, P08 scheduler internals or P09 learning commands.

Human commands are unified under `AlphaDesk.ps1`. Internal services stay modular and separately auditable. A single launcher is not a monolithic runtime.