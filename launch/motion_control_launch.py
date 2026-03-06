from ament_index_python.packages import get_package_share_path
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    meemaw_package_path = get_package_share_path("meemaw_bringup")
    joy_config_path = meemaw_package_path / "configs/ps.yaml"

    sim_time_arg = DeclareLaunchArgument(
        name="use_sim_time",
        default_value="false",
        choices=["true", "false"],
        description="Flag to enable use simulation time",
    )

    footprint_static_tf_node = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        arguments=[
            "--x",
            "0",
            "--y",
            "0",
            "--z",
            "-0.0685",
            "--yaw",
            "0",
            "--pitch",
            "0",
            "--roll",
            "0",
            "--frame-id",
            "base_link",
            "--child-frame-id",
            "base_footprint",
        ],
    )

    camera_static_tf_node = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        arguments=[
            "--x",
            "-0.05",
            "--y",
            "0",
            "--z",
            "-0.12",
            "--yaw",
            "0",
            "--pitch",
            "0",
            "--roll",
            "0",
            "--frame-id",
            "camera_link",
            "--child-frame-id",
            "base_link",
        ],
    )

    # diff_drive_node = Node(package="solid_octo", executable="diff_drive_controller")
    meemaw_interface_node = Node(
        package="meemaw_bringup", executable="motion_control_interface"
    )

    launch_teleop_twist_joy = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(get_package_share_path("teleop_twist_joy") / "launch/teleop-launch.py")
        ),
        launch_arguments={
            # "joy_config": "ps3",
            "config_filepath": str(joy_config_path),
        }.items(),
    )

    return LaunchDescription(
        [
            sim_time_arg,
            meemaw_interface_node,
            launch_teleop_twist_joy,
            camera_static_tf_node,
            footprint_static_tf_node,
        ]
    )
