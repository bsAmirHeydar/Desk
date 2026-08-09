# Model Profiles and Executor Protocol

R2 is model-provider agnostic. It emits typed Prompt Jobs containing the prompt hash, model capability profile, input artifact references and canonical context paths. The host executes the job and returns a typed Process Output Envelope.

This design allows future model changes to be measured without rewriting the scientific Vault or Run Contract.
