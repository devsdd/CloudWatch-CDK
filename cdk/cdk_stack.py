from aws_cdk import (
    core as cdk,
    aws_cloudwatch as cw
)
from cdk.load_yaml_config import load_config


class CdkStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        config = load_config("cdk/config.yaml")
        # only one dashboard now:
        # num_dashboards = len(config)
        dashboard = cw.Dashboard(self, id = "dashboard", dashboard_name = "IEM-Dashboard-CDK")

        for key in config:
            metrics = config[key]["metrics"]
        
            if key == "ECS":
                clusters = config[key]["clusters"]
            
                for cluster in clusters:
                    # print("cluster = " + cluster)
                    services = config[key]["clusters"][cluster]["services"]

                    for service in services:
                        # print("service = " + service)
                        for metric in metrics:
                            # print("metric = " + metric)
                            if metric == "RunningTaskCount":
                                ns = "ECS/ContainerInsights"
                            else:
                                ns = "AWS/ECS"

                            graphed_metric = cw.Metric(
                                metric_name = metric,
                                namespace = ns,
                                dimensions = dict(
                                    ClusterName = cluster,
                                    ServiceName = service,
                                ),
                                statistic = "Avg",
                            )
                        
                            cpu_widget = cw.GraphWidget(
                                title = key + " " + metric +  " " + service,
                                left = [graphed_metric],
                                width = 8,
                                height = 4
                            )
                            
                            dashboard.add_widgets(
                                cw.Row(
                                    cpu_widget
                                )
                            )
            elif key == "SQS":
                queues = config[key]["queues"]
                ns = "AWS/SQS"
                for queue in queues:
                    for metric in metrics:
                        # print("metric = " + metric)

                        graphed_metric = cw.Metric(
                            metric_name = metric,
                            namespace = ns,
                            dimensions = dict(
                                QueueName = queue,
                            ),
                            statistic = "Sum",
                        )
                    
                        widget = cw.GraphWidget(
                            title = key + " " + metric +  " " + queue,
                            left = [graphed_metric],
                            width = 8,
                            height = 4
                        )
                        
                        dashboard.add_widgets(
                            cw.Row(
                                widget
                            )
                        )
            # API GW part isn't working
            elif key == "ApiGateway":
                apis = config[key]["ApiId"]
                ns = "AWS/" + key
                # print("ns = " + ns)

                for api in apis:
                    for metric in metrics:
                        # print("metric = " + metric)

                        if metric == "4xx" or metric == "5xx" or metric == "Count":
                            metric_stat =  "Count"
                        elif metric == "Latency" or metric == "IntegrationLatency":
                            metric_stat =  "Avg"
                        
                        graphed_metric = cw.Metric(
                            metric_name = metric,
                            namespace = ns,
                            dimensions = dict(
                                Stage = '$default',
                                ApiId = api
                            ),
                            statistic = metric_stat,
                        )
                    
                        widget = cw.GraphWidget(
                            title = "API GW " + api + " " + metric,
                            left = [graphed_metric],
                            width = 8,
                            height = 4
                        )
                        
                        dashboard.add_widgets(
                            cw.Row(
                                widget
                            )
                        )
            elif key == "RDS":
                clusters = config[key]["clusters"]
            
                for cluster in clusters:
                    # print("cluster = " + cluster)
                    
                    for metric in metrics:
                        # print("metric = " + metric)
                        ns = "AWS/RDS"

                        graphed_metric = cw.Metric(
                            metric_name = metric,
                            namespace = ns,
                            dimensions = dict(
                                DBClusterIdentifier = cluster,
                            ),
                            statistic = "Avg",
                        )
                    
                        cpu_widget = cw.GraphWidget(
                            title = key + " " + metric +  " " + cluster,
                            left = [graphed_metric],
                            width = 8,
                            height = 4
                        )
                        
                        dashboard.add_widgets(
                            cw.Row(
                                cpu_widget
                            )
                        )
                
            # test_widget = cw.SingleValueWidget(
                    #     metrics = [cw.Metric(
                    #         metric_name = 'ResourceCount',
                    #         namespace = 'AWS/Usage',
                    #         dimensions = dict(
                    #         Type = 'Resource',
                    #         Resource = 'vCPU',
                    #         Service = 'EC2',
                    #         Class = 'Standard/OnDemand'
                    #         )
                    #     )],
                    #     width = 6,
                    #     height = 3,
                    # )        
        # for key in clusters:
        #     print("key = " + key)
        #     print(len(clusters))
