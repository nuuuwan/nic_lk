from dataclasses import dataclass


@dataclass
class NICVersion:
    nic_version: str


NICVersion.NEW = NICVersion("NEW")
NICVersion.OLD = NICVersion("OLD")
