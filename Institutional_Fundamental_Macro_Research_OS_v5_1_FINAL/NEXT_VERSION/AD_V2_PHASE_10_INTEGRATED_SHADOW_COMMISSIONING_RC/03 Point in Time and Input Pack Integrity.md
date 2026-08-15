# Point-in-time integrity

The input pack must carry timestamps for Pressure roots, expected signature declaration, actual response window and Gold observations. P03 retains the hard law that the expected signature is declared no later than the response-window start.

P10 mechanically binds the P02 fingerprint into the already-declared expected signature template; it may not alter expected direction/range after seeing the actual response.