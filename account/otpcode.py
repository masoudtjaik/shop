import random


class OtpGenerator:

    @staticmethod
    def generate_otp():
        random_otp = 'ABCDEFGHJKNMQ23546'
        otp = ""
        for i in range(6):
            otp += random_otp[random.randint(0, 17)]
        return otp


if __name__=='__main__':
    otp_code = OtpGenerator()

    print("OTP:", otp_code.generate_otp())
