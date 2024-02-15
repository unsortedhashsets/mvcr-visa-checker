## mvcr-visa-checker

Small Python script with selenium to check residence permit status on https://frs.gov.cz/informace-o-stavu-rizeni/ with Github actions pipeline

For use with GH actions define `environment` -> `secret` -> `VISA_STRING` in format `OAM-000123-XX/DP-2000`

For local use add `.env` file with `VISA_STRING` in the format `OAM-000123-XX/DP-2000`
