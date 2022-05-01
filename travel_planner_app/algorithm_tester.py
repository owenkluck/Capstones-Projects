import math


def find_distance(current_latitude, current_longitude, next_latitude, next_longitude):
        # need to figure out how to calculate whether you are still going East or West.
        distance = math.acos(math.sin(current_latitude) * math.sin(next_latitude) +
                             math.cos(current_latitude) * math.cos(next_latitude) *
                             math.cos(next_longitude - current_longitude)) * 6371
        return distance


def main():
    print(find_distance(math.radians(40.851), math.radians(-96.7592), math.radians(12.8295), math.radians(45.0228)))
    print(math.sin(40))
    print(math.sin(40.851))
    print()
    print(math.cos(12))
    print(math.cos(12.8295))
    print()
    print(math.sin(12))
    print(math.sin(12.8295))

if __name__ == '__main__':
    main()
