import csv
import math

submission_name = "Submission.csv"
simulation_range = range(1, 11)

########## Global Constants ##########

L0 = 20 # Upfront Pay
L1 = 8 # Normal Hour 
L2 = 12 # Peak Hour
L3 = 16 # Night Hour
L4 = 12 # Normal Hour (8th hour onwards)
L5 = 18 # Peak Hour (8th hour onwards)
L6 = 24 # Night Hour (8th hour onwards)

F1 = 0.35 # Fuel Cost per KM

P1 = 50 # Penalty for missed Request 
P2 = 20 # Penalty (every 10 minutes) for late return to depot

R0 = 4 # Flag-down Fare
R1 = 0.25 # Surcharge (Peak Hours)
R2 = 0.5 # Surcharge (Night Hours)
R3 = 1.25 # Distance Fare (per KM) (0th - 10th KM)
R4 = 1.75 # Distance Fare (per KM) (10th KM onwards)

########## Global Variables ##########

All_Requests_Served = []
All_Requests_Missed = []
All_Revenues = []
All_Labour_Costs = []
All_Fuel_Costs = []
All_Penalties = []
All_Profits = []

########## Global Functions ##########

def read_csv(filename):
    f = open(filename, 'r')
    lines = csv.reader(f)
    return list(lines)

def convert_integer(string):
    try: return int(string)
    except: return ""

def make_proper(integer):
    if 0 <= integer < 1440:
        return integer
    elif integer < 0:
        return make_proper(integer + 1440)
    elif integer >= 1440:
        return make_proper(integer - 1440)

def convert_time(string):
    hour, minute = string.split(":")
    integer = int(hour) * 60 + int(minute)
    return integer

def is_deployment_time(string):
    if (type(string) != str) or (len(string) < 7) or (":" not in string) or (string[-3:] not in (" AM", " PM")):
        return False
    string = string[:-3]
    hour = convert_integer(string.split(":")[0])
    minute = convert_integer(string.split(":")[1])
    if (hour == "") or (minute == ""):
        return False
    elif (0 < hour <= 12) and (minute == 0):
        return True
    else:
        return False

def convert_deployment_time(string):
    if not is_deployment_time(string):
        return ""
    if "AM" in string:
        string = string[:-3]
        hour, minute = string.split(":")
        if hour == "12":
            integer = (int(hour) + 12) * 60 + int(minute)
            integer = integer - 360
            integer = make_proper(integer)
            return integer
        else:
            integer = int(hour) * 60 + int(minute)
            integer = integer - 360
            integer = make_proper(integer)
            return integer
    elif "PM" in string:
        string = string[:-3]
        hour, minute = string.split(":")
        if hour == "12":
            integer = int(hour) * 60 + int(minute)
            integer = integer - 360
            integer = make_proper(integer)
            return integer
        else:
            integer = (int(hour) + 12) * 60 + int(minute)
            integer = integer - 360
            integer = make_proper(integer)
            return integer

def convert_request_time(string):
    hour, minute = string.split(":")
    integer = (int(hour) - 6) * 60 + int(minute)
    if integer < 0:
        return integer + 1440
    else:
        return integer

def convert_back(integer):
    integer = integer + 360
    integer = integer % 1440
    hour = ("00" + str(integer // 60))[-2:]
    minute = ("00" + str(integer % 60))[-2:]
    return (hour + ":" + minute)
    
def Simulation(k):

    ########## Read Data ##########

    Distance = read_csv("S{} - Distance.csv".format(k))
    for i in range(101): Distance[i] = list(map(lambda x: float(x), Distance[i]))

    TimePeakOne = read_csv("S{} - Time Peak One.csv".format(k))
    for i in range(101): TimePeakOne[i] = list(map(lambda x: convert_time(x), TimePeakOne[i]))

    TimeNormal = read_csv("S{} - Time Normal.csv".format(k))
    for i in range(101): TimeNormal[i] = list(map(lambda x: convert_time(x), TimeNormal[i]))

    TimePeakTwo = read_csv("S{} - Time Peak Two.csv".format(k))
    for i in range(101): TimePeakTwo[i] = list(map(lambda x: convert_time(x), TimePeakTwo[i]))

    TimeNight = read_csv("S{} - Time Night.csv".format(k))
    for i in range(101): TimeNight[i] = list(map(lambda x: convert_time(x), TimeNight[i]))

    RequestsTemp = read_csv("Requests.csv")[1:]
    Requests = [None]
    for i in range(1000):
        origin = int(RequestsTemp[i][1])
        destination = int(RequestsTemp[i][2])
        passenger_arrive = convert_request_time(RequestsTemp[i][3])
        passenger_leave = convert_request_time(RequestsTemp[i][4])
        if passenger_leave < passenger_arrive: passenger_leave += 1440
        row = [origin, destination, [passenger_arrive, passenger_leave]]
        Requests.append(row)

    ########## Driver Functions ##########

    def type_of_time(current_time):
        current_time = make_proper(current_time)
        if 0 <= current_time < 180:
            return "Peak One"
        elif 180 <= current_time < 720:
            return "Normal"
        elif 720 <= current_time < 1080:
            return "Peak Two"
        elif 1080 <= current_time < 1440:
            return "Night"
        
    def get_distance(current_location, new_location):
        return Distance[current_location][new_location]

    def get_time(current_location, new_location, current_time):
        if type_of_time(current_time) == "Peak One":
            return TimePeakOne[current_location][new_location]
        elif type_of_time(current_time) == "Normal":
            return TimeNormal[current_location][new_location]
        elif type_of_time(current_time) == "Peak Two":
            return TimePeakTwo[current_location][new_location]
        elif type_of_time(current_time) == "Night":
            return TimeNight[current_location][new_location]

    def get_revenue(current_time, distance):
        flagdown = R0
        if type_of_time(current_time) == "Peak One": surcharge = R1
        elif type_of_time(current_time) == "Normal": surcharge = 0
        elif type_of_time(current_time) == "Peak Two": surcharge = R1
        elif type_of_time(current_time) == "Night": surcharge = R2
        if distance <= 10:
            distance_rate = (int(math.ceil(distance)) * R3)
            distance_rate = (1 + surcharge) * (distance_rate)
        elif distance > 10:
            distance_rate = (int(math.ceil(10)) * R3) + (int(math.ceil(distance-10)) * R4)
            distance_rate = (1 + surcharge) * (distance_rate)
        return round(flagdown + distance_rate, 2)

    def get_labour_cost(start_time, current_time):
        if current_time % 60 != 0: current_time = current_time + (60 - current_time % 60)
        pay = L0
        counter = 1
        for time in range(start_time, current_time, 60):
            if type_of_time(time) == "Peak One":
                if counter <= 8: pay += L2
                else: pay += L5
            elif type_of_time(time) == "Normal":
                if counter <= 8: pay += L1
                else: pay += L4
            elif type_of_time(time) == "Peak Two":
                if counter <= 8: pay += L2
                else: pay += L5
            elif type_of_time(time) == "Night":
                if counter <= 8: pay += L3
                else: pay += L6
            counter += 1
        return round(pay, 2)

    def get_fuel_cost(total_distance):
        return round(F1 * total_distance, 2)

    def get_penalties(requests_missed, current_time):
        penalties = 0
        missed_penalties = requests_missed * P1
        penalties += missed_penalties
        if current_time > 1440:
            late_by = current_time - 1440
            late_by = (late_by//10) if (late_by % 10 == 0) else ((late_by//10) + 1)
            late_penalties = late_by * P2
            penalties += late_penalties
        return round(penalties, 2)

    ########### Driver Object ##########   

    class Driver:
        def __init__(self, index, deployment_time, driver_schedule):
            self.index = index
            self.schedule = driver_schedule
            
            self.start_time = deployment_time
            
            self.current_time = deployment_time
            self.current_location = 0
            self.total_distance = 0

            self.requests_served = 0
            self.requests_missed = 0

            self.revenue = 0
            self.labour_cost = 0
            self.fuel_cost = 0
            self.penalties = 0
            self.profit = 0

        def act(self):
            print("")
            print("---------- Driver {} Timeline -----------".format(self.index))
            print("")
            while self.schedule != []:
                if self.current_time >= 1440:
                    self.retire()
                    return
                elif self.current_time - self.start_time >= 840:
                    self.retire()
                    return
                request = self.schedule.pop(0)
                self.meet_request(request)
            self.retire()
            return

        def meet_request(self, request):
            origin = Requests[request][0]
            destination = Requests[request][1]
            passenger_arrive_time = Requests[request][2][0]
            passenger_leave_time = Requests[request][2][1]

            print("{} : Driver {} travel from P{} to P{} (No passenger)".format(convert_back(self.current_time), self.index, self.current_location, origin))           
            self.travel_without_passenger(origin)
            if self.current_time < passenger_arrive_time:
                self.current_time = passenger_arrive_time
                print("{} : Driver {} travel from P{} to P{} (Passenger of Request {})".format(convert_back(self.current_time), self.index, origin, destination, request))
                self.travel_with_passenger(destination)
                self.requests_served += 1
            elif passenger_arrive_time <= self.current_time <= passenger_leave_time:
                print("{} : Driver {} travel from P{} to P{} (Passenger of Request {})".format(convert_back(self.current_time), self.index, origin, destination, request))
                self.travel_with_passenger(destination)
                self.requests_served += 1
            elif self.current_time > passenger_leave_time:
                self.requests_missed += 1

        def travel_without_passenger(self, new_location):
            distance = get_distance(self.current_location, new_location)
            time = get_time(self.current_location, new_location, self.current_time)
            print("Distance: {} KM, Duration: {} minutes".format(distance, time))
            print("")

            self.current_time += time
            self.current_location = new_location
            self.total_distance += distance

        def travel_with_passenger(self, new_location):
            distance = get_distance(self.current_location, new_location)
            time = get_time(self.current_location, new_location, self.current_time)
            revenue = get_revenue(self.current_time, distance)
            print("Distance: {} KM, Duration: {} minutes, Revenue: $ {}".format(distance, time, revenue))
            print("")

            self.current_time += time
            self.current_location = new_location
            self.total_distance += distance
            self.revenue += revenue

        def retire(self):
            
            print("{}: Driver {} travel from P{} to P{} (No passenger)".format(convert_back(self.current_time), self.index, self.current_location, 0))                 
            self.travel_without_passenger(0)
            
            self.requests_missed += len(self.schedule)
            self.labour_cost = get_labour_cost(self.start_time, self.current_time)
            self.fuel_cost = get_fuel_cost(self.total_distance)
            self.penalties = get_penalties(self.requests_missed, self.current_time)
            self.revenue = round(self.revenue, 2)
            self.profit = round(self.revenue - self.labour_cost - self.fuel_cost - self.penalties, 2)

            self.print_status()

        def print_status(self):
            print("---------- Driver {} Report -------------".format(self.index))
            print("Requests Served:      {}".format(self.requests_served))
            print("Requests Missed:      {}".format(self.requests_missed))
            print("-----------------------------------------")
            print("Revenue:              {}".format(self.revenue))
            print("Labour Cost:          {}".format(self.labour_cost))
            print("Fuel Cost:            {}".format(self.fuel_cost))
            print("Penalties:            {}".format(self.penalties))
            print("-----------------------------------------")
            print("Profit:               {}".format(self.profit))
            print("-----------------------------------------")
            print("")

    ########## Submission File ##########
        
    Submission = read_csv("{}".format(submission_name))[1:]

    duplicate_check = []
    for i in range(1000):
        for j in range(2, 1002):
            n = Submission[i][j]
            n = convert_integer(n)
            if (type(n) == int) and (1 <= n <= 1000):
                duplicate_check.append(n)

    Drivers = []
    for i in range(1000):
        driver_index = Submission[i][0]
        driver_index = int(driver_index)
        deployment_time = Submission[i][1]
        deployment_time = convert_deployment_time(deployment_time)
        if type(deployment_time) != int: continue

        driver_schedule = []
        for j in range(2, 1002):
            n = Submission[i][j]
            n = convert_integer(n)
            if (type(n) == int) and (1 <= n <= 1000) and (duplicate_check.count(n) == 1):
                driver_schedule.append(n)

        Drivers.append(Driver(driver_index, deployment_time, driver_schedule))

    ########## Run ##########

    print("")        
    print("#############################################")
    print("##############  SIMULATION {}  ###############".format(k))
    print("#############################################")
    print("")

    for driver in Drivers:
        driver.act()

    Requests_Served = sum(map(lambda driver: driver.requests_served, Drivers))
    Requests_Missed = sum(map(lambda driver: driver.requests_missed, Drivers))
    Revenue = round(sum(map(lambda driver: driver.revenue, Drivers)),2 )
    Labour_Cost = round(sum(map(lambda driver: driver.labour_cost, Drivers)), 2)
    Fuel_Cost = round(sum(map(lambda driver: driver.fuel_cost, Drivers)), 2)
    Penalties = round(sum(map(lambda driver: driver.penalties, Drivers)), 2)
    Profit = round(sum(map(lambda driver: driver.profit, Drivers)), 2)

    All_Requests_Served.append(Requests_Served)
    All_Requests_Missed.append(Requests_Missed)
    All_Revenues.append(Revenue)
    All_Labour_Costs.append(Labour_Cost)
    All_Fuel_Costs.append(Fuel_Cost)
    All_Penalties.append(Penalties)
    All_Profits.append(Profit)

    def print_results():
        print("")
        print("#############################################")
        print("################  RESULTS {} #################".format(k))
        print("---------------------------------------------")
        print("Requests Served: {}".format(Requests_Served))
        print("Requests Missed: {}".format(Requests_Missed))
        print("---------------------------------------------")
        print("Revenue:         $ {}".format(Revenue))
        print("---------------------------------------------")
        print("Labour Cost:     $ {}".format(Labour_Cost))
        print("Fuel Cost:       $ {}".format(Fuel_Cost))
        print("Penalties:       $ {}".format(Penalties))
        print("---------------------------------------------")
        print("Profit:          $ {}".format(Profit))
        print("---------------------------------------------")
        print("#############################################")
        print("#############################################")
        print("")

    print_results()

########### Multiple Simulations ###########

if __name__== "__main__":
    for k in simulation_range:
        Simulation(k)

Average_Requests_Served = round(sum(All_Requests_Served)/len(All_Requests_Served), 2)
Average_Requests_Missed = round(sum(All_Requests_Missed)/len(All_Requests_Missed), 2)
Average_Revenue_Earned = round(sum(All_Revenues)/len(All_Revenues), 2)
Average_Labour_Cost = round(sum(All_Labour_Costs)/len(All_Labour_Costs), 2)
Average_Fuel_Cost = round(sum(All_Fuel_Costs)/len(All_Fuel_Costs), 2)
Average_Penalties = round(sum(All_Penalties)/len(All_Penalties), 2)
Average_Profits = round(sum(All_Profits)/len(All_Profits), 2)

print("")
print("##########################################################")
print("########################  FINAL  #########################".format(k))
print("##########################################################")
print("----------------------------------------------------------")
print("         AVERAGE REQUESTS SERVED:        {}".format(Average_Requests_Served))
print("         AVERAGE REQUESTS MISSED:        {}".format(Average_Requests_Missed))
print("----------------------------------------------------------")
print("         AVERAGE REVENUE EARNED:         $ {}".format(Average_Revenue_Earned))
print("----------------------------------------------------------")
print("         AVERAGE LABOUR COST:            $ {}".format(Average_Labour_Cost))
print("         AVERAGE FUEL COST:              $ {}".format(Average_Fuel_Cost))
print("         AVERAGE PENALTIES:              $ {}".format(Average_Penalties))
print("----------------------------------------------------------")
print("         AVERAGE PROFIT:                 $ {}".format(Average_Profits))
print("----------------------------------------------------------")
print("##########################################################")
print("##########################################################")
print("")
