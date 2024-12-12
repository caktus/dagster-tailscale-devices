from setuptools import find_packages, setup

setup(
    name="dagster_tailscale_devices",
    packages=find_packages(exclude=["dagster_tailscale_devices_tests"]),
    install_requires=["dagster", "dagster-cloud"],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
