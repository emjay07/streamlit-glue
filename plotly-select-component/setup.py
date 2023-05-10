import setuptools

setuptools.setup(
    name="plotly-select-component",
    version="0.0.1",
    author="",
    author_email="",
    description="Component to allow Plotly select tools",
    long_description="",
    long_description_content_type="text/plain",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 1.0",
    ],
)
