from lazydocs import generate_docs

# The parameters of this function correspond to the CLI options
generate_docs(
    ["th2_data_services"],
    # ignored_modules=[],
    output_path="./documentation/api",
    overview_file="index.md",
    validate=False,
    remove_package_prefix=True,
)
