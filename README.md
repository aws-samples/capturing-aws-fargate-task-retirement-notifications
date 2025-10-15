# Capturing AWS Fargate Task Retirement Notifications

This is a sample repository with an EventBridge rule and Lambda function to
capture AWS Fargate task retirement notifications and forward them to Slack.
This repository is a sample solution included in an [AWS containers
blog](https://aws.amazon.com/blogs/containers/improving-operational-visibility-with-aws-fargate-task-retirement-notifications/).

1. Build the artifact with AWS SAM

    ```bash
    $ sam build --template cloudformation.yaml --use-container
    ```

2. Deploy the artifact with AWS SAM, adding the Slack URI and Slack Channel in
   as parameters.

    ```bash
    $ sam deploy --guided
    ```

3. Push some sample AWS EventBridge events.

    ```bash
    $ aws events put-events --entries file://sample_service_event.json
    $ aws events put-events --entries file://sample_task_event.json
    ```

4. To clean up the cloudformation stack

    ```bash
    $ sam delete
    ```