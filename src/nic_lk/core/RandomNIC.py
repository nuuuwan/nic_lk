import random

from nic_lk.core.NIC import NIC


class RandomNIC:
    @staticmethod
    def generate_single():
        year_of_birth = random.randint(1970, 2000)
        gendered_day_of_year_of_birth = (
            random.randint(1, 366) + random.randint(0, 1) * 500
        )
        serial_no = random.randint(1, 999)
        nic_dummy = NIC.new_from_parts(
            year_of_birth,
            gendered_day_of_year_of_birth,
            serial_no,
            check_digit=0,
        )

        check_digit = nic_dummy.check_digit_computed
        nic = NIC.new_from_parts(
            year_of_birth,
            gendered_day_of_year_of_birth,
            serial_no,
            check_digit,
        )
        return nic

    @staticmethod
    def generate(n: int):
        nic_list = []
        for _ in range(n):
            nic_list.append(RandomNIC.generate_single())
        return nic_list


if __name__ == '__main__':
    for nic in RandomNIC.generate(10):
        print(f'\'{nic.nic_no}\',')
