import random


class OtpGenerator:

    @staticmethod
    def generate_otp():
        random_otp = 'ABCDEFGHIJKNMQ123546'
        otp = ""
        for i in range(6):
            otp += random_otp[random.randint(0, 19)]
        return otp


otp_code = OtpGenerator()

print("OTP:", otp_code.generate_otp())
