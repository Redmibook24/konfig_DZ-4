with open("output.bin", "rb") as f:
    data = f.read()
    print("Содержимое output.bin:")
    print(" ".join(f"{byte:02x}" for byte in data))
