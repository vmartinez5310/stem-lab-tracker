# Integrating Financial Engine into STEM-Lab Tracker

## Goal

Use **one identity** (Shared-Auth-Service) for all STEM practice layers **and** the Financial Engine.

See full monorepo README and Shared-Auth API for register / OTP / grant-role / JWT contract.

Default apps: science, technology, engineering, mathematics, financial-engine.

Financial Engine validates JWT with the shared SECRET_KEY and requires `financial-engine` in the apps claim.
