# modern-banking-data-stack-pipeline
# Airflow Data Engineering Project with PostgreSQL, MongoDB and Azure

## Project Summary

This is a complete end-to-end data engineering pipeline where I am building a real-world style project from scratch. It includes data generation, data storage, orchestration, and soon data lake and reporting as well. I have designed this project keeping in mind production-level quality and scalability. 

## Objective

The main aim is to simulate a real-world banking use case and build a data pipeline that can generate daily data, store into structured and unstructured databases, and later load into cloud data lake for transformation and reporting.

## Tools and Technologies Used

- Docker (for containerizing PostgreSQL, MongoDB, Airflow)
- PostgreSQL (for structured relational data)
- MongoDB (for semi-structured data like loan applications)
- Apache Airflow (for scheduling and orchestrating DAGs)
- Git and GitHub (for version control)
- Azure Data Lake / Microsoft Fabric (for cloud integration in next phase)
- Power BI or Fabric reporting (for visualization)

## What I Have Done Till Now

- Setup complete environment using Docker containers
- Designed three modular DAGs in Apache Airflow
  - DAG 1: Data generation using Faker
  - DAG 2: Load structured data into PostgreSQL
  - DAG 3: Load semi-structured data into MongoDB
- Implemented data modeling in PostgreSQL using foreign keys to ensure realistic and relational data
- Used ExternalTaskSensor to control the order of execution between DAGs
- Scheduled the data generation and loading on daily basis
- Fixed issues like broken DAGs, invalid scheduling, and bad data relationships

## What’s Next

- Extract data from PostgreSQL and MongoDB using Airflow
- Load the data into Azure Data Lake or Microsoft Fabric OneLake
- Apply Medallion architecture (Bronze, Silver, Gold)
- Perform data modeling in cloud also while designing Gold layer
- Create fact and dimension tables for analytics
- Build dashboards and KPIs using Power BI or Microsoft Fabric
- Setup CI/CD pipeline to deploy Airflow DAGs using GitHub Actions
- Make the entire project production-ready with version control and monitoring

## Status

Right now this project is under active development. The local pipeline is working fine and I am moving toward cloud phase and reporting part next.

## Folder Structure

