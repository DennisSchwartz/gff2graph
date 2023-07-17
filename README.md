# gff2graph
A pipeline to load and transform plant genomes into graph format


## Concept

This is an example implementation of a possible data pipeline built using dagster. 
There are many ways to do this depending on the existing systems and requirements, but I chose dagster because I like
its mental model and wanted to use it for a while.
A lot of my thinking around how to create up-to-date, well tracked data is coming from
[this blog article](https://dagster.io/blog/software-defined-assets) by dagster's lead dev.
Alternative systems could be built on something like Airflow, CWL, Nextflow, Databricks, AWS Glue or even a simple make pipeline.

In my current job I would probably be using Databricks notebooks and PySpark to do this, but that requires a whole cloud setup.
I like the theoretical scalability of Dagster to be able to run locally as well as on a cluster.


## Considerations

My main considerations were as follows:

### Flexibility 
Any system which needs to get things perfect from the get-to is doomed to fail. Iteration and failing fast are key in my opinion. I want a system 
which can grow and change over time, where components can be replaced and upgraded.
It should also not be locked into any specific vendor or environment - ideally a data pipeline can run on my laptop as well as on the cloud.

### Scalability
To continue on from the point above, using a tool like dagster allows relatively simple migration to bigger, cloud-based systems
from a simple starting project. It integrates with things like dbt, Databricks etc.

### Traceability
Initially I implemented a simple pipeline in Python, adding logging and metadata until I realised I was re-inventing the wheel.
Dagster allows orchestration and tracking of data processing, and storing of logs and metadata in a variety of ways and systems.
A simple version of such a system could simply write to log files on my laptop, a more mature system might write to S3, Logstash, or something like cloudwatch.
Using an existing framework means that the location of logs and metadata is simply a configuration choice.

### Change management
Systems change over time, especially in fast-growing companies. In my experience, having systems in which data and code 
is interdependent can cause issues with reliability and makes moving fast a nightmare.
My ideal system *tracks versions of code, data, and data schemas separately*. This allows my system to know if a data 
asset is compatible with a given piece of processing code and can apply it to the latest data if the schemas have not
changed.

### Testing
Data pipelines can be hard to test, since we might not know what we expect the data to look like as it changes over time.
Dagster provides a way to test pipelines out of the box, even though I haven't taken the time to implement tests for this example,
I believe in Test Driven Development and writing tests has saved my bacon many times as complex and growing systems change
over time.

I have also implemented testing frameworks for PySpark data pipelines before, but if there are out-of-the-box solutions I'd rather
use those.

## Drawbacks

There might be ways to use Docker containers directly with dagster such as you would in CWL for example, but I did not 
have time to properly explore this in the time I had.
As such, I had to install genometools manually and access it via Python which isn't ideal.


## Advantages

Software-defined data assets are a great way to specify which data should exist and materialise it when needed. 
Using a tool like dagster allows us to track metadata and configurations of the runs, as well as logs and errors. It
also allows for convenient scheduling in a variety of ways and can run both on my laptop and large, distributed cloud systems.


## Running the example pipeline
To run the example pipeline in this project, you can either run it once in the command line, or use the Dagit UI
to set up and trace runs and run configurations.

### Installation
