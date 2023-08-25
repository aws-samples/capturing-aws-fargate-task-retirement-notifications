# Capturing AWS Fargate Task Retirement Notifications

This is a sample repository with an EventBridge rule and Lambda Function to
forward AWS Fargate task retirement notifications to a Slack channel.

1. Build the artifact with AWS SAM

    ```bash
    $ sam build --template cloudformation.yaml
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

### Cleanup

To clean up the cloudformation stack

```bash
$ sam delete
```