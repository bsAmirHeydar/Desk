# C1 Environment Constitution

Installation and environment certification are separate states.

`INSTALLED` means the production host, source-domain policy, launchers and certification tools exist and the offline R4 suite still passes.

`ENVIRONMENT_CERTIFIED` additionally requires a live OpenAI API attestation on the target machine: the selected GPT-5.6 Sol model is callable, pro/reasoning settings are accepted, Responses API returns a valid model receipt, web search works under an allowed-domain filter, the data root is writable, and no secret is stored in the Vault.

Missing licensed/private feeds are not converted into public data. They remain explicit source gaps and do not automatically fail the host environment attestation; their materiality is adjudicated per run by the scientific pipeline.
