import json
import math


# --------------------------
# Function for distance
# --------------------------

def distance(point1, point2):
    return math.sqrt(
        (point2[0]-point1[0])**2 +
        (point2[1]-point1[1])**2
    )


# --------------------------
# Read JSON file
# --------------------------

with open("base_case.json","r") as file:
    data = json.load(file)


# --------------------------
# Convert warehouse list into dictionary
# --------------------------

warehouse_map = {}

for warehouse in data["warehouses"]:
    warehouse_map[warehouse["id"]] = warehouse["location"]


# --------------------------
# Store agent positions
# --------------------------

agent_locations = {}

for agent in data["agents"]:
    agent_locations[agent["id"]] = agent["location"]


# --------------------------
# Initialize report structure
# --------------------------

report = {}

for agent in data["agents"]:

    report[agent["id"]] = {
        "packages_delivered":0,
        "total_distance":0
    }


# --------------------------
# Package assignment
# --------------------------

for package in data["packages"]:

    warehouse_id = package["warehouse_id"]
    warehouse_location = warehouse_map[warehouse_id]

    nearest_agent = None
    minimum_distance = float('inf')



    # Find nearest agent
    for agent_id, location in agent_locations.items():

        d = distance(location, warehouse_location)

        if d < minimum_distance:
            minimum_distance = d
            nearest_agent = agent_id



    # Delivery simulation

    current_location = agent_locations[nearest_agent]

    pickup_distance = distance(
        current_location,
        warehouse_location
    )

    delivery_distance = distance(
        warehouse_location,
        package["destination"]
    )

    total_trip = pickup_distance + delivery_distance



    # Update report

    report[nearest_agent]["packages_delivered"] += 1

    report[nearest_agent]["total_distance"] += total_trip



    # Update agent position
    agent_locations[nearest_agent] = package["destination"]



# --------------------------
# Calculate efficiency
# --------------------------

best_agent = None
best_efficiency = float('inf')

for agent in report:

    packages = report[agent]["packages_delivered"]
    total = report[agent]["total_distance"]

    if packages > 0:
        efficiency = total/packages
    else:
        efficiency = 0


    report[agent]["total_distance"] = round(total,2)

    report[agent]["efficiency"] = round(
        efficiency,
        2
    )


    if packages>0 and efficiency < best_efficiency:

        best_efficiency = efficiency
        best_agent = agent



report["best_agent"] = best_agent


# --------------------------
# Save report
# --------------------------

with open("report.json","w") as file:

    json.dump(
        report,
        file,
        indent=4
    )


print("Report generated successfully")