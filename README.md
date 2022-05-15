#### How to run the system:
1. Create a virtual environment to avoid cluttering your environment
	- sudo apt-get install python3-venv (if not installed)
	- python3 -m venv .venv
	- source .venv/bin/activate
2. Install project requirements:
	- pip3 install -r requirements.txt
3. Run the system:
	- cd src
	- uvicorn main:app --reload

4. The service will be accessible at http://localhost:8000:
	- OpenAPI: http://localhost:8000/docs
	- The OpenAPI endpoint is a fully functional client that allows execution of all APIs without the need for a 3rd party component

**I have provided 2 scripts that automate the setup and run of the program (installReqAndRun.sh & run.sh)**

I have also decided to use [fastapi](https://fastapi.tiangolo.com "fastapi") as the framework of choice to run the web service as well as using [SQLAlchemy](https://www.sqlalchemy.org/ "SQLAlchemy") as the ORM framework for all database related work.


#### Notes regarding system security:
1. As requested, no authentication/authoriation has been implemented
2. If security was desired, a STS service would be used to secure the system:
	- *STS* should be standard-based, ex: OAuth2-based
	- The service could be bundled with the system or, preferably, a cloud-based full-fledged Indenity managment service be used, ex: Azure AD if it was B2B system, or Azure AD B2C if it was a consumer application
	- STS would be used for issuing as well as validating tokens
	- Clamis based authorization would be best option as it can easily scalled along with the business needs


#### Anyhting else could be done?
1. ALOT, testing (unit tests and/or acceptance tests) would be at the top
2. Refactor the code to use dependecy injection, especially when acquiring db instances (instead of currently creating them at module level)
3. Evolving the APIs into separate microservices (ex: perhaps this is going to be a SaaS product and companies, user & projects would be large services)
4. Probably, performance testing & optimization would be needed to support the system at scale
5. Dockerizing the services and running the system on Kubernetes (along with adopting an IaC tool)
6. Last, but not least, improving error handling, add logging, tracing and monitoring capabilities


#### How to service the system in a cloud environment?
1. The first step is automation, from build, test and deploy to run and monitoring the system's overall health
2. Utilizing build & deploy pipelines would greatly simplify this process
3. A good rollback & DR strategy would assure business continuity in the face of service disruption
4. Preference would be given to use cloud-native PaaS and/SaaS services or IaaS or custom services to free up resources and focus on adding critical business value
