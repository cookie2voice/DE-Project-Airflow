# Table of Contents
- [To Do](#ToDo)
- [Introduction To Data Modeling](#IntroductionToDataModeling)
- [Relations Data Models](#RelationsDataModels)
- [NoSQL Data Models](#NoSQLDataModels)
- [Cloud Data Warehouses](#CloudDataWarehouses)
    - [Introduction To Data Warehouses](#IntrucitonToDataWareHouses)
- [Automating Data Pipelines](#AutomatingDataPipelines)
    - [Course Introduction](#CourseIntroduction)
- [UsfulLinks](#UsfulLinks)


<br>

## ToDo
- Go through pyspark docs

## IntroductionToDataModeling

### ACID Transactions
Properties of database transactions intended to guarantee validity even in the event of errors or power failures.

Atomicity: The whole transaction is processed or nothing is processed. A commonly cited example of an atomic transaction is money transactions between two bank accounts. The transaction of transferring money from one account to the other is made up of two operations. First, you have to withdraw money in one account, and second you have to save the withdrawn money to the second account. An atomic transaction, i.e., when either all operations occur or nothing occurs, keeps the database in a consistent state. This ensures that if either of those two operations (withdrawing money from the 1st account or saving the money to the 2nd account) fail, the money is neither lost nor created. Source Wikipedia for a detailed description of this example.
Consistency: Only transactions that abide by constraints and rules are written into the database, otherwise the database keeps the previous state. The data should be correct across all rows and tables. Check out additional information about consistency on Wikipedia.
Isolation: Transactions are processed independently and securely, order does not matter. A low level of isolation enables many users to access the data simultaneously, however this also increases the possibilities of concurrency effects (e.g., dirty reads or lost updates). On the other hand, a high level of isolation reduces these chances of concurrency effects, but also uses more system resources and transactions blocking each other. Source: Wikipedia

Durability: Completed transactions are saved to database even in cases of system failure. A commonly cited example includes tracking flight seat bookings. So once the flight booking records a confirmed seat booking, the seat remains booked even if a system failure occurs. Source: Wikipedia.

### When NOT to use a NoSQL Database?
When you have a small dataset: NoSQL databases were made for big datasets not small datasets and while it works it wasn’t created for that.
When you need ACID Transactions: If you need a consistent database with ACID transactions, then most NoSQL databases will not be able to serve this need. NoSQL database are eventually consistent and do not provide ACID transactions. However, there are exceptions to it. Some non-relational databases like MongoDB can support ACID transactions.
When you need the ability to do JOINS across tables: NoSQL does not allow the ability to do JOINS. This is not allowed as this will result in full table scans.
If you want to be able to do aggregations and analytics
If you have changing business requirements : Ad-hoc queries are possible but difficult as the data model was done to fix particular queries
If your queries are not available and you need the flexibility : You need your queries in advance. If those are not available or you will need to be able to have flexibility on how you query your data you might need to stick with a relational database
Caveats to NoSQL and ACID Transactions
There are some NoSQL databases that offer some form of ACID transaction. As of v4.0, MongoDB added multi-document ACID transactions within a single replica set. With their later version, v4.2, they have added multi-document ACID transactions in a sharded/partitioned deployment.

Check out this documentation from MongoDB on multi-document ACID transactions
Here is another link documenting MongoDB's ability to handle ACID transactions
Another example of a NoSQL database supporting ACID transactions is MarkLogic.

Check out this link from their blog that offers ACID transactions.

## RelationsDataModels

### Importance of Relational Databases:
Standardization of data model: Once your data is transformed into the rows and columns format, your data is standardized and you can query it with SQL
Flexibility in adding and altering tables: Relational databases gives you flexibility to add tables, alter tables, add and remove data.
Data Integrity: Data Integrity is the backbone of using a relational database.
Structured Query Language (SQL): A standard language can be used to access the data with a predefined language.
Simplicity : Data is systematically stored and modeled in tabular format.
Intuitive Organization: The spreadsheet format is intuitive but intuitive to data modeling in relational databases.

### OLAP VS OTLP
Online Analytical Processing (OLAP):

Databases optimized for these workloads allow for complex analytical and ad hoc queries, including aggregations. These type of databases are optimized for reads.

Online Transactional Processing (OLTP):

Databases optimized for these workloads allow for less complex queries in large volume. The types of queries for these databases are read, insert, update, and delete.

The key to remember the difference between OLAP and OLTP is analytics (A) vs transactions (T). If you want to get the price of a shoe then you are using OLTP (this has very little or no aggregations). If you want to know the total stock of shoes a particular store sold, then this requires using OLAP (since this will require aggregations).

Additional Resource on the difference between OLTP and OLAP:
This Stackoverflow post describes it well: https://stackoverflow.com/questions/21900185/what-are-oltp-and-olap-what-is-the-difference-between-them

### Normalization and Denormalization
Normalization will feel like a natural process, you will reduce the number of copies of the data and increase the likelihood that your data is correct in all locations.

Normalization organizes the columns and tables in a database to ensure that their dependencies are properly enforced by database integrity constraints.

We don’t want or need extra copies of our data, this is data redundancy. We want to be able to update data in one place and have that be the source of truth, that is data integrity.

Denormalization will not feel as natural, as you will have duplicate copies of data, and tables will be more focused on the queries that will be run.

Here is an example table we will be using later in our demo and exercises. Let’s say we have a table called music_library, looks pretty standard but this is not a normalized table.

### Objectives of Normal Form:
To free the database from unwanted insertions, updates, & deletion dependencies
To reduce the need for refactoring the database as new types of data are introduced
To make the relational model more informative to users
To make the database neutral to the query statistics
See this Wikipedia page to learn more.

"OLTP queries will have little aggregations really, if any, while OLAP will heavily focus on aggregations."

### How reach Normal Form

How to reach First Normal Form (1NF):

Atomic values: each cell contains unique and single values
Be able to add data without altering tables
Separate different relations into different tables
Keep relationships between tables together with foreign keys

Second Normal Form (2NF):
Have reached 1NF
All columns in the table must rely on the Primary Key

Third Normal Form (3NF):
Must be in 2nd Normal Form
No transitive dependencies
Remember, transitive dependencies you are trying to maintain is that to get from A-> C, you want to avoid going through B.
When to use 3NF:

When you want to update data, we want to be able to do in just 1 place. We want to avoid updating the table in the Customers Detail table (in the example in the lecture slide).


### Snowflake Schema
Star Schema is a special, simplified case of the snowflake schema.
Star schema does not allow for one to many relationships while the snowflake schema does.
Snowflake schema is more normalized than Star schema but only in 1NF or 2NF

###
- Data constrains: not null(could be multiple), unique(could be multiple), primary key(not null and unique, only one)
- upsert
```
INSERT INTO customer_address (customer_id, customer_street)
VALUES
    (
    432, '923 Knox Street, Suite 1'
)
ON CONFLICT (customer_id)
DO UPDATE
    SET customer_street  = EXCLUDED.customer_street;
```

## NoSQLDataModels

### When to Use NoSQL:
- Need high Availability in the data: Indicates the system is always up and there is no downtime
- Have Large Amounts of Data
- Need Linear Scalability: The need to add more nodes to the system so performance will increase linearly
- Low Latency: Shorter delay before the data is transferred once the instruction for the transfer has been received.
- Need fast reads and write

### Eventual Consistency:
Over time (if no new changes are made) each copy of the data will be the same, but if there are new changes, the data may be different in different locations. The data may be inconsistent for only milliseconds. There are workarounds in place to prevent getting stale data.

### Is data deployment strategy an important element of data modeling in Apache Cassandra?

Deployment strategies are a great topic, but have very little to do with data modeling. Developing deployment strategies focuses on determining how many clusters to create or determining how many nodes are needed. These are topics generally covered under database architecture, database deployment and operations, which we will not cover in this lesson.

In general, the size of your data and your data model can affect your deployment strategies. You need to think about how to create a cluster, how many nodes should be in that cluster, how to do the actual installation. More information about deployment strategies can be found on this DataStax documentation page


### Apache Cassandra Data Architecture:

Understanding the architecture: https://docs.datastax.com/en/archived/cassandra/3.0/cassandra/architecture/archTOC.html
Cassandra Architecture: https://www.tutorialspoint.com/cassandra/cassandra_architecture.htm

### CAP Theorem:
- Consistency: Every read from the database gets the latest (and correct) piece of data or an error

- Availability: Every request is received and a response is given -- without a guarantee that the data is the latest update

- Partition Tolerance: The system continues to work regardless of losing network connectivity between nodes

### Data Modeling in Apache Cassandra:
- Denormalization is not just okay -- it's a must
- Denormalization must be done for fast reads
- Apache Cassandra has been optimized for fast writes
- ALWAYS think Queries first
- One table per query is a great strategy
- Apache Cassandra does not allow for JOINs between tables
- https://docs.datastax.com/en/dse/6.7/cql/cql/ddl/dataModelingApproach.html

### Cassandra Query Language
Cassandra query language is the way to interact with the database and is very similar to SQL.
The following are not supported by CQL
    - JOINS
    - GROUP BY
    - Subqueries

### Primary Key
- Must be unique
- The PRIMARY KEY is made up of either just the PARTITION KEY or may also include additional CLUSTERING COLUMNS
- A Simple PRIMARY KEY is just one column that is also the PARTITION KEY. A Composite PRIMARY KEY is made up of more than one column and will assist in creating a unique value and in your retrieval queries
- The PARTITION KEY will determine the distribution of data across the system
- https://docs.datastax.com/en/archived/cql/3.3/cql/cql_using/useSimplePrimaryKeyConcept.html#useSimplePrimaryKeyConcept


### Clustering Columns:
- The clustering column will sort the data in sorted ascending order, e.g., alphabetical order.*
- More than one clustering column can be added (or none!)
- From there the clustering columns will sort in order of how they were added to the primary key
- Commonly Asked Questions:
- How many clustering columns can we add?

    You can use as many clustering columns as you would like. You cannot use the clustering columns out of order in the SELECT statement. You may choose to omit using a clustering column in your SELECT statement. That's OK. Just remember to use them in order when you are using the SELECT statement.
- https://docs.datastax.com/en/archived/cql/3.3/cql/cql_using/useCompoundPrimaryKeyConcept.html
- https://stackoverflow.com/questions/24949676/difference-between-partition-key-composite-key-and-clustering-key-in-cassandra


## CloudDataWarehouses

### IntrucitonToDataWareHouses

- Dimensional Model Review
    - Goals of the Star Schema
    Easy to understand
    Fast analytical query performance
    Fact Tables

    Record business events, like an order, a phone call, a book review
    Fact tables columns record events recorded in quantifiable metrics like quantity of an item, duration of a call, a book rating
    Dimension Tables

    Record the context of the business events, e.g. who, what, where, why, etc..
    Dimension tables columns contain attributes like the store at which an item is purchased or the customer who made the call, etc.

- Naive Extract Transform and Load (ETL): From Third Normal Form to ETL
    Extract

    Query the 3NF DB
    Transform

    Join tables together
    Change types
    Add new columns
    Load

    Insert into facts & dimension tables

- quantifiable data or numeric data is the best candidate for a Fact table.

### Project
- Top 8 Best Practices for High-Performance ETL Processing Using Amazon Redshift
    https://aws.amazon.com/blogs/big-data/top-8-best-practices-for-high-performance-etl-processing-using-amazon-redshift/
- How I built a data warehouse using Amazon Redshift and AWS services in record time
    https://aws.amazon.com/blogs/big-data/how-i-built-a-data-warehouse-using-amazon-redshift-and-aws-services-in-record-time/
- Redshift ETL: 3 Ways to load data into AWS Redshift
    https://panoply.io/data-warehouse-guide/redshift-etl/
- 2X Your Redshift Speed With Sortkeys and Distkeys
    https://www.sisense.com/blog/double-your-redshift-performance-with-the-right-sortkeys-and-distkeys/
- recommended chart programe: https://lucid.app/documents#/templates?folder_id=home
- awesome-readme: https://github.com/matiassingers/awesome-readme
- PEP8: https://realpython.com/python-pep8/
- Well-formated sql: https://gist.github.com/fredbenenson/7bb92718e19138c20591


## AutomatingDataPipelines

### CourseIntroduction
Course Introduction
In this course, you'll learn about the concept of data pipelines, and how you can use them to accelerate your career as a data engineer.

This course will focus on applying the data pipeline concepts you'll learn through an open-source tool from Airbnb called Apache Airflow.

In the first lesson, you'll learn about data pipeline concepts including:

Data Validation
Direct Acyclic Graphs (DAG)
DAGs in Apache Airflow
Building DAGs and running them in Airflow
In the second lesson, we'll cover data quality concepts including

Data lineage in Airflow
Data pipeline schedules
Data partitioning
The third lesson is about using data pipelines in production. You'll learn about:

Extending Airflow with Plugins
Task boundaries
and when to refactor a DAG
Once you've completed this course, you will be ready to apply these skills in your career as a data engineer.

### Order of Operations For an Airflow DAG
- The Airflow Scheduler starts DAGs based on time or external triggers.
- Once a DAG is started, the Scheduler looks at the steps within the DAG and determines which steps can run by looking at their dependencies.
- The Scheduler places runnable steps in the queue.
- Workers pick up those tasks and run them.
- Once the worker has finished running the step, the final status of the task is recorded and additional tasks are placed by the scheduler until all tasks are complete.
- Once all tasks have been completed, the DAG is complete.



## UsfulLinks
- career portal: https://classroom.udacity.com/career/
- udacity support community: https://udacity.zendesk.com/hc/en-us/community/topics
- FAQ: https://udacity.zendesk.com/hc/en-us
- create db and user with pass: https://databasefaqs.com/postgresql-create-user-with-password/
