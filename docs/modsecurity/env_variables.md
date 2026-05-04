To make the modSecurity hardened add env variables that enforces protection

Replaces CRS's PARANOIA default value(1: less aggressive rules) to 2, 3 or 4
The most protection = risks to get false blocking of valid requests
The optimal levels:
`PARANOIA="2"`
`BLOCKING_PARANOIA="2"`
`DETECTION_PARANOIA="3"`

A string value enabling ModSecurity itself 
`MODSEC_RULE_ENGINE="on"`

Maximum request body size (all body, files included)
`MODSEC_REQ_BODY_LIMIT="6553600"`
Maximum request body size (just body without attachments)
`MODSEC_REQ_BODY_NOFILES_LIMIT="65536"`
Maximum number of arguments that can be processed before setting the REQBODY_ERROR
`MODSEC_ARGUMENTS_LIMIT="500"`

`SSL_PORT="443"`

http should redirect to https. Don't add this variables till we have ssl certificate
`NGINX_ALWAYS_TLS_REDIRECT="on"`