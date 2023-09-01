from .parser import Parser

svd_file = "/Users/kush/Downloads/rp2040.svd.xml"

with open(svd_file, "r") as f:
    svd_content = f.read()

dev = Parser.convert(svd_content)
# print(dev.peripherals[0])
