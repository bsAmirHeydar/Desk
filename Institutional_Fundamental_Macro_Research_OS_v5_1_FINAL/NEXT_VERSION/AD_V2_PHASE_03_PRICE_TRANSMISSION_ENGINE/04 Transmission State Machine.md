---
title: "Price Transmission State Machine"
type: scientific-contract
status: shadow-development
---
# Transmission State Machine

P03 classifies the target response relative to the frozen expected signature.

## States

### `NOT_YET_OBSERVABLE`
The response window is earlier than the declared earliest material-response time.

### `DELAYED`
No material aligned response is visible yet, but the observation remains inside the declared maximum lag window.

### `COMPRESSION`
No material aligned response is visible after the declared expected lag has elapsed. Compression is a response state, **not proof of absorption**.

### `ALIGNED_INCOMPLETE`
Price is moving with Pressure but remains below the lower expected-response range while the allowed lag window remains open.

### `UNDER_TRANSMISSION`
Price is moving with Pressure but remains below the expected range after the allowed lag window has elapsed.

### `ALIGNED`
Pressure-aligned response falls inside the frozen expected range.

### `OVER_TRANSMISSION`
Response is aligned but materially exceeds the frozen expected upper range. This can mean overshoot, amplification, an additional driver or model miss; it is not automatic reversal evidence.

### `NEGATIVE_TRANSMISSION`
Target response is materially opposite to Pressure.

### `ALIGNED_DIRECTION_ONLY`
Direction aligns but no defensible magnitude range was frozen, so magnitude conclusions are prohibited.

### `UNDETERMINED`
Evidence, timing, unit, Pressure state or expected signature is insufficient for a defensible classification.

## No `RELEASE` in P03

A price turn in the direction of Pressure is not yet `Release`. P04 must combine P02 Pressure, P03 Transmission and independent evidence before Release science may exist.
