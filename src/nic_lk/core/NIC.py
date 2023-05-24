import datetime
from functools import cache, cached_property

from utils import TIME_FORMAT_DATE, Time

from nic_lk.core.Gender import Gender
from nic_lk.core.NICVersion import NICVersion


class NIC:
    def raise_invalid_nic_no(self):
        raise ValueError(f"Invalid NIC number: {self.nic_no}")

    def __init__(self, nic_no: str):
        self.nic_no = nic_no

    @cache
    def to_dict(self):
        return dict(
            nic_no=self.nic_no,
            nic_version=self.nic_version.nic_version,
            year_of_birth=self.year_of_birth,
            gendered_day_of_year_of_birth=self.gendered_day_of_year_of_birth,
            gender=self.gender.gender,
            day_of_year_of_birth=self.day_of_year_of_birth,
            date_of_birth_ut=self.date_of_birth_ut,
            date_of_birth=self.date_of_birth,
            serial_no=self.serial_no,
            check_digit=self.check_digit,
            new_nic_num=self.new_nic_num,
            check_digit_computed=self.check_digit_computed,
            is_valid=self.is_valid,
        )

    @cached_property
    def nic_version(self) -> NICVersion:
        n = len(self.nic_no)
        if n == 10:
            return NICVersion.OLD
        elif n == 12:
            return NICVersion.NEW

        self.raise_invalid_nic_no()

    @cached_property
    def year_of_birth(self) -> int:
        if self.nic_version == NICVersion.OLD:
            return int('19' + self.nic_no[0:2])

        if self.nic_version == NICVersion.NEW:
            return int(self.nic_no[0:4])

        self.raise_invalid_nic_no()

    @cached_property
    def gendered_day_of_year_of_birth(self) -> int:
        if self.nic_version == NICVersion.OLD:
            return int(self.nic_no[2:5])

        if self.nic_version == NICVersion.NEW:
            return int(self.nic_no[4:7])

        self.raise_invalid_nic_no()

    @cached_property
    def gender(self) -> Gender:
        if self.gendered_day_of_year_of_birth < 500:
            return Gender.MALE
        else:
            return Gender.FEMALE

    @cached_property
    def day_of_year_of_birth(self) -> int:
        return self.gendered_day_of_year_of_birth % 500

    @cached_property
    def date_of_birth_ut(self) -> int:
        if self.year_of_birth % 4 == 0:
            offset = 1
        else:
            offset = 2

        return int(
            (
                datetime.datetime(self.year_of_birth, 1, 1)
                + datetime.timedelta(days=self.day_of_year_of_birth - offset)
            ).timestamp()
        )

    @cached_property
    def date_of_birth(self) -> str:
        return TIME_FORMAT_DATE.stringify(Time(self.date_of_birth_ut))

    @cached_property
    def serial_no(self) -> str:
        if self.nic_version == NICVersion.OLD:
            return int(self.nic_no[5:8])

        if self.nic_version == NICVersion.NEW:
            return int(self.nic_no[7:11])

        self.raise_invalid_nic_no()

    @cached_property
    def check_digit(self) -> int:
        if self.nic_version == NICVersion.OLD:
            return int(self.nic_no[8])

        if self.nic_version == NICVersion.NEW:
            return int(self.nic_no[11])

        self.raise_invalid_nic_no()

    @cached_property
    def new_nic_num(self) -> str:
        if self.nic_version == NICVersion.NEW:
            return self.nic_no

        if self.nic_version == NICVersion.OLD:
            return f'{self.year_of_birth:04d}{self.gendered_day_of_year_of_birth:03d}{self.serial_no:04d}{self.check_digit:01d}'

        self.raise_invalid_nic_no()

    @cached_property
    def check_digit_computed(self) -> int:
        W_LIST = [8, 4, 3, 2, 7, 6, 5, 8, 4, 3, 2, 0]

        N = 12
        i_list = [int(i) for i in self.new_nic_num]

        total_sum = sum(
            list(
                map(
                    lambda i: i_list[i] * W_LIST[i],
                    range(N),
                )
            )
        )
        mod_10 = total_sum % 11
        if mod_10 == 0:
            return 0
        return (11 - mod_10) % 10

    @cached_property
    def is_valid(self) -> bool:
        return self.check_digit == self.check_digit_computed
