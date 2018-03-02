import heapq as heap
filename = 'e_high_bonus'


class Ride:
    def __init__(self, start_row, start_col, finish_row, finish_col, early_start, late_finish, bonus, i):
        self.start_row = start_row
        self.start_col = start_col
        self.finish_row = finish_row
        self.finish_col = finish_col
        self.early_start = early_start
        self.late_finish = late_finish
        self.id = i
        self.score = 0
        self.distance = abs(finish_row - start_row) + abs(finish_col - start_col)
        self.init_dist = 0
        self.bonus = bonus

        self.calculate_score()

    def calculate_score(self, next_start=0, row=0, col=0):
        self.init_dist = abs(self.start_col - col) + abs(self.start_row - row)
        if self.init_dist + next_start <= self.early_start:
            self.score = self.bonus + self.distance
        elif self.init_dist + next_start + self.distance <= self.late_finish:
            self.score = self.distance

    def __repr__(self):
        return '(' + str(self.id) + ', ' + str(self.score) + ')'

    def __lt__(self, other):
        return self.score > other.score


class Vehicle:
    def __init__(self):
        self.rides = []
        self.row = 0
        self.col = 0
        self.busy = False
        self.finished_rides = 0
        self.rides_order = []
        self.next = 0

    def update_rides(self):
        this_ride = heap.heappop(self.rides)
        heap.heappush(self.rides, this_ride)

    def move(self, row, col):
        row_dist = abs(row - self.row)
        col_dist = abs(col - self.col)
        self.row = row
        self.col = col
        return [row_dist, col_dist]

    def assign_ride(self, ride):
        self.finished_rides += 1
        self.rides_order.append(ride.id)
        self.next += ride.init_dist + ride.distance
        self.row = ride.finish_row
        self.col = ride.finish_col

        return self

    def __lt__(self, other):
        return self.next < other.next


def start_process(ride, vehicle, grid_rows, grid_cols, bonus, sim_steps):
    pass


def init_tasks(vehicles, ride_queue):
    for i in range(len(vehicles)):
        next_vehicle = heap.heappop(vehicles)
        next_ride = heap.heappop(ride_queue)
        next_vehicle = next_vehicle.assign_ride(next_ride)
        heap.heappush(vehicles, next_vehicle)


def simulate(vehicles, ride_queue, t):
    time = 0
    while True:
        if (len(ride_queue) == 0) or time > t:
            break
        print(time)
        next_vehicle = heap.heappop(vehicles)
        time = next_vehicle.next
        new_scores = []

        for ride in ride_queue:
            ride.calculate_score(next_vehicle.next, next_vehicle.row, next_vehicle.col)
            heap.heappush(new_scores, ride)

        ride_queue = new_scores
        next_ride = heap.heappop(new_scores)
        next_vehicle = next_vehicle.assign_ride(next_ride)
        heap.heappush(vehicles, next_vehicle)


def main():
    with open(filename + '.in') as input_file:
        input_data = input_file.read()

    input_lines = input_data.splitlines()
    grid_rows, grid_cols, vehicle_no, rides_no, bonus, sim_steps = [int(i) for i in input_lines[0].split(' ')]
    ride_data = input_lines[1:]

    ride_queue = []
    for i in range(rides_no):
        ride = Ride(*[int(i) for i in ride_data[i].split(' ')], bonus, i)
        heap.heappush(ride_queue, ride)

    vehicle = []
    for i in range(vehicle_no):
        vehicle.append(Vehicle())

    # print(vehicle)
    # print(ride_queue)

    init_tasks(vehicle, ride_queue)
    simulate(vehicle, ride_queue, sim_steps)

    # start_process(ride, vehicle, grid_rows, grid_cols, bonus, sim_steps)
    write_file(vehicle)


def write_file(vehicle):
    with open(filename + '.out', 'w') as f:
        for car in vehicle:
            # rides = ' '.joincar.rides_order
            f.write(str(car.finished_rides) + ' ' + ' '.join([str(i) for i in car.rides_order]) + '\n')


main()
