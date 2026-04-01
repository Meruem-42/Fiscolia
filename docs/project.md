# Fiscolia

## Description


### Web
- [**2pts**] `Major`: Use a framework for both the frontend and backend.
	- Use a frontend framework (React, Vue, Angular, Svelte, etc.).
	- Use a backend framework (Express, NestJS, Django, Flask, Ruby on Rails, etc.).
	- Full-stack frameworks (Next.js, Nuxt.js, SvelteKit) count as both if you use both their frontend and backend capabilities.

> :warning: Total web: 2pts

### Cybersecurity
- [**2pts**] `Major`: Implement WAF/ModSecurity (hardened) + HashiCorp Vault for secrets:
	- Configure strict ModSecurity/WAF.
	- Manage secrets in Vault (API keys, credentials, environment variables), encrypted and isolated.

> :warning: Total Cyber: 2pts

### DevOps

- [**2pts**] `Major`: Infrastructure for log management using ELK (Elasticsearch, Logstash, Kibana).
	- Elasticsearch to store and index logs.
	- Logstash to collect and transform logs.
	- Kibana for visualization and dashboards.
	- Implement log retention and archiving policies.
	- Secure access to all components.
- [**2pts**] `Major`: Monitoring system with Prometheus and Grafana.
	- Set up Prometheus to collect metrics.
	- Configure exporters and integrations.
	- Create custom Grafana dashboards.
	- Set up alerting rules.
	- Secure access to Grafana.
- [**2pts**] `Major`: Backend as microservices.
	- Design loosely-coupled services with clear interfaces.
	- Use REST APIs or message queues for communication.
	- Each service should have a single responsibility.
- [**1pts**] `Minor`: Health check and status page system with automated backups and disaster recovery procedures.

> :warning: Total DevOps: 7pts


### AI
- [**2pts**] `Major`: Implement a complete RAG (Retrieval-Augmented Generation) system.
	- Interact with a large dataset of information.
	- Users can ask questions and get relevant answers.
	- Implement proper context retrieval and response generation.
- [**2pts**] `Major`: Implement a complete LLM system interface.
	- Generate text and/or images based on user input.
	- Handle streaming responses properly.
	- Implement error handling and rate limiting.
- [**2pts**] `Major`: Recommendation system using machine learning.
	- Personalized recommendations based on user behavior.
	- Collaborative filtering or content-based filtering.
	- Continuously improve recommendations over time.
- [**1pts**] `Minor`: Content moderation AI (auto moderation, auto deletion, auto warning,
etc.)
- [**1pts**] `Minor`: Image recognition and tagging system.

> :warning: Total AI: 8pts

___

> :warning: Total : 19pts
