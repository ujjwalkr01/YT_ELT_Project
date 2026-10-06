# YT_ELT_Project

## 📌 Summary

This ELT project uses **Apache Airflow** as an orchestration tool, packaged inside Docker containers.

The steps that make up the project are:

1. Data is extracted using the **YouTube API** with Python scripts.
2. The data is initially loaded into a **staging schema** in a Dockerized PostgreSQL database.
3. A Python script performs minor data transformations.
4. The transformed data is then loaded into the **core schema**, also hosted in the Dockerized PostgreSQL database.
5. The first API pull performs the initial full upload.
6. Successive API pulls **upsert** the values for certain variables (columns).
7. Once the core schema is populated and both unit and data quality tests have been implemented, the data is ready for analysis.

---

## 📊 Data Extracted

The following seven variables are extracted from the YouTube API:

| Variable | Description |
|---|---|
| Video ID | Unique identifier of the video |
| Video Title | Title of the video |
| Upload Date | Date the video was uploaded |
| Duration | Duration of the video |
| Video Views | Number of views |
| Likes Count | Number of likes |
| Comments Count | Number of comments |

---

## 🛠️ Tools & Technologies

| Category | Technology |
|---|---|
| Containerization | Docker, Docker Compose |
| Orchestration | Apache Airflow |
| Data Storage | PostgreSQL |
| Programming Languages | Python, SQL |
| CI/CD | GitHub Actions |
| Data Source | YouTube API |

---

## 🐳 Containerization

To deploy Airflow using Docker, the official `docker-compose.yaml` file is used with some changes.

The image used is an **extended Airflow image**, built using a `Dockerfile`.

The image is pulled from and pushed to **Docker Hub** using the GitHub Actions CI/CD workflow YAML file.

Once the image is created, the `docker-compose.yaml` file can be executed to run the multiple containers. This is also handled through the CI/CD workflow.

Database connections and variables are specified as environment variables.

---

## 🔐 Database Connections & Variables

The Airflow connection is specified using a URI format with the following naming convention:

```text
AIRFLOW_CONN_{CONN_ID}
