export class IotPipelineStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // IoT Core Topic Rule
    const iotRule = new iot.CfnTopicRule(this, 'SensorRule', {
      topicRulePayload: {
        actions: [{
          kinesis: {
            streamName: 'sensor-data-stream',
            partitionKey: '${timestamp()}'
          }
        }],
        sql: "SELECT * FROM 'factory/+/sensors'"
      }
    });

    // Kinesis Stream with enhanced fan-out
    const stream = new kinesis.Stream(this, 'SensorStream', {
      shardCount: 10,
      retentionPeriod: cdk.Duration.hours(24)
    });

    // Lambda Processor
    const processor = new lambda.Function(this, 'StreamProcessor', {
      runtime: lambda.Runtime.PYTHON_3_9,
      handler: 'processor.lambda_handler',
      code: lambda.Code.fromAsset('lambda'),
      environment: {
        SAGEMAKER_ENDPOINT: 'anomaly-detection-endpoint'
      }
    });

    stream.grantRead(processor);
  }
}