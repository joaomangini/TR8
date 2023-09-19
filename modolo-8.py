from troposphere import Template, Ref, Parameter, Output, Join
from troposphere.ec2 import Instance, SecurityGroup, SecurityGroupRule

template = Template()

instance_type_param = template.add_parameter(
    Parameter(
        "InstanceType",
        Description="Tipo da instância EC2",
        Type="String",
        Default="t2.micro",
        AllowedValues=["t2.micro", "t2.small", "t2.medium"],
    )
)

security_group = template.add_resource(
    SecurityGroup(
        "EC2SecurityGroup",
        GroupDescription="Permite tráfego SSH e HTTP",
        SecurityGroupIngress=[
            SecurityGroupRule(
                IpProtocol="tcp",
                FromPort="22",
                ToPort="22",
                CidrIp="0.0.0.0/0",
            ),
            SecurityGroupRule(
                IpProtocol="tcp",
                FromPort="80",
                ToPort="80",
                CidrIp="0.0.0.0/0",
            ),
        ],
    )
)

num_instances = 3
for i in range(num_instances):
    instance = template.add_resource(
        Instance(
            f"EC2Instance{i+1}",
            InstanceType=Ref(instance_type_param),
            SecurityGroups=[Ref(security_group)],
            KeyName="Leo",
            UserData="",

        )
    )

output_yaml = template.to_yaml()

with open("ec2_instances.yaml", "w") as f:
    f.write(output_yaml)
