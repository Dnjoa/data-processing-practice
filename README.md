# Data Processing Practice

This project demonstrates an end-to-end data processing workflow using Python, PySpark, and Airflow. It includes ETL jobs for loading, preprocessing, transforming, and publishing data. The project is designed to be run either locally with a virtual environment or using Docker for containerization.

## Table of Contents

- [Data Processing Practice](#data-processing-practice)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Environment Setup](#environment-setup)
      - [Running the PySpark job using Virtual Environment](#running-the-pyspark-job-using-virtual-environment)
      - [Running the PySpark job using Docker](#running-the-pyspark-job-using-docker)
  - [Project Structure](#project-structure)

## Getting Started

### Prerequisites

- Python 3.x
- Pyspark
- Java 17
- Docker and Docker Compose (optional, for containerized setup)

### Environment Setup

#### Running the PySpark job using Virtual Environment

1. **Create and Activate a Virtual Environment**

   ```shell
   /usr/local/bin/python3 -m venv myenv  # Adjust the path if necessary
   source myenv/bin/activate
   ```

   To deactivate the virtual environment, run:

   ```shell
   deactivate
   ```

2. **Install Dependencies**

   Within the virtual environment, install the required dependencies:

   ```shell
   pip3 install -r requirements.txt
   ```

3. **Initialize the Airflow Database**

   Before running Airflow, initialize its database:

   ```shell
   airflow db init
   ```

4. **Create an Airflow User**

   Create a user for Airflow's web interface:

   ```shell
   airflow users create \
       --username admin \
       --firstname YOUR_FIRST_NAME \
       --lastname YOUR_LAST_NAME \
       --role Admin \
       --email YOUR_EMAIL
   ```

5. **Start the Airflow Web Server**

   By default, it runs on port 8080:

   ```shell
   airflow webserver --port 8080
   ```

6. **Start the Airflow Scheduler**

   In a new terminal or command prompt, activate your virtual environment and start the Airflow scheduler:

   ```shell
   airflow scheduler
   ```

7. **Configure the Database Connection**

   Ensure your database connection information is configured in [`etl_jobs/config/db_connection_config.py`](etl_jobs/config/db_connection_config.py).

#### Running the PySpark job using Docker

1. **Dockerfile for Airflow with PySpark**

   Use Dockerfile to set up an environment with PySpark, Python, and Airflow.And make ensure that it also installs any other dependencies listed in your requirements.txt.

   ``` dockerfile
   FROM spark:3.5.1-scala2.12-java17-ubuntu
   USER root
   RUN set -ex; \
       apt-get update; \
       apt-get install -y python3 python3-pip; \
       rm -rf /var/lib/apt/lists/*;

   # Install Python dependencies from requirements.txt
   COPY requirements.txt /tmp/
   RUN pip3 install -r /tmp/requirements.txt

   USER spark
   ```

2. **Dcoker Compose File**

   Create a docker-compose.yml file at the root of your project. This file will define two services: one for Airflow and another for PostgreSQL. The Airflow service will use the Dockerfile you've prepared, and the PostgreSQL service will be based on the official PostgreSQL Docker image.

   ``` yml
   version: '3'
   services:
     postgres:
       image: postgres:latest
       environment:
         POSTGRES_USER: "username"
         POSTGRES_PASSWORD: "password"
         POSTGRES_DB: "database_name"
       ports:
         - "5432:5432"

     airflow:
       build: .
       depends_on:
         - postgres
       environment:
         AIRFLOW__CORE__SQL_ALCHEMY_CONN: postgresql+psycopg2://username:password@postgres:5432/database_name
         AIRFLOW__CORE__EXECUTOR: LocalExecutor
         AIRFLOW__CORE__LOAD_EXAMPLES: "false"
       volumes:
         - ./airflow/dags:/opt/airflow/dags
         - ./etl_jobs:/opt/airflow/etl_jobs
         - ./data:/opt/airflow/data
       ports:
         - "8080:8080"
       command: webserver
   ```

   This docker-compose.yml file does the following:

   Sets up a PostgreSQL service with the connection information you provided.
   Builds the Airflow service using the Dockerfile in your project directory. It also sets the AIRFLOW__CORE__SQL_ALCHEMY_CONN environment variable to the connection string for the PostgreSQL database, enabling Airflow to use it as its backend.
   Maps the airflow/dags, etl_jobs, and data directories from your project into the Airflow container, allowing Airflow to access your DAGs and ETL scripts.
   Exposes port 8080 for accessing the Airflow web interface.

3. **Running the service**
   To start the services, navigate to the directory containing your docker-compose.yml file and run:

   ``` shell
   docker-compose up --build
   ```

   This command builds the Airflow image (if it hasn't been built already) and starts the Airflow and PostgreSQL services. You can access the Airflow web interface by navigating to <http://localhost:8080> in your web browser.

## Project Structure

- [`airflow/dags/`]: Airflow DAGs for orchestrating the ETL jobs.
- [`etl_jobs/`]: Python modules for each step of the ETL process.
  - `config/`: Configuration files, including database connection info.
  - [`data_load.py`]: Module for data loading.
  - [`data_preprocessing.py`]: Module for data preprocessing.
  - [`data_transform.py`]: Module for data transformation.
  - [`data_publish.py`]: Module for publishing data.
- [`data/`]: Directory for raw, preprocessed, and transformed data.
- [`Dockerfile`]: Dockerfile for building the project's Docker image. (Consdering the option 2 is still in progress, this file you can ignore)
- [`requirements.txt`]: List of project dependencies.
