def deploy_function(lambda_client, name: str, zip_path: str, layer_arns: list = None):

    with open(zip_path, "rb") as f:
        code_zip = f.read()

    print(f"\nUpdating function code for {name}")
    response = lambda_client.update_function_code(FunctionName=name, ZipFile=code_zip)
    print(response)

    print(f"\nUpdating function configuration for {name}")
    response = lambda_client.update_function_configuration(
        FunctionName=name, Layers=layer_arns
    )
    print(response)
