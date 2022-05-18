This is a utility project designed to cater neccessities for warming up `Lambda` functions to prevent cold starts.

## Table Of Contents

- [Table Of Contents](#table-of-contents)
- [Installing Warmer](#installing-warmer)
- [Using Warmer](#using-warmer)
- [Setting up Event Bridge Notifications](#setting-up-event-bridge-notifications)

#

[![upload-artifacts-and-release-new-version](https://github.com/satyamsoni2211/LambdaWarmerPy/actions/workflows/release.yaml/badge.svg)](https://github.com/satyamsoni2211/LambdaWarmerPy/actions/workflows/release.yaml) [![PyPI version](https://badge.fury.io/py/py-lambda-warmer.svg)](https://badge.fury.io/py/py-lambda-warmer)

<a name="installing-warmer"></a>

## Installing Warmer

To install module, run the below command:

```bash
python3 -m pip install py_lambda_warmer

# or

python3 -m pip install py_lambda_warmer==<release-version>
```

<a name="using-warmer"></a>

## Using Warmer

This is very easy to incorporate in your existing Python Lambda Handlers. Follow the below code.

```python
from warmer import warmer
@warmer(flag="custom_event_key")
def handler(event, context):
    pass
```

If you handler is a Flask/FastApi application, you may follow below steps:

```python
from warmer import warmer
from flask import Flask
app = Flask()
@warmer(flag="custom_event_key")
def application(event, context):
    app(event, context)

# or

application = warmer(flag="custom_event_key")(app)

# you may now use application as your handler
```

> `warmer` will help you cater the custom events that are coming for warming _Lambda_ function.

<a name="setting-up-event-bridge-notifications"></a>

## Setting up Event Bridge Notifications

You can also setup you custom event bridge schedule for Lambda function using the `Terraform Resource` code mentioned in
the repository.

Simply download the `Terraform` code attached in the release and unzip it.

```bash
wget https://github.com/satyamsoni2211/LambdaWarmerPy/releases/download/${release}/terraform_code.zip
unzip terraform_code.zip -d terraform_code/
cd terraform_code/
# creating variable file required by terraform
cat << EOF > .auto.tfvars
arn = <arn of your lambda function>
profile = <profile alias for aws>
region = <region for aws lambda>
EOF
# initiating and applying
terraform init
terraform plan -out tfplan
terraform apply tfplan
```

You may also modify resource names as per your requirements in the code.

Happy Warming.
