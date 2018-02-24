# UCSD-Cloud-Cli 0.1.0

This tool set is designed to enable command-line-level access to common functions related to the security workflow(s) defined within this readme document for the UCSD team to use when configuring their Amazon Web Services environment(s).

## Development Environment Prerequisites

To work on this toolset, you will need several basic requirements installed. We follow a very idiomatic/standard setup for working with Python:

* Python >= 3.4
* [virtualenv](https://pypi.python.org/pypi/virtualenv)
* [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)

Assuming you're working on a mac and have [homebrew](https://brew.sh) installed, the following will install these prerequisites on an OSX machine:

```bash
brew install python3
pip3 install virtualenv
pip3 install virtualenvwrapper
```

For Ubuntu or other Debian based machines, the basic dependencies are very similar:

```bash
sudo apt-get install -y python3
pip3 install virtualenv
pip3 install virtualenvwrapper
```

`virtualenvwrapper` also requires a bit of configuration locally to ensure that it can be used from the terminal properly. Per it's [documentation](https://virtualenvwrapper.readthedocs.io/en/latest/#introduction) you'll want to souce the init script in any terminal session you want to use the toolset in. Additionally, as we're working in python3, you'll want to set an environment variable to indicate to `virtualenvwrapper` which python executable to use. This can be accomplished with the following command, either run in the terminal each time you want to use it, or otherwise added to your environment via `~/.bashrc` or `/etc/bash.bashrc` or otherwise added to your [machine's environment](http://timmyreilly.azurewebsites.net/setup-a-virtualenv-for-python-3-on-windows/) variables:

```bash
VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3
source /usr/local/bin/virtualenvwrapper.sh
```

## Installation

Installation of this project from the command line is simple:

* Download and (if applicable) un-archive this project to a directory of your choosing
* From the command line, navigate to the directory where the `setup.py` script is (should be the directory that was created via `git clone` or when the downloaded zip file was unarchived)
* Before you install, create a virtual environment for this project: `mkvirtualenv -p <path_to_python3> ucsd`
  * if/when you exit and return to the command line, re-enable the `ucsd` virtualenv with the following command: `workon ucsd`
* Run the `setuptools` install process with the following command: `python setup.py install`
* From here, you should have a `ucsd_cloud_cli` command that runs the code within this project installed to your python packages directory


## Using the Docker Image

If you'd prefer to use the Docker image and have Docker installed locally, once you've downloaded (`git clone` or otherwise) this project, you can build with the following command:

```bash
docker build -t ucsd_cloud_cli .
```

This will build an `alpine` and `python3.6`-based docker container named `ucsd_cloud_cli` locally. Running the Command Line Interface (CLI) through this interface is straightforward:

```bash
docker run -v $(HOME)/.aws:/root/.aws ucsd_cloud_cli <command> <arguments> <options>
```

This is functionally equivalent to running the above command `ucsd_cloud_cli <command> <arguments> <options>` with the benefit of running it in an consistent Docker container. Note that we also assume that you've set up a local credentials file and we simply map it in via a volume mount to the container.

## Installed Dependencies

This toolset leverages the following core dependencies:
* [boto3](https://boto3.readthedocs.io/en/latest/) sdk - AWS programmatic interactions
* [click](http://click.pocoo.org/5/) - handles the command-line experience and interface
* [troposphere](https://github.com/cloudtools/troposphere) - used to compose CloudFormation templates to avoid string-based JSON errors and other easy to make mistakes.
  * this is truly a time saver and avoids the frustration of building large CloudFormation by offering programmatic syntax and structural validation checks

## Configuring AWS Plugin for Splunk

UCSD is utilizing the [AWS Plugin](http://docs.splunk.com/Documentation/AddOns/released/AWS/Setuptheadd-on) for Splunk which will need to be configured after the overall log shipping/centralization templates have been installed in each AWS account.

The following will be configured to flow logs into S3:

* CloudTrail

This process will then fire SQS notifications which Splunk will use to determine which file(s) to pick up and ingest from the S3 bucket(s) configured. Within Splunk, the [SQS-based S3 input](http://docs.splunk.com/Documentation/AddOns/released/AWS/SQS-basedS3) should be used and wired up to the proper queue(s) and credentials.

CloudWatch Logs have a specific structure for ingest into Splunk via the [Cloudwatch Log Input](http://docs.splunk.com/Documentation/AddOns/released/AWS/SQS-basedS3).

The `target` template which is to be installed on the account for use as the 'centralized logging repository' creates an IAM user and (optionally, based on including the `--output-keys` flag at the time the template is generated) a set of credentials that are included in the CloudFormation template outputs for copy/paste into the Splunk configuration for the AWS plugin. Otherwise, the only manual step required here is to go to the IAM console, find the IAM user specified by the CloudFormation Output `splunkAccountUserName` and generate a set of AWS API credentials for use within the Splunk AWS Plugin config.

## Click CLI

Click offers a simple CLI integration tool set that has a rich set of parsers and help functions to make the user's experience as simple as possible. Note that the screen shots below were run on a development machine. When installed, rather than typing `python -m ucsd_cloud_cli` from the same directory of the project, the `ucsd_cloud_cli` command will be available whenever the proper `virtualenv` is enabled (in our case above, named `ucsd`)

### Top Level Help

![Top Level Help](doc/top_level_help.png)

The top level help shows the various commands available. Since this is a hierarchical set of commands, there are a few different pathways to manage logging source and target CloudFormation scripts/deployments.

### Target Generate Arguments and Options

![Target Generate Help](doc/target_generate_help.png)

This image shows the help string when a user is attempting to generate the log target CloudFormation script. Note that details are pulled from the [docstring](https://www.python.org/dev/peps/pep-0257/) for the description of the command.

### Source Generate Arguments and Options

![Source Generate Help](doc/source_generate_help.png)

This image is a screenshot of the parameters available when generating a CloudFormation template to point a given account's logs to the 'Target' account configured with the template generated above.

### Source flow_log Arguments and Options

![Source Flow Log Help](doc/source_flow_log_help.png)

This image is a screenshot of the parameters available when generating a CloudFormation template to point a given VPC's flow logs to the in-account setup (as created by the `ccli source generate` template) to forward on for centralized storage.

### Prompt handling for CLI use

![CLI Prompt Example](doc/cli_prompt.png)

The above shows the CLI prompting the user for values including multi-value inputs that are parsed as comma separated value strings. To enable this at the command line, set the `CLI_PROMPT` environment variable to `TRUE`:

```bash
export CLI_PROMPT=TRUE
```

Options and arguments can be passed in via prompt or in non-interactive mode depending on whether or not this environment variable is set.

# Process Flows

![Log data workflow](doc/log-data-flow.png)

![Instance Isolation Workflow](doc/instance-isolation-workflow.png)

# Test Data

| Name | Account ID |
|------|------------|
| Secuity Test Account | 802640662990 |
| UCSD Test | 969379222189 |
| Infrastructure Test Account | 169929244869 |

## Test/Validation Commands

Command to generate target CloudFormation template for our 3 test accounts:

```bash
python -m ucsd_cloud_cli target generate -a 802640662990 -a 969379222189 -a 169929244869
```
