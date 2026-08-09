# Cross-Platform, Timezone, Unicode and Windows Certification

R4 permanently carries forward the deployment lessons from R1:
- PowerShell wrappers are ASCII-only and thin;
- no compile-to-temp `.pyc` verification;
- no external `tzdata` dependency for bundled market zones;
- SQLite connections close explicitly;
- Git path staging uses Python/raw UTF-8-safe handling;
- text baseline hashes normalize UTF-8 BOM and CRLF/LF;
- Unicode filenames are not renamed by deployment unless the patch explicitly owns that rename;
- timezone-aware UTC is canonical; ambiguous/nonexistent local times fail closed.
