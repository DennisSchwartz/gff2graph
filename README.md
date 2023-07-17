# gff2graph
A pipeline to load and transform plant genomes into graph format


## Concept

This is an example implementation of a possible data pipeline built using dagster. 
There are many ways to do this depending on the existing systems and requirements, but I chose dagster because I like
its mental model and wanted to use it for a while.
Alternative systems could be built on something like Airflow, CWL, Nextflow, Databricks, AWS Glue or even a simple make pipeline.

In my current job I would probably be using Databricks notebooks and PySpark to do this, but that requires a whole cloud setup.
I like the theoretical scalability of Dagster to be able to run locally as well as on a cluster.


## Drawbacks

There might be ways to use Docker containers directly with dagster such as you would in CWL for example, but I did not 
have time to properly explore this in the time I had.
As such, I had to install genometools manually and access it via Python which isn't ideal.