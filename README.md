This is a utility project designed to cater neccessities for warming up `Lambda` functions to prevent cold starts.

## Table Of Contents

- [Table Of Contents](#table-of-contents)
- [Installing Warmer](#installing-warmer)
- [Using Warmer](#using-warmer)
- [Setting up Event Bridge Notifications](#setting-up-event-bridge-notifications)
- [Working on enhancements](#working-on-enhancements)

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
@warmer(flag="custom_event_key", _concurrency=1)
def handler(event, context):
    pass
```

> Parameters:
> *flag* (type: str)- name of the event flag to look for 
> *_concurrency* (type: int)- (optional) Number of concurrent handlers to warm up, default: 1


If your handler is a Flask/FastApi application, you may follow below steps:

```python
from warmer import warmer
from flask import Flask
app = Flask()
@warmer(flag="custom_event_key",_concurrency=1)
def application(event, context):
    return app(event, context)

# or

application = warmer(flag="custom_event_key",_concurrency=1)(app)

# you may now use application as your handler
```

> `warmer` will help you cater the custom events that are coming for warming _Lambda_ function.
> Though `_concurrency` is optional and by default it only warms up current execution. In case you want to warm up multiple instances of lambda handler, you may need to adjust `_concurrency` to *number of handlers running*.

> `Warmer` uses threading mechnism to ensure that the warming calls are actually happening concurrently and not serially.

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

You may also use `AWS SAM` template to create `Event Bridge Notifications` to warm up `Lambda` function.

```yaml
TransactionCompsAPI:
  Type: "AWS::Serverless::Function"
  Properties:
    FunctionName: fake-function
    Events:
      WarmerSchedule: # add this event to the same template
        Type: Schedule
        Properties:
          Schedule: cron(*/5 * ? * 2-6 *)
          Name: fake-function-warmer-event
          Description: Warmer Event for Lambda Function
          Enabled: true
          Input: '{"warmer": true}' # this refers to the warmer flag
```

In case you want to include concurrent executions, you may add below to include concurrent invocations.

```yaml
TransactionCompsAPI:
  Type: "AWS::Serverless::Function"
  Properties:
    FunctionName: fake-function
    Events:
      WarmerSchedule: # add this event to the same template
        Type: Schedule
        Properties:
          Schedule: cron(*/5 * ? * 2-6 *)
          Name: fake-function-warmer-event
          Description: Warmer Event for Lambda Function
          Enabled: true
          Input: '{"warmer": true, "concurrency": 5}' # this refers to the warmer flag and concurrency
```

<a name="working-on-enhancements"></a>
## Working on enhancements

If you want to work on enhancements or development, you may clone the project and run the below commands to setup environment:

```bash
python -m pip install pipenv
pipenv shell

# or

python -m pip install virtualenv
virtualenv venv
source venv/bin/activate
python -m pip install -r dev_requirements.txt
```

You may also raise a `PR` to get merged into existing project.

Happy Warming.
