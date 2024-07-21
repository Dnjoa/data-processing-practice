# Data Processing Practice

This project demonstrates an end-to-end data processing workflow using Python, PySpark, and Airflow. It includes ETL jobs for loading, preprocessing, transforming, and publishing data. The project is designed to be run either locally with a virtual environment or using Docker for containerization.

## Getting Started

### Prerequisites

- Python 3.x
- Pyspark
- Java 17
- Docker and Docker Compose (optional, for containerized setup)

### Environment Setup

#### Virtual Environment

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
