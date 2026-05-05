# To make the modSecurity hardened add env variables that enforces protection

## 1. Replaces CRS's PARANOIA default value(1: less aggressive rules) to 2, 3 or 4
The most protection = risks to get false blocking of valid requests
The optimal levels:
`PARANOIA`: 2 or 3
`BLOCKING_PARANOIA`: 2 or 3
`DETECTION_PARANOIA`: 3

## 2. Number of rules that were violated needed to block the request
2=NOTICE
3=WARNING
4=ERROR
5=CRITICAL
`ANOMALY_INBOUND`: 3 (default value was 5, so now we don't wait critical number of violated rules and block the request earlier)

## 3. A string value enabling ModSecurity itself 
`MODSEC_RULE_ENGINE`: on

## 4. Maximum request body size (all body, files included)
`MODSEC_REQ_BODY_LIMIT`: 6553600 (half from the default value)
Maximum request body size (just body without attachments)
`MODSEC_REQ_BODY_NOFILES_LIMIT`: 65536 (half from the default value)
Maximum number of arguments that can be processed before setting the REQBODY_ERROR
`MODSEC_ARGUMENTS_LIMIT`: 500 (half from the default value)

## 5. HTTPs
`SSL_PORT`: 443

http should redirect to https. Don't add this variables till we have ssl certificate
`NGINX_ALWAYS_TLS_REDIRECT`: on