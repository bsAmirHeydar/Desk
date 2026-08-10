# Source and Retrieval Commissioning

C1 maps every V21.3 D2 source contract to an explicit production access mode and domain allow-list.

Public web-accessible contracts may be retrieved by the OpenAI web-search tool with domain filtering and full source-list receipts. Subscription/licensed contracts are `UNBOUND` unless an explicit external connector is commissioned; they are never simulated by public search.

Three supplemental live discovery lanes are captured before the decision cutoff: official macro/policy discovery, high-quality narrative attention discovery, and official event/calendar discovery. These are supporting discovery evidence only. They do not become direct D1 facts merely because they were found.

For live runs, `first_available_time` is conservatively no earlier than successful retrieval time unless a stronger independently auditable availability clock is supplied. For historical strict runs, C1 returns a web-retrieved snapshot only when it can establish an official archive/vintage with an explicit publication/vintage identity not later than the cutoff; otherwise it returns unavailable.

## Pre-cutoff discovery lanes

C1 captures four supplemental discovery lanes before the live cutoff freezes: broad official macro/policy data, institutional macro surveys/PMIs, high-quality market narrative, and official event calendars. These lanes are supporting discovery only; W21/W22 and D1 still control admission. Institutional/news discovery never silently upgrades itself to an observed/direct fact.
