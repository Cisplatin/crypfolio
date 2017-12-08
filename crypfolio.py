import yaml

if __name__ == '__main__':
    with open('portfolio.yaml', 'r') as stream:
        try:
            print yaml.load(stream)
        except yaml.YAMLError as exc:
            print exc
