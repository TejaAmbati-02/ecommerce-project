# Retail Data Processing Application

A PySpark-based data processing application that analyzes retail customer and order data. This project demonstrates ETL (Extract, Transform, Load) operations using Apache Spark, including data reading, filtering, joining, and aggregation.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Data Processing Pipeline](#data-processing-pipeline)
- [Environment Setup](#environment-setup)
- [Contributing](#contributing)
- [License](#license)

## Overview

This application processes retail data across multiple environments (LOCAL, TEST, PROD) using Apache Spark. It reads customer and order data from CSV files, applies business logic to filter and aggregate data, and generates insights about order distribution across different states.

The project is designed with modularity and configuration management in mind, allowing seamless execution across different deployment environments without code changes.

## Features

- **Multi-Environment Support**: Easily switch between LOCAL, TEST, and PROD environments
- **Modular Architecture**: Separated concerns with dedicated modules for data reading, manipulation, and configuration
- **Spark DataFrame Processing**: Efficient data processing using Apache Spark
- **Configuration Management**: Environment-specific configurations for data paths and Spark settings
- **Order Analysis**: Filter, join, and aggregate order data by customer state
- **Scalable Design**: Built to handle large datasets with horizontal scaling

## Project Structure

```
ecommerce-project/
├── main.py                      # Entry point of the application
├── Pipfile                      # Python dependencies (Pipenv)
├── Pipfile.lock                 # Locked dependency versions
├── configs/
│   ├── application.conf         # Application configuration (file paths)
│   └── pyspark.conf            # Spark configuration settings
├── data/
│   ├── customers.csv           # Customer data
│   └── orders.csv              # Order data
├── lib/
│   ├── ConfigReader.py         # Configuration management utilities
│   ├── DataReader.py           # Data reading and schema definitions
│   ├── DataManupulation.py     # Data transformation logic
│   └── Utils.py                # Utility functions (Spark session creation)
└── README.md                    # This file
```

## Prerequisites

- **Python**: 3.7 or higher
- **Java**: 8 or higher (required by Spark)
- **Apache Spark**: 2.4+ (installed via Pipenv)
- **Pipenv**: For Python dependency management

### System Requirements

- Minimum 4GB RAM for local development
- 500MB disk space for dependencies
- macOS, Linux, or Windows (with appropriate Java/Scala setup)

## Installation

### 1. Clone or Download the Project

```bash
git clone <repository-url>
cd ecommerce-project
```

### 2. Install Dependencies

Ensure `pipenv` is installed:

```bash
pip install pipenv
```

Install project dependencies:

```bash
pipenv install
```

This installs all packages specified in `Pipfile`, including PySpark.

### 3. Download Java (if not installed)

For macOS:
```bash
brew install openjdk@11
```

For Linux:
```bash
sudo apt-get install openjdk-11-jdk
```

Verify Java installation:
```bash
java -version
```

## Configuration

### Application Configuration (`configs/application.conf`)

Contains file paths for data sources:

```ini
[LOCAL]
customers.file.path = data/customers.csv
orders.file.path = data/orders.csv

[TEST]
customers.file.path = data/customers.csv
orders.file.path = data/orders.csv

[PROD]
customers.file.path = data/customers.csv
orders.file.path = data/orders.csv
```

Modify file paths based on your data location.

### Spark Configuration (`configs/pyspark.conf`)

Contains Apache Spark settings:

```ini
[LOCAL]
spark.app.name = retail-local

[TEST]
spark.app.name = retail-test
spark.executor.instances = 3
spark.executor.cores = 5
spark.executor.memory = 15GB

[PROD]
spark.app.name = retail-prod
spark.executor.instances = 3
spark.executor.cores = 5
spark.executor.memory = 15GB
```

Adjust executor settings based on your cluster resources.

## Usage

### Running the Application

Execute the application with the environment as an argument:

```bash
# Local environment
pipenv run python main.py local

# Test environment
pipenv run python main.py test

# Production environment
pipenv run python main.py prod
```

### Expected Output

The application will:
1. Create a Spark session for the specified environment
2. Read customer and order data from configured paths
3. Filter orders with status "CLOSED"
4. Join orders with customer information
5. Group and count orders by state
6. Display results in a table format

Example output:
```
Creating Spark Session
Created Spark Session
+-----+-----+
|state|count|
+-----+-----+
|  CA |  150|
|  TX |  120|
|  NY |  100|
|  FL |   85|
+-----+-----+
end of main
```

## Data Processing Pipeline

### Step 1: Read Data
- **Customers**: Reads `customers.csv` with schema including customer_id, name, address, state, etc.
- **Orders**: Reads `orders.csv` with schema including order_id, order_date, customer_id, order_status

### Step 2: Filter Orders
- Filters orders where `order_status = 'CLOSED'`
- Reduces dataset to relevant records

### Step 3: Join Data
- Performs inner join between filtered orders and customer data on `customer_id`
- Enriches order records with customer information including state

### Step 4: Aggregate Results
- Groups by customer state
- Counts the number of closed orders per state
- Generates summary statistics

## Module Descriptions

### `ConfigReader.py`

Handles configuration file parsing:

- `get_app_conf(env)`: Reads application.conf and returns file paths for given environment
- `get_pyspark_config(env)`: Reads pyspark.conf and returns SparkConf object

### `DataReader.py`

Manages data ingestion:

- `get_customers_schema()`: Defines customer data structure
- `read_customers(spark, env)`: Reads customer CSV with proper schema
- `get_orders_schema()`: Defines order data structure
- `read_orders(spark, env)`: Reads order CSV with proper schema

### `DataManupulation.py`

Implements business logic transformations:

- `filter_closed_orders(orders_df)`: Filters orders with CLOSED status
- `join_orders_customers(orders_df, customers_df)`: Joins orders and customer data
- `count_orders_state(joined_df)`: Aggregates orders by state

### `Utils.py`

Provides utility functions:

- `get_spark_session(env)`: Creates and configures SparkSession based on environment
  - Local mode: Uses local[2] master
  - Remote modes (TEST/PROD): Enables Hive support for cluster execution

## Environment Setup

### For Development (Local)

```bash
# Activate Pipenv shell
pipenv shell

# Run application
python main.py local
```

### For Testing

```bash
pipenv run python main.py test
```

### For Production

```bash
# Submit to Spark cluster
spark-submit --properties-file configs/pyspark.conf main.py prod
```

## Data Format Requirements

### Customers CSV (`data/customers.csv`)

Expected columns:
- `customer_id` (int)
- `customer_fname` (string)
- `customer_lname` (string)
- `username` (string)
- `password` (string)
- `address` (string)
- `city` (string)
- `state` (string)
- `pincode` (string)

### Orders CSV (`data/orders.csv`)

Expected columns:
- `order_id` (int)
- `order_date` (string)
- `customer_id` (int)
- `order_status` (string)

## Troubleshooting

### Issue: "Java not found"
**Solution**: Install Java using the commands in the Prerequisites section.

### Issue: "Module not found: pyspark"
**Solution**: Run `pipenv install` to install all dependencies.

### Issue: "File not found" errors
**Solution**: Verify file paths in `configs/application.conf` match your data location.

### Issue: Spark session creation fails
**Solution**: Check Spark configuration in `configs/pyspark.conf` matches your system resources.

## Performance Optimization Tips

1. **Increase Executor Memory**: Adjust `spark.executor.memory` for large datasets
2. **Tune Parallelism**: Adjust `spark.executor.cores` and `spark.executor.instances`
3. **Partition Data**: For very large datasets, partition inputs by state before processing
4. **Caching**: Use `.cache()` for DataFrames used multiple times

## Contributing

1. Create a feature branch
2. Make your changes
3. Test with `python main.py local`
4. Submit a pull request

## Future Enhancements

- [ ] Add support for Parquet data format
- [ ] Implement data validation and quality checks
- [ ] Add logging framework
- [ ] Create unit tests for data transformations
- [ ] Add support for database sources (PostgreSQL, MySQL)
- [ ] Implement incremental processing
- [ ] Add data partitioning strategies

## License

This project is provided as-is for educational and development purposes.

---

**Last Updated**: April 2026  
**Version**: 1.0.0
