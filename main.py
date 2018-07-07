import yaml

# config file
try:
    stream = open("config.yaml", "r")
    config = yaml.load(stream)
except FileNotFoundError:
    print("Configuratiebestand (config.yaml) niet aanwezig")
    exit(1)

def main():
    print(config)

if __name__ == "__main__":
    main()