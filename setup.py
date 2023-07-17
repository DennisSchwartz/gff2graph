from setuptools import find_packages, setup

setup(
    name="dagster_pipeline",
    packages=find_packages(exclude=["gff2graph_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
