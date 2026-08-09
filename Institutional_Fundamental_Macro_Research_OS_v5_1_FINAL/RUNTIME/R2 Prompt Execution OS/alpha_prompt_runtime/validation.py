import json
from pathlib import Path

class ValidationError(RuntimeError): pass

def validate_json_schema(vault_root,schema_ref,payload):
    try:
        import jsonschema
    except Exception as e:
        raise ValidationError('jsonschema package required for R2 strict output validation') from e
    sp=Path(vault_root)/schema_ref
    schema=json.loads(sp.read_text(encoding='utf-8'))
    try:
        # legacy resolver is intentionally used for relative file refs and remains portable here
        resolver=jsonschema.RefResolver(base_uri=sp.parent.resolve().as_uri()+'/',referrer=schema)
        jsonschema.Draft202012Validator(schema,resolver=resolver).validate(payload)
    except Exception as e:
        raise ValidationError(f'schema validation failed for {schema_ref}: {e}') from e
    return True
