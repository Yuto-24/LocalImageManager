"""
This file is basic config file for the backend.
"""

from pydantic.dataclasses import dataclass


@dataclass
class Config:
    """ Config for all backend """
    img_dir: str
    log_path: str


config = Config(
    img_dir="/app/img",
    log_path="/var/log/backend.log",
)
