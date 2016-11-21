import boto.ec2


class Event:
    def __init__(self, instance_id, region, alarm_type, resource, description, severity, additional_info):
        """

        :param instance_id: Instance ID of the resource associated with the alarm.
        :param region: Region of the resource associated with the alarm.
        :param alarm_type: The type of alarm e.g. CPUUtilization.
        :param resource: AWS namespace of the resource e.g. AWS/EC2.
        :param description: Description of the alarm.
        :param severity: Must be set in constructor or in SN Event Rule. CloudWatch has no concept of severity.
        :param additional_info: A JSON representation of the entire SNS message from CloudWatch.
        """
        self.source = 'CloudWatch'
        self.instance_id = instance_id
        self.region = region
        self.type = alarm_type
        self.resource = resource
        self.description = description
        self.severity = severity
        self.additional_info = additional_info
        self.node = instance_id
        # Change node property to AWS name tag if resource namespace is AWS/EC2
        self.parse_alarm_resource()

    def parse_alarm_resource(self):
        if self.resource == 'AWS/EC2':
            self.node = self.__get_aws_name_tag()
        else:
            pass

    def __get_aws_name_tag(self):
        # Lookup instance by id
        conn = boto.ec2.connect_to_region(self.region)
        reservations = conn.get_all_instances(instance_ids=[self.instance_id])
        instance = reservations[0].instances[0]
        print("Name tag: ", instance.tags['Name'])
        # Return name tag.
        return instance.tags['Name']
